from random import choice

class RandomTalker :

    RESPONSES = [
        '今日は寒いね',
        '今日は暑いね',
        'チョコ食べたいなぁ'
    ]

    def __init__(self) : 
        pass

    def response(self, _) :
        return choice(RandomTalker.RESPONSES)