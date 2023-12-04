import numpy as np


def calc_max_rmse(*values) -> float:
    """

    Calculate the Standard of max RMSE


    Returns
    -------
    float
        rmse of from values

    Equation
    -----
    devi = \max( \sqrt( < || val - <val>_f ||^2 > ) )
    """
    assert len(values), "Please input one more values"
    values = np.concatenate(values)  # Shape = (N_forcefield, F, N_atom, dim)
    avg_values = np.average(values, axis=0)  # Shape = (F, N_atom, dim)
    values_devi = values - avg_values  # Shape = (N_forcefield, F,  N_atom, dim)
    values_devi = np.sum(np.multiply(values_devi, values_devi), axis=-1)  # Shape = (N_forcefield, F, N_atom)
    values_devi = np.sqrt(np.average(values_devi, axis=-1))  # Shape = (N_forcefield, F)
    values_devi = np.max(values_devi, axis=0)
    return values_devi
