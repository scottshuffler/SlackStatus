import sys
import os.path
import datetime
import time as t
from slackclient import SlackClient


BOT_NAME = 'rpis'

slack_client = SlackClient('')
rpi_list = ["rpi2b", "rpi4b", "rpi5b", "rpi6b", "rpi7b"]
directory = "/usr/local/bee/beemon"
rpi = ""
date = ""
time = ""
full_path = ""
while True:
    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
    if slack_client.rtm_connect() and int(datetime.datetime.now().strftime("%H")) >= 8 or int(datetime.datetime.now().strftime("%H")) <= 22:
        x = 0
        slack_client.api_call("chat.postMessage", channel="#rpi_status", text="----- "+datetime.datetime.now().strftime("%H-%M-%S")+" -----",username='rpis', icon_emoji=':robot_face:')

        for x in range(len(rpi_list)):
            full_path += directory
            full_path += "/"
            full_path += rpi_list[x]
            full_path += "/"
            full_path += datetime.datetime.now().strftime("%Y-%m-%d/video")
            hours = (int(datetime.datetime.now().strftime("%H")) - 8) * 60
            minutes = hours + int(datetime.datetime.now().strftime("%M"))
            list_dir = []
            list_dir = os.listdir(full_path)
            count = 0
            for file in list_dir:
                if file.endswith(".h264"):
                    count += 1
            if minutes >= count and minutes-5 <= count:
                #print(rpi_list[x] + " is good, current uploads: " + str(count) + " current minutes pased: " + str(minutes))
                #slack_client.api_call("chat.postMessage", channel="#rpi_status", text=rpi_list[x] + " is good. Current uploads: " + str(count) + " current minutes pased: " + str(minutes)+" :tada:",username='rpis', icon_emoji=':robot_face:')
                slack_client.api_call("chat.postMessage", channel="#rpi_status", text=rpi_list[x] + " is good. :tada:",username='rpis', icon_emoji=':robot_face:')

                #sys.stdout.write(rpi_list[x] + " is good. Current uploads: " + str(count) + " current minutes pased: " + str(minutes)+"\r\n")
                #sys.stdout.flush()
            else:
                print("Too many minutes have passed since last upload, check " + rpi_list[x])
                slack_client.api_call("chat.postMessage", channel="#rpi_status", text=rpi_list[x]+" is struggling :finnadie:",username='rpis', icon_emoji=':robot_face:')
            # full_path += ".h264"
            # if glob.glob('/usr/local/bee/beemon/rpi2b/2017-02-28/video/05-03-*.h264'):
            #     print("Good")
            # else:
            #     print("No file found")
            full_path = ""
        slack_client.api_call("chat.postMessage", channel="#rpi_status", text="--------------------",username='rpis', icon_emoji=':robot_face:')

    t.sleep(300)

