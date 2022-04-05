from random import choice, randrange
import re
from models.tools.analyzer import MessageAnalyzer
from models.tools.mebo_adapter import Mebo

class Responder :
    def __init__(self, dictionary, markov) :
        self._dictionary = dictionary
        self._markov = markov

    def response(self, params):
        """
            params : 
                message : text,
                user_id : user_id
        """
        pass

class Parrot(Responder) :
    def response(self, params) : 
        response_message = '{}ってなに？'.format(params['message'])
        return response_message



class RandomTalker(Responder) :
    def response(self, _) :
        return self._dictionary.select_random()



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
        template = self._dictionary.select_template(count)
        if len(template) > 0 :
            for keyword in keywords :
                template = template.replace('%noun%', keyword, 1)
            return template
        else :
            return self._dictionary.select_random()

class MarkovTalker(Responder) :
    def response(self, params) :
        parts = MessageAnalyzer.analyze(params['message'])
        keywords = [word for word, part in parts if MessageAnalyzer.is_keyword(part)]
        response_texts = []
        if len(keywords) > 0 :
            keyword = choice(keywords)
            temp_response = self._markov.make_sentence(keyword=keyword)
            if len(temp_response) > 0 :
                response_texts.append(temp_response)
            temp_response = self._markov.make_sentence(start_with=keyword)
            if len(temp_response) > 0 :
                response_texts.append(temp_response)
        response_texts.append(self._markov.make_sentence())
        return choice(response_texts)

class MeboTalker(Responder) :
    def __init__(self, mebo_api_key, mebo_agent_id) :
        self.__mebo = Mebo(mebo_api_key, mebo_agent_id)

    def response(self, params) :
        return self.__mebo.send_message(params['message'], params['user_id'])
