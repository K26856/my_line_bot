from random import choice

class Responder :
    def __init__(self) :
        pass

    def response(self, params):
        """
            params : 
                message : text
        """
        pass

class Parrot(Responder) :
    def response(self, params) : 
        response_message = '{}ってなに？'.format(params['message'])
        return response_message

class RandomTalker(Responder) :
    RESPONSES = [
        '今日は寒いね',
        '今日は暑いね',
        'チョコ食べたいなぁ'
    ]

    def response(self, _) :
        return choice(RandomTalker.RESPONSES)
        