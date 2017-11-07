# test
# test2
import json
import datetime as dt

#inputData = {"Version":1,"TimeStamp":"2017-05-15T06:30:22.4313462+02:00","Days":[{"Date":"2017-04-26T00:00:00","Steps":6041,"StepsGoal":10000,"SleepMinutes":0,"SleepGoalMinutes":0,"WasRunning":False},{"Date":"2017-03-26T00:00:00","Steps":0,"StepsGoal":10000,"SleepMinutes":0,"SleepGoalMinutes":0,"WasRunning":False},{"Date":"2017-04-27T00:00:00","Steps":10606,"StepsGoal":10000,"SleepMinutes":0,"SleepGoalMinutes":0,"WasRunning":False},{"Date":"2017-04-28T00:00:00","Steps":10624,"StepsGoal":10000,"SleepMinutes":0,"SleepGoalMinutes":0,"WasRunning":False},{"Date":"2017-04-29T00:00:00","Steps":6534,"StepsGoal":10000,"SleepMinutes":0,"SleepGoalMinutes":0,"WasRunning":False},{"Date":"2017-05-01T00:00:00","Steps":11825,"StepsGoal":10000,"SleepMinutes":0,"SleepGoalMinutes":0,"WasRunning":False},{"Date":"2017-04-30T00:00:00","Steps":14045,"StepsGoal":10000,"SleepMinutes":0,"SleepGoalMinutes":0,"WasRunning":False},{"Date":"2017-05-03T00:00:00","Steps":3774,"StepsGoal":10000,"SleepMinutes":529,"SleepGoalMinutes":480,"WasRunning":False},{"Date":"2017-05-02T00:00:00","Steps":13320,"StepsGoal":10000,"SleepMinutes":0,"SleepGoalMinutes":0,"WasRunning":False},{"Date":"2017-05-04T00:00:00","Steps":7447,"StepsGoal":10000,"SleepMinutes":520,"SleepGoalMinutes":480,"WasRunning":False},{"Date":"2017-05-05T00:00:00","Steps":4771,"StepsGoal":10000,"SleepMinutes":564,"SleepGoalMinutes":465,"WasRunning":False},{"Date":"2017-05-06T00:00:00","Steps":4973,"StepsGoal":10000,"SleepMinutes":514,"SleepGoalMinutes":465,"WasRunning":False},{"Date":"2017-05-07T00:00:00","Steps":7573,"StepsGoal":10000,"SleepMinutes":444,"SleepGoalMinutes":465,"WasRunning":False},{"Date":"2017-05-08T00:00:00","Steps":13580,"StepsGoal":10000,"SleepMinutes":475,"SleepGoalMinutes":450,"WasRunning":True},{"Date":"2017-05-09T00:00:00","Steps":11141,"StepsGoal":10000,"SleepMinutes":418,"SleepGoalMinutes":450,"WasRunning":False},{"Date":"2017-05-10T00:00:00","Steps":12781,"StepsGoal":10000,"SleepMinutes":0,"SleepGoalMinutes":0,"WasRunning":False},{"Date":"2017-05-11T00:00:00","Steps":9571,"StepsGoal":10000,"SleepMinutes":291,"SleepGoalMinutes":450,"WasRunning":False},{"Date":"2017-05-12T00:00:00","Steps":9477,"StepsGoal":10000,"SleepMinutes":556,"SleepGoalMinutes":450,"WasRunning":False},{"Date":"2017-05-13T00:00:00","Steps":15233,"StepsGoal":10000,"SleepMinutes":0,"SleepGoalMinutes":0,"WasRunning":False},{"Date":"2017-05-14T00:00:00","Steps":12824,"StepsGoal":10000,"SleepMinutes":628,"SleepGoalMinutes":450,"WasRunning":False},{"Date":"2017-05-15T00:00:00","Steps":209,"StepsGoal":10000,"SleepMinutes":452,"SleepGoalMinutes":450,"WasRunning":False}]}
month = {"January": "01", "February": "02", "March": "03", "April": "04", "May": "05", "June": "06", "July": "07", "August": "08", "September": "09", "October": "10", "November": "11", "December": "12"}
print_text = "W dniu {}: Kroki: {}, Ilosc snu: {} "

def open_file():
    with open("Activity.db", "r") as f:
        for element in f:
            return json.loads(element)

def create_records(date, steps, sleep, run):
    return {"date": date, "steps": steps, "sleep": sleep, "run": run}


def upload_data(inputData):
    data = []
    for day in inputData["Days"]:
        date, steps, sleep, run = day["Date"],day["Steps"], day["SleepMinutes"], day["WasRunning"]
        data.append(create_records(date,steps,sleep,run))
    return data


def stats_for_month(data,input_month):
    data_month = []
    for record in data:
        if record["date"][5:7] == month[input_month]:
            date, steps, sleep, run = record["date"], record["steps"], record["sleep"], record["run"]
            data_month.append(create_records(date, steps, sleep, run))
    return data_month


def get_sort_by_date(data):
    return data["date"]

def get_sort_by_steps(data):
    return data["steps"]

def get_sort_by_sleep(data):
    return data["sleep"]


def print_stats_for_month():
    ask_for_data = True
    while ask_for_data:
        input_month = input("For which month you want see statistics? ").capitalize()
        sort_by = input("Do you want to sort data by date, steps or sleep? ").lower()

        if sort_by == "date":
            get_sort_value = get_sort_by_date
            ask_for_data = False
        elif sort_by == "steps":
            get_sort_value = get_sort_by_steps
            ask_for_data = False
        elif sort_by == "sleep":
            get_sort_value = get_sort_by_sleep
            ask_for_data = False
        else:
            print("Incorrect input! Try again!")

    data = upload_data(open_file())
    data_month = stats_for_month(data,input_month)
    data_month.sort(key=get_sort_value,reverse=True)
    steps_stats, sleep_stats = stats_for_value(data_month, "steps"), stats_for_value(data_month, "sleep")
    print_data(data_month, steps_stats, sleep_stats)


def stats_for_value(data, value): # calculates average amount of steps / hours of sleep for given period of time
    counter, deposit, daily_goal = 1, 0, 0
    for element in data:
        if element[value] > 0:
            deposit += int(element[value])# value = "steps" or "sleep"
            counter += 1

    if value == "steps":
        daily_goal = (deposit/counter)/100
    else:
        daily_goal = (deposit/counter)*0.2222

    return round(deposit / counter, 1), round(daily_goal, 1)


def print_data(data, steps_stats, sleep_stats): #input data is a list of dictonaries
    for element in data:
        print(print_text.format(element["date"][:10], element["steps"], round(element["sleep"]/60,1)))

    print()
    print("W danym okresie robiles srednio " + str(int(steps_stats[0])) + " krokow dziennie. (" + str(steps_stats[1]) +"% normy)")
    print("W danym okresie spales srednio " + str(int(sleep_stats[0]//60)) + "h " + str(int(sleep_stats[0]%60)) + "min dziennie. (" + str(sleep_stats[1]) +"% normy)")


def print_stats_for_day():
    data = upload_data(open_file())
    last_date = data[-1]["date"][5:10]
    last_record = data[-1]
    today_day = str(dt.date.today())[5:]
    today_day_time = str(dt.datetime.now())

    if today_day == last_date:
        print()
        print("Stan na " + today_day_time)
        print("Dzisiaj na zrobiles: " + str(last_record["steps"]) + " krokow.")
        if last_record["steps"] < 10000:
            print("Do wykonania dziennego celu brakuje " + str(10000-last_record["steps"]))
        print("Dzisiaj spales: " + str(int(last_record["sleep"]//60)) + "h " + str(int(last_record["sleep"]%60)) +"min.")
    else:
        print("No data from today! Synchronize data.")


def main():
    print("Jakie dane chcesz wyswietlic? ")
    print("[1] dla dzisiejszego dnia \n[2] dla wybranego miesiaca")
    choose = input("Podaj liczbe: ")
    true_input = True

    while true_input:
        if choose == "1":
            true_input = False
            print_stats_for_day()
        elif choose == "2":
            true_input = False
            print_stats_for_month()
        else:
            print("Incorrect input!")


main()