import numpy as np

# Number of integers to generate
n = 1000000000  # Change this to a number that would approximately result in a 10GB file

# Generate random integers
data = np.random.randint(-10000, 10001, size=n)

# Save to a .npy file
np.save('synthetic_data.npy', data)

# Load the data from the .npy file
loaded_data = np.load('synthetic_data.npy')

# Convert to a Python list
loaded_data_list = loaded_data.tolist()

print(len(loaded_data_list))