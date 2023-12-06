"""! @pykdgrav3_utils
This module reads the group statistics returned by PKDGRAV3

In the code, when calling GroupStats, the following struct is filled for
each Friends-of-Friends group. And then dumped into binary format to a file.
This file usually ends in `.fofstats`

struct TinyGroupTable:
  float rPot[3];
  float minPot;
  float rcen[3];
  float rcom[3];
  float vcom[3];
  float angular[3];
  float inertia[6];
  float sigma;
  float rMax;
  float fMass;
  float fEnvironDensity0;
  float fEnvironDensity1;
  float rHalf;
  int nBH;
  int nStar;
  int nGas;
  int nDM;
"""

import numpy as np

# Not sure about the inertia axes ordering!
tinyGroupTable = np.dtype(
    [
        ("rPot_x", "=f4"),
        ("rPot_y", "=f4"),
        ("rPot_z", "=f4"),
        ("minPot", "=f4"),
        ("rcen_x", "=f4"),
        ("rcen_y", "=f4"),
        ("rcen_z", "=f4"),
        ("rcom_x", "=f4"),
        ("rcom_y", "=f4"),
        ("rcom_z", "=f4"),
        ("vcom_x", "=f4"),
        ("vcom_y", "=f4"),
        ("vcom_z", "=f4"),
        ("angular_x", "=f4"),
        ("angular_y", "=f4"),
        ("angular_z", "=f4"),
        ("inertia_xx", "=f4"),
        ("inertia_yy", "=f4"),
        ("inertia_zz", "=f4"),
        ("inertia_xy", "=f4"),
        ("inertia_xz", "=f4"),
        ("inertia_yz", "=f4"),
        ("sigma", "=f4"),
        ("rMax", "=f4"),
        ("fMass", "=f4"),
        ("fEnvironDensity0", "=f4"),
        ("fEnvironDensity1", "=f4"),
        ("rHalf", "=f4"),
        ("nBH", "=i4"),
        ("nStar", "=i4"),
        ("nGas", "=i4"),
        ("nDM", "=i4"),
    ]
)


def open_fofstat(filename, ncounts=999):
    """!
    Read the fofstats for the input file.

    @param filename Name of the input fofstat filename
    @param ncounts Number of FoF groups to be read. A number higher than
        the total amount of groups will read the whole file. If the expected
        number of groups is above the default, it should be increased!
    @return array of tinyGroupTable types with the FoF statistics
    """
    fofstat_file = open(filename, "rb")
    fofstats = np.fromfile(fofstat_file, dtype=tinyGroupTable, count=ncounts)
    fofstat_file.close()
    return fofstats
