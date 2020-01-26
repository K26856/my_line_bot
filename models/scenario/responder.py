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

    def __init__(self) : 
        super().__init__(self)
        self.__responses = []

        with open('dics/random_message.dat', mode='r', encoding='utf-8') as f :
            for line in f : 
                if line :
                    line = line.strip()
                    self.__responses.append(line)

    def response(self, _) :
        return choice(self.__responses)
