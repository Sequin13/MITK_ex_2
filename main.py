import time
import timeit
import plotly.graph_objects as go

import hashlib

# Dictionary to cache hash results
cache = {}

def hash_with_algorithm(algorithm: str, data: str = None, file_path: str = None):
    """
    Calculate the hash of the provided data or file using the specified algorithm.

    Args:
        algorithm (str): The name of the hash algorithm to use.
        data (str, optional): The data to be hashed. Defaults to None.
        file_path (str, optional): The path to the file to be hashed. Defaults to None.

    Returns:
        str: The hash value of the input data or file.
    """
    # Check if the result is already cached
    if (algorithm, data, file_path) in cache:
        return cache[(algorithm, data, file_path)]

    # Create hash object based on the specified algorithm
    hash_func = hashlib.new(algorithm)

    # Check if both data and file_path are provided, only one should be provided
    if data and file_path:
        raise ValueError("Only one argument must be provided")
    elif data:
        # Update hash with provided data
        hash_func.update(data.encode('utf-8'))
    elif file_path:
        # Update hash with contents of the file
        with open(file_path, 'rb') as binary_file:
            while chunk := binary_file.read(4096):
                hash_func.update(chunk)
    else:
        # If neither data nor file_path is provided, raise an error
        raise ValueError("Either 'data' or 'file_path' must be provided.")

    # Calculate hash value based on the algorithm
    if algorithm == "shake_128":
        hash_value = hash_func.hexdigest(16)
    elif algorithm == "shake_256":
        hash_value = hash_func.hexdigest(32)
    else:
        hash_value = hash_func.hexdigest()

    # Cache the result
    cache[(algorithm, data, file_path)] = hash_value

    # Return the hash value
    return hash_value


def file_hash_comparison(hash_result: str,
                         known_hash: str = "071d5a534c1a2d61d64c6599c47c992c778e08b054daecc2540d57929e4ab1fd"):
    """
    Compare the calculated hash with a known hash value.

    Args:
        hash_result (str): The calculated hash value.
        known_hash (str, optional): The known hash value for comparison. Defaults to "071d5a534c1a2d61d64c6599c47c992c778e08b054daecc2540d57929e4ab1fd" - it's Ubuntu hash.

    Returns:
        bool: True if the hash_result matches the known_hash, False otherwise.
    """

    if hash_result == known_hash:
        return True
    else:
        return False

def measure_hash_time(message_sizes: list, algorithm: str = 'sha256'):
    """
    Measure the time taken to hash messages of different sizes using a specified algorithm.

    Args:
        message_sizes (list): List of message sizes to measure.
        algorithm (str): The name of the hash algorithm to use. Defaults to 'sha256'.

    Returns:
        dict: A dictionary containing message sizes as keys and corresponding time taken to hash as values.
    """
    time_results = {}
    for size in message_sizes:
        message = 'a' * size
        time_taken = timeit.timeit(lambda: hash_with_algorithm(algorithm, data=message), number=1)
        time_results[size] = time_taken
    return time_results

def main():
    """
    Main function to demonstrate hashing and compare hash values.

    This function showcases the hashing of a file and compares the generated hash
    with a precomputed hash using different hashing algorithms. It also measures
    the time taken to hash messages of varying sizes and visualizes the results
    using a bar chart.

    Returns:
        None
    """

    # File paths
    data = r"C:\Users\kubac\Downloads\ubuntu-22.04.4-desktop-amd64.iso"
    data_txt = r"Pan Tadeusz.txt"

    # Get available hashing algorithms
    algorithms = hashlib.algorithms_available
    sha_hash = ""

    # Dictionary to store algorithm and its corresponding time
    alg_time_dict = {}

    # Iterate through algorithms, hash data, and measure time
    for algorithm in algorithms:
        start_time = time.time()
        hashed_data = hash_with_algorithm(algorithm, None, data_txt)
        end_time = time.time()
        elapsed_time = end_time - start_time
        if algorithm == "sha256":
            sha_hash = hashed_data
        alg_time_dict[algorithm] = elapsed_time
        print(f"Algorithm: {algorithm}, hashed value: {hashed_data}, time: {elapsed_time}")

    # Compare hash value with precomputed hash
    comparison_result = file_hash_comparison(sha_hash)
    if comparison_result:
        print("Correct hash")
    else:
        print("Wrong hash")

    # Measure hash time for different message sizes for sha256 hash
    message_sizes = [1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000]
    hash_time_results = measure_hash_time(message_sizes)

    # Visualize hash time results
    fig = go.Figure(data=go.Bar(x=list(hash_time_results.keys()), y=list(hash_time_results.values())))
    fig.update_layout(title='Elapsed time for hashing messages of different sizes',
                      xaxis_title='Message Size (characters)',
                      yaxis_title='Time (microseconds)')
    fig.show()


if __name__ == "__main__":
    main()
