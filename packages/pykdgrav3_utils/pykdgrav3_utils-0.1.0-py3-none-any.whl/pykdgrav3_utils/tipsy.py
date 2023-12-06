"""! @pykdgrav3_utils
This module handles the (deprecated) TIPSY format

"""

import numpy as np


# Read information from TIPSY files.
# This should be avoided, as HDF5 is the main format for I/O right now, but
# it is still useful to have this around.
#
# Note that the naming and ordering is different from HDF5!
def openTipsy(filename):
    """!
    Read information from TIPSY files.

    The use of this is now discouraged as the preferred format is HDF5.
    However, it is mantained here just in case it is needed.

    Note that the naming convention is different than with HDF5 snapshots

    @param filename Name of the file to be read
    @return Tuple with header, gas, dark, star arrays
    """
    header_type = np.dtype(
        [
            ("time", ">f8"),
            ("N", ">i4"),
            ("Dims", ">i4"),
            ("Ngas", ">i4"),
            ("Ndark", ">i4"),
            ("Nstar", ">i4"),
            ("pad", ">i4"),
        ]
    )

    gas_type = np.dtype(
        [
            ("mass", ">f4"),
            ("x", ">f4"),
            ("y", ">f4"),
            ("z", ">f4"),
            ("vx", ">f4"),
            ("vy", ">f4"),
            ("vz", ">f4"),
            ("rho", ">f4"),
            ("temp", ">f4"),
            ("hsmooth", ">f4"),
            ("metals", ">f4"),
            ("phi", ">f4"),
        ]
    )

    dark_type = np.dtype(
        [
            ("mass", ">f4"),
            ("x", ">f4"),
            ("y", ">f4"),
            ("z", ">f4"),
            ("vx", ">f4"),
            ("vy", ">f4"),
            ("vz", ">f4"),
            ("eps", ">f4"),
            ("phi", ">f4"),
        ]
    )

    star_type = np.dtype(
        [
            ("mass", ">f4"),
            ("x", ">f4"),
            ("y", ">f4"),
            ("z", ">f4"),
            ("vx", ">f4"),
            ("vy", ">f4"),
            ("vz", ">f4"),
            ("metals", ">f4"),
            ("tform", ">f4"),
            ("eps", ">f4"),
            ("phi", ">f4"),
        ]
    )

    tipsy = open(filename, "rb")
    header = np.fromfile(tipsy, dtype=header_type, count=1)
    header = dict(zip(header_type.names, header[0]))
    gas = np.fromfile(tipsy, dtype=gas_type, count=header["Ngas"])
    dark = np.fromfile(tipsy, dtype=dark_type, count=header["Ndark"])
    star = np.fromfile(tipsy, dtype=star_type, count=header["Nstar"])

    return header, gas, dark, star
