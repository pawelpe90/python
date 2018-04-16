# Create folder/directory
os.makedirs(directory)

# Check if dir exists
os.path.exists(directory)

# Rename
os.rename(current_file_name, new_file_name)

# Working directory
os.getcwd()

# Remove directories
os.removedirs(directory)

# Copy files
import shutil
shutil.copy(src, dst)

# Listing elements of directory
os.listdir(path)

# Take arguments from command line
sys.argv[i]

# Open file with explorer
from Tkinter import Tk
from tkFileDialog import askopenfilename
opts = {}
opts['filetypes'] = [('Shape files','.shp')]

Tk().withdraw()
fc = askopenfilename(**opts)

# Sort dict
def sort_by_x(data):
	return data["x"]
dict.sort(key=sort_by_x,reverse=False)

from functools import reduce
reduce(lambda x, y: x * y, nums)

minutes, seconds = divmod(seconds, 60)

for path,folder,files in os.walk(dir):