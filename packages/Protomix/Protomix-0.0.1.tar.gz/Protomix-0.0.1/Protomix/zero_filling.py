import numpy as np
import pandas as pd

def zero_filling(fid_df: pd.DataFrame, acqus_df: pd.DataFrame, target_points: int = 5000) -> pd.DataFrame:
    """
    Zero-fill or add zeros to the end of FID signals in a DataFrame to achieve the target number of points.

    Parameters:
    - fid_df (pd.DataFrame): DataFrame containing FID signals in rows.
    - target_points (int): Target number of points.
    - acqus_df (pd.DataFrame): DataFrame containing acquisition parameters.

    Returns:
    - pd.DataFrame: DataFrame containing FID signals with zeros added to the end.
    """
    dwell_time = 1 / float(acqus_df['$SW_h'][0])
    current_points = fid_df.shape[1]
    total_points = current_points + target_points
    time_values = np.linspace(dwell_time, total_points * dwell_time, total_points)

    # Create a DataFrame of zeros with the new time values
    zero_fill_df = pd.DataFrame(0, index=fid_df.index, columns=time_values)

    # Concatenate the original DataFrame with the zero-filled DataFrame
    result_df = pd.concat([fid_df, zero_fill_df], axis=1)

    return result_df