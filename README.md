# Telegram Analyzer

This program will enable you to analyze the messages that you sent to a specific user.<br/>
The resulting analyze contains chart of hours of your conversations, number of your conversations and how many times who initiated it and average response time in seconds of both users.<br/>
Based on : https://gitlab.com/mthcom/telegram-time-analyzer<br/>
WhatsApp Analyzer : https://github.com/PSS1998/whatsapp-chat-analyzer<br/>

## Setup

Step one:
```bash
pip install -r requirements.txt
```
Step two:

Create a file named **api.config** in which there are two lines. First line contains your `api_id` and second line contains your `api_hash`. To obtain these values visit [https://my.telegram.org](https://my.telegram.org).

## Usage

Run ```extract_time_data.py``` and it will ask you the username for which you want to analyze.
