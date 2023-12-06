"""! @pykdgrav3_utils
This class handles the unit convention used in PKDGRAV3

"""

import numpy as np


class units:
    KBOLTZ = 1.3806485e-16
    MHYDR = 1.6735575e-24
    MSOLG = 1.98847e33
    GCGS = 6.67408e-8
    KPCCM = 3.085678e21
    SIGMAT = 6.6524e-25
    LIGHTSPEED = 2.9979e10

    dMsolUnit = 1.0
    dKpcUnit = 1.0
    dGasConst = 1.0
    dErgPerGmUnit = 1.0
    dGmPerCcUnit = 1.0
    dSecUnit = 1.0
    dKmPerSecUnit = 1.0
    dComovingGmPerCcUnit = 1.0
    dMeanMolWeight = 1.0

    def __init__(self, Msol=None, Kpc=None, L=None, h=None, verbose=False):
        """!
        Computes pkdgrav3's unit conversion factors.

        There are two calling options. When Msol and Kpc are both given,
        the class just computes the remaining conversion factors. When L
        and h are both given, all conversion factors are computed.
        No other argument combination is allowed.

        @param Msol Mass unit, same as dMsolUnit in the parameters file
        @param Kpc Distance unit, same as dKpcUnit in the parameters file
        @param L Box size in Mpc / h
        @param h Dimensionless Hubble constant, H0 / (100 km s^-1 Mpc^-1)
        @param verbose Print all the resulting units after computing them
        """

        if Msol is not None and Kpc is not None:
            self.dMsolUnit = Msol
            self.dKpcUnit = Kpc
        elif L is not None and h is not None:
            self.dKpcUnit = L * 1e3 / h
            H0_cgs = 100 * h * 1e5 / (1e3 * self.KPCCM)
            critDens0_cgs = 3 * H0_cgs**2 / (8 * np.pi * self.GCGS)
            critDens0 = critDens0_cgs * (self.KPCCM**3 / self.MSOLG)
            self.dMsolUnit = critDens0 * self.dKpcUnit**3
        else:
            raise RuntimeError(
                "The units class takes either Msol and Kpc "
                "or L and h as valid argument combinations"
            )

        # Boltzmann constant / m_H in code units
        self.dGasConst = (
            self.dKpcUnit
            * self.KPCCM
            * self.KBOLTZ
            / (self.MHYDR * self.GCGS * self.dMsolUnit * self.MSOLG)
        )
        # code energy per unit mass --> erg per g
        self.dErgPerGmUnit = (
            self.GCGS * self.dMsolUnit * self.MSOLG / (self.dKpcUnit * self.KPCCM)
        )
        # code density --> g per cc
        self.dGmPerCcUnit = (self.dMsolUnit * self.MSOLG) / np.power(
            self.dKpcUnit * self.KPCCM, 3.0
        )
        # code time --> seconds
        self.dSecUnit = np.sqrt(1 / (self.dGmPerCcUnit * self.GCGS))
        # code speed --> km/s
        self.dKmPerSecUnit = (
            np.sqrt(
                self.GCGS * self.dMsolUnit * self.MSOLG / (self.dKpcUnit * self.KPCCM)
            )
            / 1e5
        )
        # code comoving density --> g per cc = msr->param.dGmPerCcUnit (1+z)^3
        # TODO
        self.dComovingGmPerCcUnit = self.dGmPerCcUnit

        if verbose:
            print("dMsolUnit = %e" % self.dMsolUnit)
            print("dKpcUnit = %e" % self.dKpcUnit)
            print("dGasConst = ", self.dGasConst)
            print("dErgPerGmUnit = ", self.dErgPerGmUnit)
            print("dGmPerCcUnit = ", self.dGmPerCcUnit)
            print("dSecUnit = ", self.dSecUnit)
            print("dKmPerSecUnit = ", self.dKmPerSecUnit)
            print("dComovingGmPerCcUnit = ", self.dComovingGmPerCcUnit)
