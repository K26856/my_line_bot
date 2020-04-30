import sqlite3
from models.tools.analyzer import MessageAnalyzer
from random import choice, randrange

class Dictionary :

    __DB_NAME = "./db/linebot.sqlite3"
    __CON = None

    def __init__(self) :
        if Dictionary.__CON is None :
            Dictionary.__CON = sqlite3.connect(Dictionary.__DB_NAME, check_same_thread=False)
            Dictionary.__CON.execute("pragma foreign_keys='ON'")

    def __del__(self) :
        if Dictionary.__CON is not None :
            Dictionary.__CON.close()
    
    def study(self, text) :
        self.insert_randoms(text)
        self.insert_templates(text)


    def select_random(self) :
        try :
            count = Dictionary.__CON.execute("select count(message) from randoms").fetchone()[0]
            rand = randrange(0, count)
            random_message = Dictionary.__CON.execute("select message from randoms limit ?,1", (rand,)).fetchone()
            if random_message :
                return random_message[0]
            else :
                return ""
        except sqlite3.Error as e:
            print(e)
            return ""

    def insert_randoms(self, text) :
        try :
            Dictionary.__CON.execute("insert into randoms(message) values (?)", (text,))
            Dictionary.__CON.commit()
        except sqlite3.Error as e:
            print(e)

    def select_template(self, word_num_condition) :
        try : 
            count = Dictionary.__CON.execute(
                "select count(word_num_condition) from templates where word_num_condition=?" , 
                (word_num_condition,)
                ).fetchone()[0]
            if count == 0 :
                return ""
            rand = randrange(0, count)
            template_message = Dictionary.__CON.execute(
                "select message from templates where word_num_condition=? limit ?,1",
                (word_num_condition, rand)
                ).fetchone()
            if template_message :
                return template_message[0]
            else :
                return ""
        except sqlite3.Error as e :
            print(e)
            return ""

    def insert_templates(self, text) :
        parts = MessageAnalyzer.analyze(text)
        message = ''
        count = 0
        for word, part in parts :
            if MessageAnalyzer.is_keyword(part) :
                word = '%noun%'
                count += 1
            message += word
        if count <= 0 :
            return 
        try :
            self.__CON.execute(
                "insert into templates(message, word_num_condition) values (?,?)",
                (message, count)
            )
            self.__CON.commit()
        except sqlite3.Error as e :
            print(e)
                    
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
