import numpy as np

def convolution2d(input_matrix, kernel, stride=1):
    if not isinstance(input_matrix, np.ndarray) or not isinstance(kernel, np.ndarray):
        raise ValueError("Both input_matrix and kernel must be Numpy arrays.")
    
    if not input_matrix.size or not kernel.size or stride <= 0:
        raise ValueError("Input matrix and kernel must not be empty, and stride must be greater than 0.")

    input_rows, input_cols = input_matrix.shape
    kernel_rows, kernel_cols = kernel.shape

    # Check if the kernel size is smaller than the input size
    if input_rows < kernel_rows or input_cols < kernel_cols:
        raise ValueError("Kernel size must be smaller than or equal to the input matrix size.")

    # Calculate the output size
    output_rows = (input_rows - kernel_rows) // stride + 1
    output_cols = (input_cols - kernel_cols) // stride + 1

    # Initialize the output matrix
    output_matrix = np.zeros((output_rows, output_cols))

    # Perform the convolution
    for i in range(0, input_rows - kernel_rows + 1, stride):
        for j in range(0, input_cols - kernel_cols + 1, stride):
            output_matrix[i // stride, j // stride] = np.sum(input_matrix[i:i + kernel_rows, j:j + kernel_cols] * kernel)

    return output_matrix

# Example usage:
input_matrix = np.array([
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
])

kernel = np.array([
    [1, 0],
    [0, 1]
])

stride_value = 1

result = convolution2d(input_matrix, kernel, stride=stride_value)
print(result)
