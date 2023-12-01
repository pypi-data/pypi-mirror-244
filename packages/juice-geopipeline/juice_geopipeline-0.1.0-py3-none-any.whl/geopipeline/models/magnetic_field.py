"""
Module Description: Functions related to Jupiter's magnetic field analysis as provided by the PEP team.
"""

import JupiterMag as jm
import numpy as np

import spiceypy as spice

import matplotlib.pyplot as plt

JUPITER_RADII = spice.bodvrd('JUPITER', 'RADII', 3)[1]


def magnetic_field_vector(et_array):
    """
    Calculate the total magnetic field vector at a given array of times.

    Parameters
    ----------
    et_array : array-like
        Array of Ephemeris Times (ET).

    Returns
    -------
    np.ndarray
        Array containing the x, y, z components of the magnetic field in IAU_JUPITER coordinates (nT).
    """
    # positions in Jupiter radii and in IAU_JUPITER (1 Rj = 71492km)
    juipos, lt = spice.spkpos('JUICE', et_array, 'IAU_JUPITER', 'NONE', 'JUPITER')

    # use jrm33 internal magnetic field model in cartesian coordinates (x,y,z).
    # Input coordinates are in IAU_JUPITER in units of Jupiter radii (1 Rj = 71492 km)
    xyz = juipos / JUPITER_RADII

    # Internal magnetic field
    jm.Internal.Config(Model='jrm33', CartesianIn=True, CartesianOut=True)
    B_int = np.array(jm.Internal.Field(*xyz.T)).T

    # External magnetic field
    jm.Con2020.Config(equation_type='analytic', CartesianIn=True, CartesianOut=True)
    B_ext = np.array(jm.Con2020.Field(*xyz.T)).T

    B_total = B_int + B_ext

    B_total_reshaped = np.reshape(B_total, (-1, 3)).T
    # Reshape to have each element as a row of three elements
    B_total_final = np.reshape(B_total_reshaped, (-1, 3))
    # array with the x, y, z IAU_JUPITER components of the magnetic field in nT
    return B_total_final


def magnetic_field_lines(et_array, plot=False):
    """
    Trace magnetic field lines and optionally visualize them.

    Parameters
    ----------
    et_array : array-like
        Array of Ephemeris Times (ET).
    plot : bool, optional
        Flag to visualize the field lines (default: False).

    Returns
    -------
    jm.TraceField
        Object representing the traced magnetic field lines.
    """
    # positions in Jupiter radii and in IAU_JUPITER (1 Rj = 71492km)
    juipos, lt = spice.spkpos('JUICE', et_array, 'IAU_JUPITER', 'NONE', 'JUPITER')

    # use jrm33 internal magnetic field model in cartesian coordinates (x,y,z).
    # Input coordinates are in IAU_JUPITER in units of Jupiter radii (1 Rj = 71492 km)
    xyz = juipos / JUPITER_RADII

    # Trace field lines using the input positions
    T = jm.TraceField(*xyz.T, IntModel='jrm33', ExtModel='Con2020')

    if plot:
        # visualize the field lines
        ax = T.PlotRhoZ(label='JRM33 + Con2020', color='red')  # R_cylndrical,Z plot (IAU_JUPITER)
        plt.show()


    return T

def l_shell(et_array):
    """
    Calculate the L-shell distance of the magnetic equator from the planet center in jovian radii.

    Parameters
    ----------
    et_array : array-like
        Array of Ephemeris Times (ET).

    Returns
    -------
    np.ndarray
        Array containing the L-shell distances for each field line.
    """
    # T.R is the radial distance of any point on a traced field line.
    # The max distance of the field line in this field model coincides occurs at the magnetic equator crossing
    # This is termed as L-shell or M-shell, distance of the magnetic equator from the planet center in jovian radii
    # axis =1 is provided to get the L-shell from each of the four field lines
    T = magnetic_field_lines(et_array)

    # Calculate the L-shell
    lshell = np.nanmax(T.R, axis=1)

    return lshell


def pitch_angle(et_array, instrument='JUICE_PEP_JEI', direction=False):
    """
    Calculate the pitch angle of particles based on the given instrument direction.

    Parameters
    ----------
    et_array : array-like
        Array of Ephemeris Times (ET).
    instrument : str, optional
        Instrument name (default: 'JUICE_PEP_JEI').
    direction : array-like or False, optional
        Direction vector for the instrument in the instrument reference frame
        if not specified the instrument boresight is used (default: False).

    Returns
    -------
    list
        List of pitch angles for particles based on the instrument direction.
    """
    B_total = magnetic_field_vector(et_array)

    shape, frame, bsight, n, bounds = spice.getfvn(instrument, 99, 99, 99)

    pitch_angle = []  # Generate array for storing pitch angle

    for b_total_temp, et_temp in zip(B_total, et_array):  # loop through both the magnetic field and et-time using zip
        mat = spice.pxform(frame, 'IAU_JUPITER', et_temp)  # JEI boresight is given in JUICE_PEP_JEI
        if direction:
            bsight = direction

        boresight_iau = spice.mxv(mat, bsight)  # rotation matrix is pform, use it to transofrom JUICE_PEP_JEI bs to IAU_JUPITER

        # angle between field vector &  boresight, in deg
        # notice this is the angle of the detector to the magnetic field.
        # The particle comes into the detector from the "anti-boresight" direction, so the particle pitch angle is 180-detector_pitch_angle
        detector_pitch_angle = spice.convrt(spice.vsep(boresight_iau, b_total_temp), 'RADIANS', 'DEGREES')
        pitch_angle.append(180.0 - detector_pitch_angle)

    return pitch_angle