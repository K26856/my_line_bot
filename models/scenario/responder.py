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
        patterns = self._dictionary.select_pattern_messages(user_id=params['user_id'])
        match_patterns = []
        for pattern in patterns :
            matcher = re.match(pattern[0], params['message'])
            if matcher :
                match_patterns.append((pattern[0], pattern[1].replace('%match%', matcher.group(0)), pattern[2], pattern[3]))
        if len(match_patterns) == 0 :
            return ""
        else :
            chosen_pattern = choice(match_patterns)
            self._dictionary.update_user_info(params['user_id'], chosen_pattern[2], chosen_pattern[3])
            return chosen_pattern[1]

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
        parts = MessageAnalyzer.analyze(params['message'])
        keywords = [word for word, part in parts if MessageAnalyzer.is_keyword(part)]
        if len(keywords) > 0 :
            keyword = choice(keywords)
            response_text = self._markov.make_sentence(keyword=keyword)
        else :
            response_text = self._markov.make_sentence()
        if len(response_text) > 0 :
            return response_text
        else :
            return choice(self._dictionary.random_messages)
                