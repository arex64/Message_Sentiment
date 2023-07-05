import json
import requests
from elasticsearch import Elasticsearch


class BotController:
    def get_specific_attributes(msg):
        messages = msg
        result = ''
        for message in messages:
            result += f"{message.author.name}:"
            result += f"{message.content}"
            result += "\n"
            result += f"{message.created_at}"
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
