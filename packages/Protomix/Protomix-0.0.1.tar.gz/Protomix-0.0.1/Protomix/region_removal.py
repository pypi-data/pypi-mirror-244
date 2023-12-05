import pandas as pd 

def region_removal(spectra_df: pd.DataFrame, range=(4.5, 6.1)) -> pd.DataFrame:
    """
    Zero out specified ppm range in each spectrum in the DataFrame.
    
    Parameters:
    - spectra_df (pd.DataFrame): DataFrame where each row is a spectrum and columns are ppm values.
    - range (tuple): Start and end ppm values of the region to zero out.
    
    Returns:
    - pd.DataFrame: Updated spectra_df with the specified region zeroed out, retaining original indexes.
    """
    
    start_ppm, end_ppm = range
    
    # Extract the columns (ppm values) within the specified range
    cols_to_zero = [col for col in spectra_df.columns if start_ppm <= float(col) <= end_ppm]
    
    # Set values in the specified columns to zero
    spectra_df.loc[:, cols_to_zero] = 0
    
    return spectra_df