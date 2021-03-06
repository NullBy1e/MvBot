import datetime


def getDate():
    date = datetime.datetime.now().strftime("%d%m%Y")
    return date


def getTime():
    offset = datetime.timezone(datetime.timedelta(hours=1))
    Hours = datetime.datetime.now(offset).strftime("%H")
    Minutes = datetime.datetime.now().strftime("%M")
    Seconds = datetime.datetime.now().strftime("%S")
    Time = Hours + ":" + Minutes + ":" + Seconds
    return Time


def log(Type, Message):
    date = getDate()
    time = getTime()
    try:
        logFile = open("Logs/{}.log".format(str(date)), "a")
        logFile.write(time + " " + Type + " " + Message + "\n")
    except:
        print('Please create the Logs folder in root dir!')
