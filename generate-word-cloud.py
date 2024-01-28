import matplotlib
matplotlib.use('Agg')

from telethon import TelegramClient, events, sync
from datetime import timezone, datetime, timedelta 
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from wordcloud import WordCloud
import re

# Telegram part
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

total_msgs = client.get_messages(username).total

# Collect messages
messages = []
i = 0
for message in client.iter_messages(username):
    i += 1
    print(" Message " + str(i) + " of " + str(total_msgs), end="\r")
    if message.text:
        messages.append(message.text)

client.disconnect()

# Word Cloud part
def clean_text(raw_list):
    raw_string = ' '.join(raw_list)
    no_links = re.sub(r'http\S+', '', raw_string)
    no_links = re.sub(r'\S+.com', '', no_links)
    return no_links

def create_words(clean_string):
    words = clean_string.split(" ")
    words = [w for w in words if len(w) > 3]  # ignore short words
    return words

# Generate the cloud
cleaned_text = clean_text(messages)
words = create_words(cleaned_text)
clean_string = ' '.join(words)
wc = WordCloud(background_color="white", max_words=2000)
wc.generate(clean_string)

plt.imshow(wc, interpolation='bilinear')
plt.axis("off")
#plt.show(block=True)
plt.savefig('word_cloud.png', format='png', dpi=300)
plt.close()
