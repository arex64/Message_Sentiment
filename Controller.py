import json
from datetime import datetime
import requests
from elasticsearch import Elasticsearch
import discord


class BotController:
    def retrieve_messages(channel_id):
        headers = {
            'authorization': ''
        }

        url = f"https://discord.com/api/v9/channels/{channel_id}/messages?"

        params = {
            'limit': 100,
        }

        response = requests.get(url, headers=headers,
                                params=params)  # Make GET request to Discord API and retrieve messages
        print(response.text)
        if response.status_code == 200:
            return json.loads(response.text)

        else:
            print(f"Error: {response.status_code}")

    def get_specific_attributes(msg, timestamp1, timestamp2):
        if timestamp1 == None:
            timestamp1 = timestamp2
        elif timestamp2 == None:
            timestamp2 = timestamp1

        print(msg)
        messages = msg
        message_info = []
        result = ''
        for message in messages:
            print(message)
            message_timestamp = int(datetime.fromisoformat(message['timestamp']).timestamp()) // 1000
            if timestamp1 == timestamp2:  # Get messages with a timestamp after timestamp1
                if message_timestamp and timestamp1 >= timestamp1:
                    username = message["author"]["username"]
                    content = message['content']
                    timestamp = message['timestamp']
                    output = {'username': username, 'content': content, 'timestamp': timestamp}

                    if output not in message_info:
                        message_info.append(output)
                        print(message_info)
                    result += str(output)
                elif message_timestamp and timestamp2 <= timestamp2:
                    username = message["author"]["username"]
                    content = message['content']
                    timestamp = message['timestamp']
                    output = {'username': username, 'content': content, 'timestamp': timestamp}
                    if output not in message_info:
                        message_info.append(output)
                        print(message_info)
                    result += str(output)
            else:
                if timestamp1 <= message_timestamp <= timestamp2:  # Get messages with between timestamp1 and timestamp2
                    username = message["author"]["username"]
                    content = message["content"]
                    timestamp = message['timestamp']
                    output = {'username': username, 'content': content, 'timestamp': timestamp}

                    if output not in message_info:
                        message_info.append(output)
                        print(message_info)
        for message in message_info:
            result += f"{message['username']}:"
            result += f"{message['content']}"
            result += "\n"
            result += f"{message['timestamp']}"
            result += "\n"

        new_msg = json.dumps(result)
        print(new_msg)
        return new_msg

    def gpt_response(message):
        url = "https://cube10-ai.darkube.app/sentiment"
        print(message)
        mes = message
        payload = {
            'message': mes
        }
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=json.dumps(payload))
        print(response)
        jsn = json.loads(response.text)
        x2 = ''
        for i in range(len(jsn)):
            obj2 = str(
                jsn['sentiment'],
            )
            x2 += obj2
        msg_x = json.dumps(x2)
        print(msg_x)
        return msg_x

    def messages_elastic(dte_range, filtered_messages, msg_sentiment):
        payload = {
            'date range': dte_range,
            'message': filtered_messages,
            'sentiment': msg_sentiment,
        }
        es = Elasticsearch("https://cube10-elastic.darkube.app:443")
        cr_index = es.index(index="chat_sentiment", document=payload)
        return cr_index['result']

    # retrieve_messages('1117719750781448275')
