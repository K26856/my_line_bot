from models.cooking.nhkrecipe import recipe
from models.scenario import responder
from models.scenario import dictionary
from random import choice, randrange

class Coordinator :
    
    def __init__(self) :
        # user_status
        # 0 : present
        # 1 : absent
        self.__bot_user_status = 0 
        self.__dictionary = dictionary.Dictionary()
        self.__responders = {
            'parrot' : responder.Parrot(self.__dictionary), 
            'random' : responder.RandomTalker(self.__dictionary),
            'pattern' : responder.PatternTalker(self.__dictionary)
        }

    def text_message_handler(self, event) :
        recieved_message = event.message.text
        send_message = ''

        if 'わたしはどこ' in recieved_message:
            if self.__bot_user_status == 0 :
                send_message = 'ウチにいるよ？\r\n'
            else :
                send_message = '外出してるよ？\r\n'
        elif '何が食べたい？' in recieved_message:
            recipe_site = recipe.NHKRecipe()
            send_message = 'これが食べたいな。\r\n' + recipe_site.get_random_recipe()
        else:
            chance = randrange(0, 100)
            if chance in range(0, 59) : 
                send_message += self.__responders['pattern'].response({
                    'message' : recieved_message
                }) + '\r\n'
            elif chance in range(60, 89) :
                send_message += self.__responders['random'].response({
                    'message' : recieved_message
                }) + '\r\n'
            else :
                send_message += self.__responders['parrot'].response({
                    'message' : recieved_message
                }) + '\r\n'
        return send_message
