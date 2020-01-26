from models.cooking.nhkrecipe import recipe
from models.scenario import responder

class Coordinator :
    
    def __init__(self) :
        # user_status
        # 0 : present
        # 1 : absent
        self.__bot_user_status = 0 
        self.__responders = {
            'parrot' : responder.Parrot(), 
            'random' : responder.RandomTalker()
        }
        self.__keywords = {
            'ただいま' : '',
            'いってきます' : '',
            'わたしはどこ' : '',
            '何が食べたい' : ''
        }

    @property
    def keywords(self) : 
        return self.__keywords.keys()

    def text_message_handler(self, event) :
        recieved_message = event.message.text

        send_message = self.__responders['parrot'].response({
            'message' : recieved_message
        })
        send_message += '\r\n'
        send_message += self.__responders['random'].response({
            'message' : recieved_message
        }) 

        if 'ただいま' in recieved_message:
            send_message = 'おかえり\uDBC0\uDCB1'
            self.__bot_user_status = 0
        elif 'いってきます' in recieved_message:
            send_message = 'いってらっしゃい!気を付けてね～'
            self.__bot_user_status = 1
        elif 'わたしはどこ' in recieved_message:
            if self.__bot_user_status == 0 :
                send_message = 'ウチにいるよ？'
            else :
                send_message = '外出してるよ？'
        elif '何が食べたい？' in recieved_message:
            recipe_site = recipe.NHKRecipe()
            send_message = 'これが食べたいな。\r\n' + recipe_site.get_random_recipe()
        else:
            pass

        return send_message
