import pandas as pd

def negative_values_zeroing(spectra_df: pd.DataFrame) -> pd.DataFrame:
    """
    Set all negative values in the spectra to zero.
    
    Parameters:
    - spectra (pd.DataFrame): DataFrame where each row is a spectrum.
    
    Returns:
    - pd.DataFrame: Spectra with negative values set to zero, retaining original indexes.
    """
    
    # Apply the zeroing operation to each row in the DataFrame
    corrected_spectra = spectra_df.apply(lambda spectrum: spectrum.where(spectrum >= 0, 0), axis=1)
    
    return corrected_spectra