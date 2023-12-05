import pandas as pd

def group_delay_removal(fid_df: pd.DataFrame, acqus_df: pd.DataFrame) -> pd.DataFrame:
    """
    Removes the group delay from the input FID data.
    
    Parameters:
    - fid_df (pd.DataFrame): Input FID data with rows as individual FID values and columns representing time.
    - acqus_df (pd.DataFrame): Input FID data with rows as individual FID values and columns representing time.
    
    Returns:
    - pd.DataFrame: FID data with group delay removed.
    """
    grpdly = int(acqus_df['$GRPDLY'][0])

    # Use DataFrame slicing to remove the group delay
    return fid_df.iloc[:, grpdly:]