import numpy as np

def svd_engine(A):
    """
    Purpose: Its only job is to take a matrix A and decompose it into its three SVD components: U, S, and Vᵀ.
    
    Inputs: It will take one argument: a NumPy matrix, which we can call A.
    
    Outputs: It will return three variables: the U matrix, a 1D array of singular values S, and the Vᵀ matrix.
    """
    
    # Handle edge cases
    if A.size == 0:
        raise ValueError("Input matrix A cannot be empty")
    
    # Compute A^T * A
    ATA = A.T @ A
    
    # Construct the S and V matrices
    eigenvalues, V = np.linalg.eigh(ATA)
    
    # Sort eigenvalues and eigenvectors in descending order
    sort_indices = np.argsort(eigenvalues)[::-1]
    eigenvalues = eigenvalues[sort_indices]
    V = V[:, sort_indices]
    
    # Calculate the singular values (S)
    # Handle negative eigenvalues due to numerical precision
    eigenvalues = np.maximum(eigenvalues, 0)
    S = np.sqrt(eigenvalues)
    
    # Let's compute U matrix
    U_columns = []
    
    for i in range(V.shape[1]):
        v_i = V[:, i]
        s_i = S[i]
        
        # Handle division by zero
        if s_i > 1e-10:  # Use threshold instead of exact zero
            u_i = (A @ v_i) / s_i
        else:
            u_i = np.zeros(A.shape[0])
        
        U_columns.append(u_i)
    
    # Assemble the U matrix from the list of columns
    U = np.stack(U_columns, axis=1)
    
    return U, S, V.T
