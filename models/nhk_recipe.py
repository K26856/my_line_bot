import urllib.request
import time
import random
from html.parser import HTMLParser


class RecipeNumParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self._num = -1
        self._recipe_str_flag = False
        self._num_flag = False

    @property
    def num(self):
        return self._num

    def handle_starttag(self, tag, attrs):
        if self._num != -1:
            return
        attrs = dict(attrs)
        if tag == "span" and 'class' in attrs and attrs['class'] == 'num':
            self._num_flag = True
        else:
            self._num_flag = False

    def handle_data(self, data):
        if self._num != -1:
            return
        if 'レシピ一覧' in data: 
            self._recipe_str_flag = True
        elif self._recipe_str_flag==True and self._num_flag==True :
            self._recipe_str_flag = False
            self._num = int(data)
        else:
            self._recipe_str_flag = False
            

class RecipeParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self._recipe_list = []

    @property
    def recipe_list(self):
        return self._recipe_list
        
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'div' and 'class' in attrs and 'data-url' in attrs and attrs['class'] == 'recipe--category-recipe':
            self._recipe_list.append(attrs['data-url'])


class NHKRecipe : 
    def __init__(self) :
        self._root_url = 'https://www.kyounoryouri.jp'
        self._params = {
            'keyword' : '',
            'timeclass' : '',
            'genre[]' : '',
            'calorie_min' : 0,
            'calorie_max' : 0,
            'year' : '',
            'month' : '',
            'pg' : ''
        }
   
    def get_random_recipe(self) :
        # 一回検索しレシピ数を取得
        req = urllib.request.Request('{}?{}'.format(self._root_url+'/search/recipe', urllib.parse.urlencode(self._params)))
        with urllib.request.urlopen(req) as res :
            body = res.read().decode(encoding='utf-8')
            # レシピ数をパースして取得
            recipe_num_parser = RecipeNumParser()
            recipe_num_parser.feed(body)
            recipe_num_parser.close()
            # レシピ数を20で割って切り上げしページのmax値を割り出す
            if recipe_num_parser.num == -1:
                max_page = -1
            else:
                max_page = -(-recipe_num_parser.num // 20)

        # レシピがなければNoneを返す
        if max_page == -1:
           return None
        

        # ランダムなページのランダムなレシピを取得する
        self._params['pg'] = random.randrange(1, max_page, 1)
        req = urllib.request.Request('{}?{}'.format(self._root_url+'/search/recipe', urllib.parse.urlencode(self._params)))
        with urllib.request.urlopen(req) as res :
            body = res.read().decode(encoding='utf-8')
            # レシピをパースして取得
            recipe_parser = RecipeParser()
            recipe_parser.feed(body)
            recipe_parser.close()

        if len(recipe_parser.recipe_list) == 0:
            return None
        else:
            return self._root_url + recipe_parser.recipe_list[random.randrange(0, len(recipe_parser.recipe_list)-1, 1)]
        
