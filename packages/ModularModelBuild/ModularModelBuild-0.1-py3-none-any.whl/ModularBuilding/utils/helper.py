import os

def save_list_to_file(directory, filename, given_list):
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open(os.path.join(directory, filename), 'w') as f:
        for item in given_list:
            f.write("%s\n" % item)

def read_list_from_file(directory, filename):
    if not os.path.exists(os.path.join(directory, filename)):
        print(f"The file {filename} does not exist in the directory {directory}.")
        return
    with open(os.path.join(directory, filename), 'r') as f:
        lines = f.readlines()
    return [line.strip() for line in lines]
