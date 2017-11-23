import os


def directory(path, extension):
    list_dir = []
    list_dir = os.listdir(path)
    count = 0
    for file in list_dir:
        if file.endswith(extension):  # eg: '.txt'
            count += 1
    return count


def list_all_signposts_in_dataset(path,country,dataset,signposts):
    list_dir = os.listdir(path)
    for element in list_dir:
        if element.endswith(".svg"):
            signpost_id = element.rstrip(".svg")
            signposts.write("{},{},{}\n".format(country,dataset,signpost_id))


def main():

    extension = '.svg'
    region = "kor"
    release = raw_input("Release in pattern yyyy_mm: ")

    counts_file = open(r"C:\city\Signposts\Tools\{}_{}_counts.txt".format(region,release), "w")
    signposts = open(r"C:\city\Signposts\Tools\{}_{}_list.txt".format(region,release), "a")

    with open(r"C:\city\Signposts\Tools\{}.txt".format(region), "r") as f:
        content = f.readlines()
        for element in content:
            country = element.split(",")[0]
            dataset = element.split(",")[1].strip()
            path = r"C:\city\Signposts\02_Validation\{}\{}\{}\{}".format(release, region, country, dataset)

            list_all_signposts_in_dataset(path,country,dataset,signposts)

            counts = directory(path, extension)

            counts_file.write("{},{},{}\n".format(country,dataset,counts))

    counts_file.close()
    signposts.close()


main()