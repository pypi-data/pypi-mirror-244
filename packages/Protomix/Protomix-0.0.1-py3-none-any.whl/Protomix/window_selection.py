import pandas as pd

def window_selection(spectra_df: pd.DataFrame, range=(0.2, 10)) -> pd.DataFrame:
    """
    Extract a specified ppm range from the spectra_df DataFrame.
    
    Parameters:
    - spectra_df (pd.DataFrame): DataFrame where each row is a spectrum and columns are ppm values.
    - range (tuple): Start and end ppm values of the region to extract.
    
    Returns:
    - pd.DataFrame: Extracted spectra_df with the specified ppm range, retaining original indexes.
    """
    start_ppm, end_ppm = range
    
    # Extract the columns (ppm values) within the specified range
    cols_to_extract = [col for col in spectra_df.columns if start_ppm <= float(col) <= end_ppm]
    
    return spectra_df.loc[:, cols_to_extract]
