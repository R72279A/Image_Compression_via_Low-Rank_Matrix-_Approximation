import numpy as np
from .mathematical_engine import svd_engine

def compress_image(image_matrix, num_singular_values):
    """
    Purpose: Compress an image using SVD by retaining only a specified number of singular values.
    
    Inputs:
    - image_matrix: A 2D NumPy array representing the grayscale image.
    - num_singular_values: The number of singular values to retain for compression.
    
    Outputs:
    - compressed_image: The reconstructed image after compression.
    """
    
    # Input validation
    if not isinstance(image_matrix, np.ndarray):
        raise ValueError("image_matrix must be a NumPy array")
    
    if len(image_matrix.shape) != 2:
        raise ValueError("image_matrix must be a 2D array")
    
    if num_singular_values <= 0:
        raise ValueError("num_singular_values must be positive")
    
    # Ensure num_singular_values doesn't exceed matrix dimensions
    max_singular_values = min(image_matrix.shape)
    num_singular_values = min(num_singular_values, max_singular_values)
    
    # Perform SVD on the image matrix
    try:
        U, S, VT = svd_engine(image_matrix)
    except Exception as e:
        print(f"Error in SVD computation: {e}")
        return image_matrix  # Return original if SVD fails
    
    # Retain only the top 'num_singular_values' singular values
    S_reduced = np.zeros_like(S)
    S_reduced[:num_singular_values] = S[:num_singular_values]
    
    # Reconstruct the compressed image
    compressed_image = U @ np.diag(S_reduced) @ VT
    
    return compressed_image
