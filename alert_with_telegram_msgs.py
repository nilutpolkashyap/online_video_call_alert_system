import paho.mqtt.client as paho
from Tkinter import *
import os
import requests

broker="192.168.XX.XX"    #IP address of computer running MQTT broker

beep = lambda x: os.system("echo -n '\a';sleep 0.2;" * x)

def telegram_bot_sendtext(bot_message):

   bot_token = 'TELEGRAM_BOT_TOKEN'
   bot_chatID = 'TELEGRAM_BOT_CHAT_ID'
   send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message

   response = requests.get(send_text)

   return response.json()


def alert_popup(title, message, path):
    root = Tk()
    root.title(title)

    w = 400     
    h = 200     

    sw = root.winfo_screenwidth()
    sh = root.winfo_screenheight()

    x = (sw - w)/2
    y = (sh - h)/2
    root.geometry('%dx%d+%d+%d' % (w, h, x, y))

    m = message
    m += '\n'
    m += path
    w = Label(root, text=m, width=120, height=10)
    w.pack()
    b = Button(root, text="OK", command=root.destroy, width=10)
    b.pack()
    mainloop()
    

def on_message(client, userdata, message):
	msg = str(message.payload.decode("utf-8"))

	print(msg)
	msg = int(msg)
	if(msg>900):
		beep(2)
		alert_popup("ALERT","ALERT","SOMEONE'S CALLING YOU!!!!!!")
		test = telegram_bot_sendtext("ALERT!! SOMEONE'S CALLING YOU!!!!!!")

client= paho.Client("client-001")
client.on_message=on_message

print("connecting to broker ",broker)
client.connect(broker)
print("subscribing ")
client.subscribe("sensor_data")
client.loop_forever()
