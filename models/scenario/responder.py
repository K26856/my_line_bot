from random import choice
import re

class Responder :

    def __init__(self, dictionary) :
        self.__dictionary = dictionary

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

    def response(self, _) :
        return choice(self.__dictionary.random_messages)



class PatternTalker(Responder) : 

    def response(self, params) : 
        for ptn in self.__dictionary.pattern :
            matcher = re.match(ptn['pattern'], params['message'])
            if matcher :
                chosen_message = choice(ptn['phrases'])
                return chosen_message.replace('%match%', matcher[0])
        return choice(self.__dictionary.random_messages)