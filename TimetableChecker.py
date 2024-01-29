import pandas as pd
import datetime as dt

lessonTimes = [dt.time(1, 0), dt.time(9, 0), dt.time(9, 55), dt.time(10, 50), dt.time(11, 10), dt.time(12, 5),
               dt.time(13, 0), dt.time(13, 55), dt.time(14, 50), dt.time(15, 45), dt.time(16, 40), dt.time(23, 50)]

data = pd.read_csv("data/timetable.csv")


def get_day():  # TODO
    w_day, now = get_current_data()
    if w_day > 5:
        return "no school today you silly goose"
    day = data.columns[w_day]
    d = data[day]

    for i in range(len(lessonTimes)):
        if lessonTimes[i] > now:
            # print(f"now is {now}, or {lessons[i - 1]}")
            # print(d[lesson])
            return d[i - 1]


def get_current_data():
    now1 = dt.datetime.now()
    now = dt.time(now1.hour, now1.minute)
    today = dt.date.today()

    return today.weekday() + 1, now

# print(get_day())