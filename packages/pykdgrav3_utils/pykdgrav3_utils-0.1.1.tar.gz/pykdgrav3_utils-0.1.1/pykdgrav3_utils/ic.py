"""! @pykdgrav3_utils
This module contains examples of initial condition file conversion
to pkdgrav3's HDF5 input format

"""

from glob import glob

import numpy as np

from . import hdf5, units


def from_gadget2binary(
    infile,
    outfile,
    init_gas_temp=None,
    init_hyd_abun=None,
    bMemSoft=False,
    bMemMass=False,
    ref_soft=None,
    ref_mass=None,
):
    """!
    Converts cosmological ICs from Gadget-2 binary format to pkdgrav3 HDF5 format.
    Assumes particle type 0 corresponds to gas particles and all other types to dark-
    matter particles. Either gas or dark-matter particles are optional.
    Gadget-2 units are assumed to be the following:
        Length: kpc / h
        Mass: 1e10 Msol / h
        Velocity: km / sec

    If init_gas_temp and init_hyd_abun are given, gas particle specific internal energies
    will be computed using them regardless of what is stored in the input file(s).

    @param infile The prefix string present in all the names of the input files to be read.
    @param outfile Name of the output file to be written. Will be overwritten if it exists.
    @param init_gas_temp Initial gas temperature in [K].
    @param init_hyd_abun Initial hydrogen abundance by mass.
    @param bMemSoft If set to True, particle softenings will be stored as a separate dataset
        in each PartType group. Requires ref_soft to be given. See documentation of hdf5.save
        function for more details.
    @param bMemMass Like bMemSoft, but for particle masses instead of softenings.
    @param ref_soft Reference softening value in [kpc / h] for a particle of mass ref_mass.
        Particle softenings are then this value scaled with the cubic root of the ratio of
        particle masses to ref_mass.
    @param ref_mass Reference particle mass in [1e10 Msol / h] for the softening value given
        in ref_soft. If omitted, the smallest particle mass will be used instead.
    """

    from scipy.io import FortranFile

    if bMemSoft:
        assert ref_soft is not None, (
            "Cannot store individual particle softenings if "
            "ref_soft is not provided. Aborting"
        )

    header_dtype = [
        "(6,)i4",
        "(6,)f8",
        "(1,)f8",
        "(1,)f8",
        "(1,)i4",
        "(1,)i4",
        "(6,)i4",
        "(1,)i4",
        "(1,)i4",
        "(1,)f8",
        "(1,)f8",
        "(1,)f8",
        "(1,)f8",
        "(1,)i4",
        "(1,)i4",
        "(6,)i4",
        "(16,)i4",
    ]

    file_list = glob(f"{infile:s}*")
    print(f"Found {len(file_list):d} IC file(s)")

    with FortranFile(file_list[0], "r") as gfile:
        header = gfile.read_record(*header_dtype)

    mass_table = header[1]
    a = header[2][0]
    z = header[3][0]
    npart = header[6]
    nfiles = header[8][0]
    L = header[9][0]
    Om = header[10][0]
    OL = header[11][0]
    h = header[12][0]
    npart_hw = header[15]

    assert nfiles == len(file_list), (
        "Number of files as per the file headers "
        "({:d}) does not match the number of files "
        "found ({:d}). Aborting".format(nfiles, len(file_list))
    )
    assert np.sum(npart_hw) == 0

    print("Unit system:")
    unit_sys = units.units(L=L * 1e-3, h=h, verbose=True)

    # If gas is present, set up its spec. internal energy
    read_gas_u = False
    if npart[0] > 0:
        if init_gas_temp is None or init_hyd_abun is None:
            gas_u = np.empty(npart[0], dtype=np.float32)
            read_gas_u = True
        else:
            # Mean mol. weight of neutral gas of primordial composition
            mu = 4.0 / (1.0 + 3.0 * init_hyd_abun)
            gamma = 5.0 / 3.0
            init_u = init_gas_temp * unit_sys.dGasConst / ((gamma - 1.0) * mu)
            gas_u = np.full(npart[0], init_u, dtype=np.float32)

    # Read particle data
    npart_tot = npart.sum()
    p_pos = np.empty((npart_tot, 3), dtype=np.float32)
    p_vel = np.empty((npart_tot, 3), dtype=np.float32)
    p_mass = np.empty(npart_tot, dtype=np.float32)
    p_type = np.empty(npart_tot, dtype=np.int32)
    start, start_gas = 0, 0
    for f in file_list:
        with FortranFile(f, "r") as gfile:
            n_thisfile = gfile.read_record(*header_dtype)[0]
            n_thisfile_tot = n_thisfile.sum()
            end = start + n_thisfile_tot

            read_mass = np.any(~(mass_table > 0.0) & (n_thisfile > 0))

            p_pos[start:end] = gfile.read_record("f4").reshape((n_thisfile_tot, 3))
            p_vel[start:end] = gfile.read_record("f4").reshape((n_thisfile_tot, 3))
            _p_id_unused = gfile.read_record("u4")
            if read_mass:
                temp_mass = gfile.read_record("f4")
            if read_gas_u and n_thisfile[0] > 0:
                end_gas = start_gas + n_thisfile[0]
                gas_u[start_gas:end_gas] = gfile.read_record("f4")
                start_gas = end_gas

        start_thisfile = start
        start_mass = 0
        for i in range(6):
            if n_thisfile[i] == 0:
                continue
            end_thisfile = start_thisfile + n_thisfile[i]

            p_type[start_thisfile:end_thisfile] = i

            if mass_table[i] > 0.0:
                p_mass[start_thisfile:end_thisfile] = mass_table[i]
            else:
                end_mass = start_mass + n_thisfile[i]
                p_mass[start_thisfile:end_thisfile] = temp_mass[start_mass:end_mass]
                start_mass = end_mass

            start_thisfile = end_thisfile

        start = end

    assert end == npart_tot

    # If provided, set up particle softenings
    if ref_soft is not None:
        if ref_mass is None:
            ref_mass = p_mass.min()

        ref_soft /= unit_sys.dKpcUnit * h
        p_soft = ref_soft * np.power(p_mass / ref_mass, 1.0 / 3.0)

    # Convert unit system and scale-factor dependencies
    p_pos = p_pos / L - 0.5
    p_vel = (p_vel / np.sqrt(a)) / unit_sys.dKmPerSecUnit
    p_mass = (p_mass * 1e10 / h) / unit_sys.dMsolUnit
    if read_gas_u:
        gas_u /= unit_sys.dKmPerSecUnit**2

    # Set up particle fields
    p_mask = (p_type == 0, p_type > 0)
    npart_write = (npart[0], npart[1:].sum())
    data_dict = {}
    start = 0
    for i in range(2):
        if npart_write[i] > 0:
            p_dict = data_dict[f"PartType{i:d}"] = {}

            p_dict["Coordinates"] = p_pos[p_mask[i]]
            p_dict["Velocities"] = p_vel[p_mask[i]]
            p_dict["Masses"] = p_mass[p_mask[i]]
            if ref_soft is not None:
                p_dict["Softening"] = p_soft[p_mask[i]]

            end = start + npart_write[i]
            p_dict["ParticleIDs"] = np.arange(start, end, dtype=np.uint64)
            start = end
    if npart[0] > 0:
        data_dict["PartType0"]["InternalEnergy"] = gas_u

    extra_groups = {
        "Header": {
            "Redshift": z,
            "OmegaLambda": OL,
            "Omega0": Om,
            "HubbleParam": h,
            "BoxSize": L * 1e-3,
        },
        "Units": {
            "MsolUnit": unit_sys.dMsolUnit,
            "KpcUnit": unit_sys.dKpcUnit,
            "SecUnit": unit_sys.dSecUnit,
            "KmPerSecUnit": unit_sys.dKmPerSecUnit,
        },
    }

    print(f"Saving converted ICs to {outfile:s}")
    hdf5.save(
        data_dict,
        outfile,
        time=a,
        bMemSoft=bMemSoft,
        bMemMass=bMemMass,
        extra_groups=extra_groups,
    )


def from_gadget2hdf5(
    infile,
    outfile,
    init_gas_temp=None,
    init_hyd_abun=None,
    bMemSoft=False,
    bMemMass=False,
    ref_soft=None,
    ref_mass=None,
):
    """!
    Converts cosmological ICs from Gadget-2 to pkdgrav3 HDF5 format. Assumes gas
    particles are stored in the PartType0 group and all other groups are dark-matter
    particles. Either gas or dark-matter particles are optional.
    Gadget-2 units are assumed to be the following:
        Length: kpc / h
        Mass: 1e10 Msol / h
        Velocity: km / sec

    If init_gas_temp and init_hyd_abun are given, gas particle specific internal energies
    will be computed using them regardless of what is stored in the input file(s). If not
    given, and the input file(s) does not contain internal energy, an error is raised.

    @param infile The prefix string present in all the names of the input files to be read.
    @param outfile Name of the output file to be written. Will be overwritten if it exists.
    @param init_gas_temp Initial gas temperature in [K]. Required if the ICs contain gas but
        not its internal energy.
    @param init_hyd_abun Initial hydrogen abundance by mass. Required if the ICs contain
        gas but not its internal energy.
    @param bMemSoft If set to True, particle softenings will be stored as a separate dataset
        in each PartType group. Requires ref_soft to be given. See documentation of hdf5.save
        function for more details.
    @param bMemMass Like bMemSoft, but for particle masses instead of softenings.
    @param ref_soft Reference softening value in [kpc / h] for a particle of mass ref_mass.
        Particle softenings are then this value scaled with the cubic root of the ratio of
        particle masses to ref_mass.
    @param ref_mass Reference particle mass in [1e10 Msol / h] for the softening value given
        in ref_soft. If omitted, the smallest particle mass will be used instead.
    """

    import h5py

    if bMemSoft:
        assert ref_soft is not None, (
            "Cannot store individual particle softenings if "
            "ref_soft is not provided. Aborting"
        )

    file_list = glob(f"{infile:s}*")
    print(f"Found {len(file_list):d} IC file(s)")

    has_gas_u = False
    for f in file_list:
        assert h5py.is_hdf5(f), f"File {f:s} is not an HDF5 file. Aborting"
        if has_gas_u:
            continue
        with h5py.File(f, "r") as gfile:
            has_gas_u = "PartType0/InternalEnergy" in gfile

    with h5py.File(file_list[0], "r") as gfile:
        attrs = gfile["Header"].attrs
        L = attrs.get("BoxSize")
        h = attrs.get("HubbleParam")
        a = attrs.get("Time")
        z = attrs.get("Redshift")
        OL = attrs.get("OmegaLambda")
        Om = attrs.get("Omega0")
        npart = attrs.get("NumPart_Total")[...]
        mass_table = attrs.get("MassTable")[...]
        nfiles = attrs.get("NumFilesPerSnapshot")

    assert nfiles == len(file_list), (
        "Number of files as per the file headers "
        "({:d}) does not match the number of files "
        "found ({:d}). Aborting".format(nfiles, len(file_list))
    )
    assert npart.sum() > 0, "IC files do not contain particles. Aborting"

    print("Unit system:")
    unit_sys = units.units(L=L * 1e-3, h=h, verbose=True)

    # Set up particle fields
    ptype_slice = (np.s_[0:1], np.s_[1:])
    data_dict = {}
    start = 0
    for i in range(2):
        n_thistype = npart[ptype_slice[i]]
        m_thistype = mass_table[ptype_slice[i]]
        n_total = n_thistype.sum()
        if n_total > 0:
            p_dict = data_dict[f"PartType{i:d}"] = {}

            p_dict["Coordinates"] = np.empty((n_total, 3), dtype=np.float32)
            p_dict["Velocities"] = np.empty((n_total, 3), dtype=np.float32)

            p_dict["Masses"] = np.empty(n_total, dtype=np.float32)
            for j, mass in enumerate(m_thistype):
                if mass == 0.0:
                    continue
                ni = n_thistype[:j].sum()
                nf = ni + n_thistype[j]
                p_dict["Masses"][ni:nf] = mass

            end = start + n_total
            p_dict["ParticleIDs"] = np.arange(start, end, dtype=np.uint64)
            start = end

    # Special case: If gas is present, set up its spec. internal energy
    read_gas_u = False
    if npart[0] > 0:
        if init_gas_temp is None or init_hyd_abun is None:
            assert has_gas_u, (
                "You must provide init_gas_temp and init_hyd_abun "
                "when gas internal energy is not in the input file(s)"
            )
            data_dict["PartType0"]["InternalEnergy"] = np.empty(
                npart[0], dtype=np.float32
            )
            read_gas_u = True
        else:
            # Mean mol. weight of neutral gas of primordial composition
            mu = 4.0 / (1.0 + 3.0 * init_hyd_abun)
            gamma = 5.0 / 3.0
            init_u = init_gas_temp * unit_sys.dGasConst / ((gamma - 1.0) * mu)
            gas_u = np.full(npart[0], init_u, dtype=np.float32)
            data_dict["PartType0"]["InternalEnergy"] = gas_u

    # Read particle data
    ptype_map = (0, 1, 1, 1, 1, 1)
    read_mass = mass_table == 0.0

    dmOffsets = np.cumsum(npart[1:-1])
    start = np.zeros(6, dtype=np.uint64)
    end = np.zeros(6, dtype=np.uint64)
    start[2:] = end[2:] = dmOffsets
    for f in file_list:
        with h5py.File(f, "r") as gfile:
            n_thisfile = gfile["Header"].attrs.get("NumPart_ThisFile")[...]
            for i in range(6):
                if n_thisfile[i] == 0:
                    continue
                end[i] = start[i] + n_thisfile[i]
                src = np.s_[: n_thisfile[i]]
                dst = np.s_[start[i] : end[i]]

                root = "PartType{:d}"
                p_group = gfile[root.format(i)]
                p_dict = data_dict[root.format(ptype_map[i])]

                p_group["Coordinates"].read_direct(p_dict["Coordinates"], src, dst)
                p_group["Velocities"].read_direct(p_dict["Velocities"], src, dst)
                if read_mass[i]:
                    p_group["Masses"].read_direct(p_dict["Masses"], src, dst)
                if i == 0 and read_gas_u:
                    p_group["InternalEnergy"].read_direct(
                        p_dict["InternalEnergy"], src, dst
                    )
                start[i] = end[i]

    assert np.all(end[:2] == npart[:2])
    assert np.all(end[2:] == dmOffsets + npart[2:])

    # If provided, set up particle softenings
    if ref_soft is not None:
        if ref_mass is None:
            min_mass = np.inf
            for p_dict in data_dict.values():
                curr_min = p_dict["Masses"].min()
                if curr_min < min_mass:
                    min_mass = curr_min
            ref_mass = min_mass

        ref_soft /= unit_sys.dKpcUnit * h
        for p_dict in data_dict.values():
            p_dict["Softening"] = ref_soft * np.power(
                p_dict["Masses"] / ref_mass, 1.0 / 3.0
            )

    # Convert unit system and scale-factor dependencies
    for p_dict in data_dict.values():
        p_dict["Coordinates"] = p_dict["Coordinates"] / L - 0.5
        p_dict["Velocities"] = (
            p_dict["Velocities"] / np.sqrt(a)
        ) / unit_sys.dKmPerSecUnit
        p_dict["Masses"] = (p_dict["Masses"] * 1e10 / h) / unit_sys.dMsolUnit
    if read_gas_u:
        data_dict["PartType0"]["InternalEnergy"] /= unit_sys.dKmPerSecUnit**2

    extra_groups = {
        "Header": {
            "Redshift": z,
            "OmegaLambda": OL,
            "Omega0": Om,
            "HubbleParam": h,
            "BoxSize": L * 1e-3,
        },
        "Units": {
            "MsolUnit": unit_sys.dMsolUnit,
            "KpcUnit": unit_sys.dKpcUnit,
            "SecUnit": unit_sys.dSecUnit,
            "KmPerSecUnit": unit_sys.dKmPerSecUnit,
        },
    }

    print(f"Saving converted ICs to {outfile:s}")
    hdf5.save(
        data_dict,
        outfile,
        time=a,
        bMemSoft=bMemSoft,
        bMemMass=bMemMass,
        extra_groups=extra_groups,
    )
