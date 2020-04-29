import re
import os
import pathlib
import sqlite3
from collections import defaultdict
from models.tools.analyzer import MessageAnalyzer

class Dictionary :

    DICT = {
        'random' : './models/scenario/dics/random_message.dat',
        'template' : './models/scenario/dics/template_message.dat'
    }

    __DB_NAME = "./db/linebot.sqlite3"
    __CON = None

    def __init__(self) :
        if Dictionary.__CON is None :
            Dictionary.__CON = sqlite3.connect(Dictionary.__DB_NAME, check_same_thread=False)
            Dictionary.__CON.execute("pragma foreign_keys='ON'")
        Dictionary.touch_dict()
        self.__random_messages= []
        self.__template_messages = []
        self.load_random()
        self.load_template()

    def __del__(self) :
        if Dictionary.__CON is not None :
            Dictionary.__CON.close()
        

    @property
    def random_messages(self) :
        return self.__random_messages

    @property
    def template_messages(self) : 
        return self.__template_messages



    @staticmethod
    def touch_dict() : 
        for dic in Dictionary.DICT.values() :
            if not pathlib.Path(dic).exists() :
                pathlib.Path(dic).touch()



    def study(self, text) :
        self.study_random(text)
        self.study_template(MessageAnalyzer.analyze(text))



    def load_random(self) :
        with open(Dictionary.DICT['random'], mode='r', encoding='utf-8') as f :
            self.__random_messages = [x for x in f.read().splitlines() if x]

    def study_random(self, text) : 
        if not text in self.__random_messages : 
            self.__random_messages.append(text)
            self.save_random()

    def save_random(self) :
        with open(Dictionary.DICT['random'], mode='w', encoding='utf-8') as f : 
            f.write('\n'.join(self.__random_messages))

    def select_pattern_messages(self, user_id) :
        user_info = self.select_user_info(user_id)
        if user_info is None :
            return []
        try : 
            sql =  "select recieve, response, next_user_status, next_scenario from patterns"
            sql += " where (user_status_condition=? or user_status_condition=?)"
            sql += " and (scenario_condition=? or scenario_condition=?)"
            return Dictionary.__CON.execute(sql, ("any", user_info[0], "any", user_info[1])).fetchall()
        except sqlite3.Error as e :
            print(e)
            return []

    def select_user_info(self, user_id) :
        try :
            sql = "select user_id, status, scenario from user_info where user_id=?"
            user_info = Dictionary.__CON.execute(sql, (user_id,)).fetchone()
            if user_info :
                return user_info
            else :
                Dictionary.__CON.execute("insert into user_info(user_id) values (?)", (user_id,))
                Dictionary.__CON.commit()
                return (user_id, "0000000", "0000000")
        except sqlite3.Error as e :
            print(e)
            return None

    def update_user_info(self, user_id, user_status, scenario) :
        query_list = []
        query_tuple = ()
        if user_status!="keep" and user_status!="any" :
            query_list.append("status=?")
            query_tuple += (user_status,)
        if scenario!="keep" and scenario!="any" :
            query_list.append("scenario=?")
            query_tuple += (scenario,)
        if len(query_list) == 0 :
            return
        try :
            sql = "update user_info set " + ", ".join(query_list) + " where user_id=?"
            query_tuple += (user_id,)
            Dictionary.__CON.execute(sql, query_tuple)
            Dictionary.__CON.commit()
        except sqlite3.Error as e :
            print(e)

    def load_template(self) :
        with open(Dictionary.DICT['template'], mode='r', encoding='utf-8') as f :
            self.__template_messages = defaultdict(list)
            for line in f :
                if line : 
                    count, template = line.strip().split('\t')
                    if count and template :
                        count = int(count)
                        self.__template_messages[count].append(template)

    def study_template(self, parts) :
        template = ''
        count = 0
        for word, part in parts :
            if MessageAnalyzer.is_keyword(part) :
                word = '%noun%'
                count += 1
            template += word
        if count > 0 and template and not template in self.__template_messages[count] :
            self.__template_messages[count].append(template)
            
    def save_template(self) : 
        with open(Dictionary.DICT['template'], mode='w', encoding='utf-8') as f :
            for count, templates in self.__template_messages.items() :
                for template in templates :
                    f.writelines('{}\t{}'.format(count, template))