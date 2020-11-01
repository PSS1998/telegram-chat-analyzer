from telethon import TelegramClient, events, sync
from datetime import timezone, datetime, timedelta 
import numpy as np
from draw import draw

with open('api.config', 'r') as config_file:
    lines = config_file.readlines()
    api_id = int(lines[0])
    api_hash = lines[1][:-1]

client = TelegramClient('session_name', api_id, api_hash)
client.start()
print("Client started!")
my_id = client.get_me().id

username = input("Enter username (or phonenumber) e.g.: mohammad or +989374321123\n")
if username.isnumeric():
	username = int(username)
message_times = list()
total_msgs = client.get_messages(username).total

time_diffrence = timedelta(hours = 6)
receive_response_count = 0
receive_total_response_time = 0
sent_response_count = 0
sent_total_response_time = 0
num_sent_start_conversation = 0
num_receive_start_conversation = 0
num_total_sent = 0
num_total_receive = 0
count_conversation = 0
last_msg_date = 0
last_msg_id = 0
i = 0
for message in client.iter_messages(username):
    message_time = message.date.replace(tzinfo=timezone.utc).astimezone(tz=None)
    message_times.append([message_time, message.sender.id == my_id])
    i += 1
    print(" Message " + str(i) + " of " + str(total_msgs), end="\r")
    if message.sender.id == my_id:
        num_total_sent += 1
    else:
        num_total_receive += 1
    new_msg_date = message_time
    new_msg_id = message.sender.id == my_id
    if i != 1:
        if (new_msg_date < last_msg_date-time_diffrence):
            if message.sender.id == my_id:
                num_sent_start_conversation += 1
            else:
                num_receive_start_conversation += 1
            count_conversation += 1
        else:
            if last_msg_id != new_msg_id:
                if message.sender.id == my_id:
                    receive_response_count += 1
                    receive_response_time = (last_msg_date - new_msg_date).total_seconds()
                    receive_total_response_time += receive_response_time
                else:
                    sent_response_count += 1
                    sent_response_time = (last_msg_date - new_msg_date).total_seconds()
                    sent_total_response_time += sent_response_time
    last_msg_date = new_msg_date
    last_msg_id = new_msg_id

avg_sent_response_time = sent_total_response_time / sent_response_count
avg_receive_response_time = receive_total_response_time / receive_response_count

print('')
print("Number of total messages : "+str(num_total_receive+num_total_sent))
print("Number of total messages sent : "+str(num_total_sent))
print("Number of total messages received : "+str(num_total_receive))
print("Number of total conversations : "+str(count_conversation))
print("Number of total conversations sender started : "+str(num_sent_start_conversation))
print("Number of total conversations receiver started : "+str(num_receive_start_conversation))
print("Average response time of sender : "+str(avg_sent_response_time))
print("Average response time of receiver : "+str(avg_receive_response_time))
file_path = str(username) + "_times.npy"
np.save(file_path, np.array(message_times))
draw(file_path, True)