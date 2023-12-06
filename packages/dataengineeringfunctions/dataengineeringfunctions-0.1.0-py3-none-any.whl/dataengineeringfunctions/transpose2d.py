def transpose2d(input_matrix):
    # Check if the input_matrix is empty
    if not input_matrix:
        return []

    # Determine the number of rows and columns
    num_rows = len(input_matrix)
    num_cols = len(input_matrix[0])

    # Transpose the matrix
    transposed_matrix = [[0] * num_rows for _ in range(num_cols)]
    for i in range(num_rows):
        for j in range(num_cols):
            transposed_matrix[j][i] = input_matrix[i][j]

    return transposed_matrix

# Example usage:
matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

result = transpose2d(matrix)
print(result)
