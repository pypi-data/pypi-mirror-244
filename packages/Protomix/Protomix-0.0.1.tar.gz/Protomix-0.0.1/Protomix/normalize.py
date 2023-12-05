import pandas as pd
import numpy as np

def normalize(spectra_df: pd.DataFrame, method: str = 'PQN') -> pd.DataFrame:
    """
    Apply different normalization methods to a DataFrame of spectra.

    Parameters:
    - spectra_df (pd.DataFrame): The DataFrame containing the spectra with samples as rows and data points as columns.
    - method (str): The normalization method to apply. Options: 'PQN' (default), 'TotalArea', 'SNV'.

    Returns:
    - pd.DataFrame: The normalized spectra.
    """

    if method == 'PQN':
        # Probabilistic Quotient Normalization (PQN)

        # Step 1: Reference Spectrum Creation
        # Calculating the median spectrum across all samples to get the reference spectrum
        reference_spectrum = spectra_df.median(axis=0)

        # Step 2: Quotient Calculation
        # Calculating the quotients by dividing each spectrum by the reference spectrum
        quotients = spectra_df.divide(reference_spectrum, axis=1)

        # Step 3: Median Quotient Computation
        # Calculating the median quotient for each spectrum to get the scaling factors
        scaling_factors = quotients.median(axis=1)

        # Ensuring the scaling_factors are not zero to avoid division by zero errors
        scaling_factors.replace(0, 1, inplace=True)

        # Step 4: Normalization
        # Normalizing each spectrum by its respective scaling factor
        normalized_spectra = spectra_df.divide(scaling_factors, axis=0)

    elif method == 'TotalArea':
        # Total Area Normalization

        # Calculate the total area under the curve for each spectrum
        total_area = spectra_df.sum(axis=1)

        # Normalize each spectrum by dividing by the total area
        normalized_spectra = spectra_df.divide(total_area, axis=0)
        
    elif method == 'SNV':
        # Standard Normal Variate (SNV)

        # Centering each spectrum
        centered_spectra = spectra_df.subtract(spectra_df.mean(axis=1), axis=0)

        # Dividing each spectrum by the standard deviation
        std_dev = centered_spectra.std(axis=1)
        normalized_spectra = centered_spectra.divide(std_dev, axis=0)
    else:
        raise ValueError("Invalid normalization method. Choose from 'PQN', 'TotalArea', 'ReferenceCompound', 'SNV'.")

    return normalized_spectra