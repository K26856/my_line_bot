import urllib.request
import time
import random
from . import parser

class NHKRecipe :
    def __init__(self) :
        self.__root_url = 'https://www.kyounoryouri.jp'

    @property
    def root_url(self) : 
        return self.__root_url
      
    def get_recipe_num(self, params):
        """
        get the number of recipes
        return
             success : correct number
             error   : -1
        """
        req = urllib.request.Request('{}?{}'.format(self.root_url+'/search/recipe', urllib.parse.urlencode(params)))
        with urllib.request.urlopen(req) as res :
            body = res.read().decode(encoding='utf-8')
            # レシピ数をパースして取得
            recipe_num_parser = parser.RecipeNumParser()
            recipe_num_parser.feed(body)
            recipe_num_parser.close()
        return int(recipe_num_parser.num)
        
    def get_recipe_list(self, params):
        """
        get recipes from page 'page'
        return 
            success : recipe list
            error   : empty list
        """
        req = urllib.request.Request('{}?{}'.format(self.root_url+'/search/recipe', urllib.parse.urlencode(params)))
        with urllib.request.urlopen(req) as res :
            body = res.read().decode(encoding='utf-8')
            # レシピをパースして取得
            recipe_parser = parser.RecipeParser()
            recipe_parser.feed(body)
            recipe_parser.close()
        return recipe_parser.recipe_list


    def get_random_recipe(self) :
        """
        get a recipe 
        return
            success : recipe url
            error : empty string
        """
        params = {
            'keyword' : ''
        }
        return self.get_random_recipe_by_params(params)

    
    def get_random_recipe_by_params(self, params) :
        """
        get a recipe using params
        params
           params = {
                'keyword' : '',    # recipe name or food
                'timeclass' : '',  # ???
                'genre[]' : '',    # 1=Japanese, 2=Western, 3=Chinese, 4=Korean, 5=ethnic, 6=etc
                'calorie_min' : 0, # 
                'calorie_max' : 0, # 
                'year' : '',       # when the recipe registered
                'month' : '',      # when the recipe registered
            }
        return
            success : recipe url
            error : empty string
        """
        # レシピ数を取得
        recipe_num = self.get_recipe_num(params)
        if recipe_num <= 0:
            return ''

        # レシピ数を20で割って切り上げしページ数を割り出す
        max_page = -(-recipe_num // 20)

        params["pg"] = random.randrange(1, max_page, 1)
        # ランダムなページのランダムなレシピを取得する
        recipe_list = self.get_recipe_list(params)
        if len(recipe_list) <= 0:
            return ''
        
        # レシピリストからランダムに選択し出力する
        return self.root_url + recipe_list[random.randrange(0, len(recipe_list)-1, 1)]
