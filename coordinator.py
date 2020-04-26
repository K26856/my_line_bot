from models.cooking.nhkrecipe import recipe
from models.scenario import responder
from models.scenario import dictionary
from models.tools.hmm import HiddenMarkovModel
from random import choice, randrange

class Coordinator :
    
    def __init__(self) :
        # user_status
        # 0 : present
        # 1 : absent
        self.__bot_user_status = 0 
        self.__dictionary = dictionary.Dictionary()
        self.__markov = HiddenMarkovModel(chain=3)
        self.__responders = {
            'parrot' : responder.Parrot(self.__dictionary, self.__markov), 
            'random' : responder.RandomTalker(self.__dictionary, self.__markov),
            'pattern' : responder.PatternTalker(self.__dictionary, self.__markov),
            'template' : responder.TemplateTalker(self.__dictionary, self.__markov),
            'markov' : responder.MarkovTalker(self.__dictionary, self.__markov)
        }

    def text_message_handler(self, event) :
        recieved_message = event.message.text
        send_message = ''

        if 'わたしはどこ' in recieved_message:
            if self.__bot_user_status == 0 :
                send_message = 'ウチにいるよ？'
            else :
                send_message = '外出してるよ？'
        elif '何が食べたい？' in recieved_message:
            recipe_site = recipe.NHKRecipe()
            send_message = 'これが食べたいな。\r\n' + recipe_site.get_random_recipe()
        else:
            chance = randrange(0, 100)
            if chance in range(0, 34) : 
                send_message += self.__responders['pattern'].response({
                    'message' : recieved_message
                })
            elif chance in range(35, 59) :
                send_message += self.__responders['template'].response({
                    'message' : recieved_message
                })
            elif chance in range(60, 84) :
                send_message += self.__responders['markov'].response({
                    'message' : recieved_message
                })
            elif chance in range(85, 94) :
                send_message += self.__responders['random'].response({
                    'message' : recieved_message
                })
            else :
                send_message += self.__responders['parrot'].response({
                    'message' : recieved_message
                })

        # study message
        self.__dictionary.study(recieved_message)
        
        return send_message
