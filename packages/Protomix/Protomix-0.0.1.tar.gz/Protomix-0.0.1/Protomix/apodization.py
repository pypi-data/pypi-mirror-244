import pandas as pd
import numpy as np

def apodization(fid_df: pd.DataFrame , LB: float = 1, apodization_type: str = 'gaussian') -> pd.DataFrame:
    """
    Applies an apodization function to each Free Induction Decay (FID) row in a DataFrame.

    Apodization, in the context of NMR (Nuclear Magnetic Resonance) spectroscopy, is a windowing technique applied to FID signals to enhance signal-to-noise ratio and line shape in the frequency domain. This function supports two types of apodization: Gaussian and Exponential.

    Parameters:
    - fid_df (pd.DataFrame): A DataFrame where each row represents an FID signal and columns represent time points.
    - LB (float, optional): Line broadening parameter, which determines the width of the apodization function. A higher value results in more broadening. Defaults to 1.
    - apodization_type (str, optional): Type of apodization function to apply. Options are 'gaussian' for Gaussian apodization, and 'exponential' for Exponential apodization. Defaults to 'gaussian'.

    Returns:
    - pd.DataFrame: A DataFrame of the same shape as fid_df, containing the apodized FID values. Each FID row in the input DataFrame is multiplied by the apodization function, transforming the data in the time domain.

    Raises:
    - AssertionError: If fid_df is not a pandas DataFrame, LB is negative, or apodization_type is not 'gaussian' or 'exponential'.
    """
    # Assertive lines
    assert isinstance(fid_df, pd.DataFrame), "fid_df should be a pandas DataFrame."
    assert LB >= 0, "LB should be non-negative."
    assert apodization_type in ['gaussian', 'exponential'], "apodization_type should be either 'gaussian' or 'exponential'."
    
    time = fid_df.columns.astype(float)
    
    if apodization_type == 'gaussian':
        apod_func = np.exp(-0.5 * (LB * time)**2)
    else:
        apod_func = np.exp(-LB * time)
    
    # Vectorized operation
    apodized_df = fid_df.multiply(apod_func, axis=1)
    
    return apodized_df