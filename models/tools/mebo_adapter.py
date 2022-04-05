import urllib.request
import json

class Mebo :
    def __init__(self, api_key, agent_id) :
        self.__endpoint = 'https://api-mebo.dev/api'
        self.__api_key = api_key
        self.__agent_id = agent_id

    def send_message(self, utterance, uid) :
        """
        params : 
            utterance
            uid
        return :
            success :  response_message
            error : ''
        """

        post_form_data = {
            "api_key" : self.__api_key,
            "agent_id" : self.__agent_id,
            "utterance" : utterance,
            "uid" : uid
        }
        post_form_headers = {
            'User-Agent' : 'curl/7.35.0',
            'Content-Type' : 'application/json'
        }

        post_req = urllib.request.Request(
            self.__endpoint, 
            data=json.dumps(post_form_data).encode('utf-8'), 
            headers=post_form_headers, 
            method='POST'
            )

        response_message = ''
        with urllib.request.urlopen(post_req) as res :
            body = json.loads(res.read())
            response_message = body['bestResponse']['utterance']
            
        return response_message
