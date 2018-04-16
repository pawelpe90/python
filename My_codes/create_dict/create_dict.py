import os

input_dir = r"C:\Users\pruszyns\Documents\python-repo\My_codes\create_dict\input.txt"
dir = input("dir: ")
counter = 0

with open(input_dir) as i:
    for line in i:
        if not os.path.exists("{}\{}".format(dir, line.strip())):
            os.makedirs("{}\{}".format(dir, line.strip()))
            counter += 1

print("{} directories created".format(counter))