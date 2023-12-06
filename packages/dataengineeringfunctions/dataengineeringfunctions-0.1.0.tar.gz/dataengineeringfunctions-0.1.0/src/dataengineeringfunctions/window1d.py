import numpy as np

def window1d(input_array, size, shift=1, stride=1):
    if not input_array or size <= 0 or shift <= 0 or stride <= 0:
        return []

    # Convert input_array to Numpy array for consistent handling
    input_array = np.array(input_array)

    # Calculate the number of windows
    num_windows = ((len(input_array) - size) // shift) + 1

    # Generate the windows
    windows = [input_array[i * shift : i * shift + size : stride] for i in range(num_windows)]

    return windows

# Example usage:
input_data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
window_size = 3
shift_size = 2
stride_size = 1

result = window1d(input_data, size=window_size, shift=shift_size, stride=stride_size)
print(result)