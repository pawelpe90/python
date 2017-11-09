import urllib.request
import json
import datetime


# dict_keys(['stationId', 'stationName', 'aqIndex', 'values'])

def create_factor_dict():
    pass


def printer(container, condition, log_file):
    for element in container:
        if element['stationName'].startswith(condition):

            log_file.write(element['stationName'] + "\n")

            for factor, value in element['values'].items():
                log_file.write("{}: {}\n".format(factor, value))

            log_file.write("\n")


def main():
    current_time_and_date = str(datetime.datetime.now())[:19].replace(":", "-")
    # condition = input("City name: ")
    condition = "Łódź"

    log_file = open("log-file {} {}.txt".format(current_time_and_date, condition), "w", encoding='utf-8')

    with urllib.request.urlopen('http://powietrze.gios.gov.pl/pjp/current/getAQIDetailsList?param=AQI') as response:
        container = json.loads(response.read())

    printer(container, condition, log_file)

    log_file.close()


main()