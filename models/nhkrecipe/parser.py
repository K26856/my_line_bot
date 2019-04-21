from html.parser import HTMLParser

class RecipeParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.__recipe_list = []

    @property
    def recipe_list(self):
        return self.__recipe_list
        
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'div' and 'class' in attrs and 'data-url' in attrs and attrs['class'] == 'recipe--category-recipe':
            self.__recipe_list.append(attrs['data-url'])


class RecipeNumParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.__num = -1
        self.__recipe_str_flag = False
        self.__num_flag = False

    @property
    def num(self):
        return self.__num

    def handle_starttag(self, tag, attrs):
        if self.__num != -1:
            return
        attrs = dict(attrs)
        if tag == "span" and 'class' in attrs and attrs['class'] == 'num':
            self.__num_flag = True
        else:
            self.__num_flag = False

    def handle_data(self, data):
        if self.__num != -1:
            return
        if 'レシピ一覧' in data: 
            self.__recipe_str_flag = True
        elif self.__recipe_str_flag==True and self.__num_flag==True :
            self.__recipe_str_flag = False
            self.__num = int(data)
        else:
            self.__recipe_str_flag = False
            
