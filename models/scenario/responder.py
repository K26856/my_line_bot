from random import choice
import re
from models.tools.analyzer import MessageAnalyzer

class Responder :
    def __init__(self, dictionary, markov) :
        self._dictionary = dictionary
        self._markov = markov

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
        return choice(self._dictionary.random_messages)



class PatternTalker(Responder) : 
    def response(self, params) : 
        for ptn in self._dictionary.pattern_messages :
            matcher = re.match(ptn['pattern'], params['message']) 
            if matcher :
                chosen_message = choice(ptn['phrases'])
                return chosen_message.replace('%match%', matcher.group(0))
        return choice(self._dictionary.random_messages)

class TemplateTalker(Responder) :
    def response(self, params) :
        parts = MessageAnalyzer.analyze(params['message'])
        keywords = [word for word, part in parts if MessageAnalyzer.is_keyword(part)]
        count = len(keywords)
        if count > 0 and count in self._dictionary.template_messages :
            template = choice(self._dictionary.template_messages[count])
            for keyword in keywords :
                template = template.replace('%noun%', keyword, 1)
            return template
        else :
            return choice(self._dictionary.random_messages)

class MarkovTalker(Responder) :
    def response(self, params) :
        response_text = self._markov.make_sentence()
        if not response_text is None :
            return response_text
        else : 
            return choice(self._dictionary.random_messages)




        