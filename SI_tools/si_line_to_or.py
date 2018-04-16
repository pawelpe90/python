output = open(r"C:\Users\pruszyns\Documents\python-repo\SI_tools\or_output.txt", "w")

counter = 0

with open(r"C:\Users\pruszyns\Documents\python-repo\SI_tools\input.txt", "r") as o:
    for line in o:
        output.write(line.rstrip("\n") + " OR ")
        counter += 1
        if counter == 60:
            output.write("\n")
            counter = 0

output.close()