from vkparser import VKParser
import schedule
import time



def Time():
    t = time.gmtime()
    return time.asctime(t)


def Logs(text):
    t = time.gmtime()
    time.asctime(t)
    text += '\n' + Time() + '\n' + ('=' * 10)
    my_file = open("logs.txt", 'a+')
    my_file.write(text)
    my_file.close()


def Main():
    Logs("Start working: ")
    vk_pars = VKParser()
    vk_pars.Main()


schedule.every().day.at("10:00").do(Main)
schedule.every().day.at("15:00").do(Main)
schedule.every().day.at("19:30").do(Main)

while True:
    try:
        schedule.run_pending()
        time.sleep(1)
    except Exception as Ex:
        Logs("Error: " + str(Ex))
        time.sleep(1)