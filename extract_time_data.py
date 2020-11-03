from telethon import TelegramClient, events, sync
from datetime import timezone, datetime, timedelta 
import numpy as np
import matplotlib.pyplot as plt
import re
from PIL import Image
from persian_wordcloud.wordcloud import PersianWordCloud, add_stop_words

from draw import draw



def create_wordcloud(username, messages):
    def removeWeirdChars(text):
        weridPatterns = re.compile("["
                                   u"\U0001F600-\U0001F64F"  # emoticons
                                   u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                   u"\U0001F680-\U0001F6FF"  # transport & map symbols
                                   u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                   u"\U00002702-\U000027B0"
                                   u"\U000024C2-\U0001F251"
                                   u"\U0001f926-\U0001f937"
                                   u'\U00010000-\U0010ffff'
                                   u"\u200d"
                                   u"\u2640-\u2642"
                                   u"\u2600-\u2B55"
                                   u"\u23cf"
                                   u"\u23e9"
                                   u"\u231a"
                                   u"\u3030"
                                   u"\ufe0f"
                                   u"\u2069"
                                   u"\u2066"
                                   u"\u200c"
                                   u"\u2068"
                                   u"\u2067"
                                   "]+", flags=re.UNICODE)
        return weridPatterns.sub(r' ', text)

    def clean_tweets(raw_list):
        while None in raw_list:
            raw_list.remove(None)
        raw_string = ' '.join(raw_list)
        no_links = re.sub(r'http\S+', '', raw_string)
        no_links = re.sub(r'\S+.com', '', no_links)
        return no_links

    def create_words(clean_string):
        words = clean_string.split(" ")
        words = [w for w in words if len(w) > 3]  # ignore a, to, at...
        return words

    raw_tweets = messages
    clean_text = clean_tweets(raw_tweets)
    words = create_words(clean_text)
    clean_string = ','.join(words)
    mask = np.array(Image.open('twitter-logo.jpg'))
    wc = PersianWordCloud(background_color="white", max_words=2000, mask=mask)
    clean_string = removeWeirdChars(clean_string)
    wc.generate(clean_string)
    plt.clf()
    plt.cla()
    plt.imshow(wc, interpolation='bilinear')
    plt.axis("off")
    plt.savefig(username + '.png', bbox_inches='tight')



with open('api.config', 'r') as config_file:
    lines = config_file.readlines()
    api_id = int(lines[0])
    api_hash = lines[1][:-1]

client = TelegramClient('session_name', api_id, api_hash)
client.start()
print("Client started!")
my_id = client.get_me().id

username = input("Enter username (or telegram id as a number) e.g.: mohammad or 81273618\n")
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
messages_recieve = []
messages_sent = []
i = 0
for message in client.iter_messages(username):
    # print(message.text)
    if message.sender.id == my_id:
        messages_sent.append(message.text)
    else:
        messages_recieve.append(message.text)
    message_time = message.date.replace(tzinfo=timezone.utc).astimezone(tz=None)
    message_times.append([message_time, message.sender.id == my_id])
    i += 1
    print(" Message " + str(i) + " of " + str(total_msgs), end="\r")
    if message.sender.id == my_id:
        num_total_sent += 1
    else:
        num_total_receive += 1
    new_msg_time = message_time
    new_msg_id = message.sender.id == my_id
    if i != 1:
        if (new_msg_time < last_msg_date-time_diffrence):
            if message.sender.id == my_id:
                num_sent_start_conversation += 1
            else:
                num_receive_start_conversation += 1
            count_conversation += 1
        else:
            if last_msg_id != new_msg_id:
                if message.sender.id == my_id:
                    receive_response_count += 1
                    receive_response_time = (last_msg_date - new_msg_time).total_seconds()
                    receive_total_response_time += receive_response_time
                else:
                    sent_response_count += 1
                    sent_response_time = (last_msg_date - new_msg_time).total_seconds()
                    sent_total_response_time += sent_response_time
    last_msg_date = new_msg_time
    last_msg_id = new_msg_id

avg_sent_response_time = sent_total_response_time / sent_response_count
avg_receive_response_time = receive_total_response_time / receive_response_count

print('')
with open(str(username)+"_analysis.txt", "w") as text_file:
    print("Number of total messages : "+str(num_total_receive+num_total_sent), file=text_file)
    print("Number of total messages sent : "+str(num_total_sent), file=text_file)
    print("Number of total messages received : "+str(num_total_receive), file=text_file)
    print("Number of total conversations : "+str(count_conversation), file=text_file)
    print("Number of total conversations sender started : "+str(num_sent_start_conversation), file=text_file)
    print("Number of total conversations receiver started : "+str(num_receive_start_conversation), file=text_file)
    print("Average response time of sender : "+str(avg_sent_response_time), file=text_file)
    print("Average response time of reciver : "+str(avg_receive_response_time), file=text_file)
file_path = str(username) + "_times.npy"
np.save(file_path, np.array(message_times))
draw(file_path, True)
create_wordcloud(username, messages_recieve)
create_wordcloud("me_"+username, messages_sent)