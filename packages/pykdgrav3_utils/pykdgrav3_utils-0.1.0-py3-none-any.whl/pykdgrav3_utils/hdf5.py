"""! @pykdgrav3_utils
This module handles I/O in HDF5 format.

"""

import h5py
import numpy as np

from . import units


def read_single(filename, return_units=True, convert_to_physical=False, verbose=False):
    """!
    Ultra-thin wrapper for reading single HDF5 snapshots

    @param filename Path to the snapshot to be read
    @return h5py.File with the snapshot, and if requested the units as extracted
        from the header.
    """

    snap = h5py.File(filename, "r")

    if return_units or convert_to_physical:
        MsolUnit = snap["Units"].attrs["MsolUnit"]
        KpcUnit = snap["Units"].attrs["KpcUnit"]
        u = units.units(MsolUnit, KpcUnit, verbose=verbose)

        if convert_to_physical:
            try:
                a = 1.0 / (snap["Header"].attrs["Redshift"] + 1.0)
            except:
                print("No 'Redshift' field detected!!")

            snap["PartType0/Density"][...] /= a**3
            # PKDGRAV3 outputs \dot{x}; x being the comoving coordinates
            snap["PartType0/Velocities"][...] *= a

    if return_units:
        return snap, u
    else:
        return snap


def save(
    data_dict, filename, time=0.0, bMemSoft=False, bMemMass=False, extra_groups={}
):
    """!
    Save data into a hdf5 snapshot prepared for PKDGRAV3

    This function takes the labels from the data_dict structure, such that
    it must already represent the tree structure of the snapshot. For example:

    PartType0
        |- Masses
        |- Coordinates
        |- Velocities
        |- Temperature

    PartType1
        |- Masses
        |- Coordinates
        |- Velocities

    NOTES:
        1. Even in the case of having the same mass for all particles,
           the 'Masses' array must be present.
        2. pkdgrav3 limits the total number of classes to 256. This means that,
           when using them, the number of unique particle softenings (if bMemSoft
           is False), particle masses (if bMemMass is False) or softening-mass
           pairs (if both bMemSoft and bMemMass are False) cannot exceed 256.

    @param data_dic Dictionary with the data and structure of the file to save.
    @param filename Name of the file which will be created.
    @param time Time of the snapshot. If using comoving coordinates, the
        scale factor is to be given instead.
    @param bMemSoft If set to True, particle softenings are stored as a separate
        dataset in each PartType group, and hence it requires a 'Softening' key
        to be provided for all PartTypes. If set to False and a 'Softening' key
        is provided for a given PartType, then said PartType group will have its
        softening values stored in classes. In any other case, no softening
        information will be stored.
    @param bMemMass Like bMemSoft, but for particle masses instead of softenings.
    @param extra_groups Dictionary of additional HDF5 groups to be stored in
        the file. Each of its items consist of the group name and a dictionary
        containing name-value pairs that will be stored as the group's attributes.
    """
    snap = h5py.File(filename, "w")

    gHeader = snap.create_group("Header")
    gHeader.attrs["Time"] = time

    for group_name, attrs in extra_groups.items():
        group = snap.require_group(group_name)
        for attr_name, value in attrs.items():
            group.attrs[attr_name] = value

    dTypes = {
        "default": "<f4",
        "Velocites": "<f4",
        "Coordinates": "<f8",
        "ParticleIDs": "<u8",
    }

    class_type = {
        "names": ["class", "mass", "soft", "start"],
        "formats": ["u1", "<f8", "<f8", "<u8"],
        "offsets": [0, 16, 24, 8],
        "itemsize": 40,
    }

    # pkdgrav3 limits the total number of classes to 256, so we enforce it.
    nMaxClasses = 256
    nPrevClasses = 0
    iStart = 0

    for partType in data_dict.keys():
        gPartType = snap.create_group(partType)
        partDict = data_dict[partType]

        mass_present = "Masses" in partDict.keys()
        assert (
            mass_present
        ), "No mass information has been given for {:s}. " "Aborting".format(partType)
        class_mass = not bMemMass

        soft_present = "Softening" in partDict.keys()
        if not soft_present:
            assert not bMemSoft, (
                "bMemSoft was set to True but "
                "no softening information has "
                "been given for {:s}".format(partType)
            )
            print(
                "WARNING: No softening information has been given "
                "for {:s}".format(partType)
            )
            class_soft = False
        else:
            class_soft = not bMemSoft

        # We can 'safely' assume that at least 'Coordinates' is present
        npart = partDict["Coordinates"].shape[0]

        # If not provided, make sure that the particleIDs are stored to assert
        # that unique IDs are generated
        if "ParticleIDs" not in partDict.keys():
            partDict["ParticleIDs"] = (
                np.arange(npart, dtype=dTypes["ParticleIDs"]) + iStart
            )
            iStart += npart

        for var in partDict.keys():
            if var == "Softening" and class_soft:
                continue
            if var == "Masses" and class_mass:
                continue

            if var in dTypes:
                var_type = dTypes[var]
            else:
                var_type = dTypes["default"]

            gPartType.create_dataset(var, data=partDict[var], dtype=var_type)

        if class_soft and class_mass:
            print(f"Storing {partType:s} softening and mass in classes")
            soft = partDict["Softening"]
            mass = partDict["Masses"]
        elif class_soft:
            print(f"Storing {partType:s} softening in classes")
            soft = partDict["Softening"]
            mass = np.zeros_like(soft)
        elif class_mass:
            print(f"Storing {partType:s} mass in classes")
            mass = partDict["Masses"]
            soft = np.zeros_like(mass)
        else:
            continue

        pairs = np.column_stack((mass, soft))
        upairs, inv = np.unique(pairs, axis=0, return_inverse=True)
        nClasses = upairs.shape[0]
        assert nClasses + nPrevClasses < nMaxClasses, (
            "Too many classes are needed. You should set bMemMass and/or "
            "bMemSoft to True"
        )

        # We always output a 'class' field to avoid having to deal with
        # particle order
        gPartType.create_dataset("class", data=inv.astype("|u1"))

        classes = np.zeros(nClasses, dtype=class_type)
        for i in range(nClasses):
            classes[i]["class"] = i
            classes[i]["mass"] = upairs[i, 0]
            classes[i]["soft"] = upairs[i, 1]
            # As we always output a 'class' field, the following is not needed
            classes[i]["start"] = 0

        gPartType.create_dataset("classes", data=classes)
        nPrevClasses += nClasses

    snap.close()
