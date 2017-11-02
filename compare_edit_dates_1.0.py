import os
import datetime

log_file = open("log.txt", "w")

def get_size_and_edit_date(directory):
    container = []
    for root, dirs, filenames in os.walk(directory):
        for name in filenames:
            path = root + "\\" + name
            t = os.path.getmtime(path)
            value = (name, os.path.getsize(path), str(datetime.datetime.fromtimestamp(t))[:19])
            container.append(create_dict(value))
    return container

def create_dict(element):
    return {"name": element[0], "size": element[1], "date": element[2]}

def get_sort_by(data):
    return data["name"]

def printer(values_1, values_2):
    for i in range(len(values_1)):
        if values_1[i]["size"] != values_2[i]["size"] or values_1[i]["date"] != values_2[i]["date"]:
            result = "changed"
        else:
            result = "OK"

        log_file.write("{} {} {}".format(values_1[i]["name"], values_1[i]["size"], values_1[i]["date"]).ljust(100))
        log_file.write("|||".center(5))
        log_file.write("{} {} {}".format(values_2[i]["name"], values_2[i]["size"], values_2[i]["date"]).ljust(100))
        log_file.write("|||".center(5))
        log_file.write("{}".format(result))
        log_file.write("\n")

def main():
    # dir_1 = sys.argv[1]
    # dir_2 = sys.argv[2]
    dir_1 = r"C:\Users\pruszyns\Google Drive\Python\Moje\buildings\data"  # old dir
    dir_2 = r"C:\Users\pruszyns\Google Drive\Python\Moje\buildings\data_2"  # new dir

    values_1 = get_size_and_edit_date(dir_1)
    values_1.sort(key=get_sort_by, reverse=False)
    values_2 = get_size_and_edit_date(dir_2)
    values_2.sort(key=get_sort_by, reverse=False)

    printer(values_1, values_2)

main()