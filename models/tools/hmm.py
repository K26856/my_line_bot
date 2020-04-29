import sqlite3
import random
from janome.tokenizer import Tokenizer

class HiddenMarkovModel :

    WAKATI_TOKENIZER = Tokenizer(wakati=True)
    DB_NAME = "./db/markov.sqlite3"
    START_WORD = "%START%"
    END_WORD = "%END%"
    MIN_CHAIN = 2
    MAX_CHAIN = 5
    __CON = None

    def __init__(self, chain=2) :
        if HiddenMarkovModel.__CON is None :
            HiddenMarkovModel.__CON = sqlite3.connect(HiddenMarkovModel.DB_NAME, check_same_thread=False)
            HiddenMarkovModel.__CON.execute("pragma foreign_keys='ON'")
        self.__sword_id, _ = self.__select_word_by(word=HiddenMarkovModel.START_WORD)
        self.__eword_id, _ = self.__select_word_by(word=HiddenMarkovModel.END_WORD)
        self.__chain = chain
        if self.__chain < HiddenMarkovModel.MIN_CHAIN :
            self.__chain = HiddenMarkovModel.MIN_CHAIN
        if self.__chain > HiddenMarkovModel.MAX_CHAIN :
            self.__chain = HiddenMarkovModel.MAX_CHAIN

    def __del__(self) :
        if HiddenMarkovModel.__CON is not None :
            HiddenMarkovModel.__CON.close()

    def make_sentence(self, start_with="", keyword="", max_length=20) :
        sentence = []
        selected_start_word = self.__select_word_by(word=start_with)
        selected_keyword = self.__select_word_by(word=keyword)
        
        keyword_id = selected_keyword[0] if selected_keyword else None
        query_data = {}
        counter = 0
        for i in range(1, self.__chain) :
            query_data["pre_word_id" + str(i)] = self.__sword_id
        if selected_start_word :
            sentence.append(selected_start_word[1])
            query_data["pre_word_id" + str(self.__chain)] = selected_start_word[0]
            counter += 1
        
        while counter < max_length :
            chains = self.__select_chains(**query_data)
            if len(chains) == 0 :
                return ""
            if counter == 0 :
                chosen_chain = random.choice(chains)
                chosen_word = self.__select_word_by(word_id=chosen_chain[self.__chain-1])
                query_data["pre_word_id" + str(self.__chain)] = chosen_word[0]
                sentence.append(chosen_word[1])
                counter += 1
            else :
                chosen_chain = self.__choice_chain(keyword_id, chains)

            chosen_word = self.__select_word_by(word_id=chosen_chain[self.__chain])
            if chosen_word[0] == self.__eword_id :
                break
            sentence.append(chosen_word[1])
            counter += 1
            for i in range(1, self.__chain) :
                query_data["pre_word_id" + str(i)] = query_data["pre_word_id" + str(i+1)]
            query_data["pre_word_id" + str(self.__chain)] = chosen_word[0]

        return "".join(sentence)

    def __choice_chain(self, keyword_id, chains) :
        if keyword_id :
            for chain in chains :
                if keyword_id == chain[self.__chain] :
                    return chain
        return random.choice(chains)

    def study_from_wakati_list(self, wakati_id_list, restudy=False) :
        if not(restudy):
            self.__insert_sentences(" ".join(map(str,wakati_id_list)))
        wakati_id_list.append(self.__eword_id)
        data = {}
        for i in range(1, self.__chain+1) :
            data["pre_word_id" + str(i)] = self.__sword_id
        data["next_word_id"] = self.__sword_id
        counter = 1

        for word_id in wakati_id_list :
            for i in range(1, self.__chain) :
                data["pre_word_id" + str(i)] = data["pre_word_id" + str(i+1)]
            data["pre_word_id" + str(self.__chain)] = data["next_word_id"]
            data["next_word_id"] = word_id
            if counter != 1 :
                self.__insert_chains(**data)
            counter += 1

    def study_from_line(self, line) :
        wakati_words = HiddenMarkovModel.WAKATI_TOKENIZER.tokenize(line.strip())
        wakati_id_list = []
        for wakati_word in wakati_words :
            word_id = self.__insert_word(wakati_word)
            if word_id :
                wakati_id_list.append(word_id)
        self.study_from_wakati_list(wakati_id_list)

    def study_from_file(self, filename) :
        with open(filename, mode="r") as f:
            for line in f:
                if line :
                    self.study_from_line(line)

    def restudy(self) :
        try :
            check_data = HiddenMarkovModel.__CON.execute("select count(next_word_id) from chains" + str(self.__chain)).fetchone()[0]
            if check_data > 0 :
                return
            self.__init_chains()
            sentences = HiddenMarkovModel.__CON.execute("select id_sentence from sentences")
            parts = sentences.fetchmany()
            while len(parts) > 0 :
                for part in parts :
                    self.study_from_wakati_list(part[0].split(" "), restudy=True)
                parts = sentences.fetchmany()
        except sqlite3.Error as e :
            print(e)

    def forget_grammer(self) :
        try :
            HiddenMarkovModel.__CON.execute("delete from sentences")
            HiddenMarkovModel.__CON.commit()
            self.__init_chains()
        except sqlite3.Error as e :
            print(e)

    def __select_word_by(self, word_id=None, word=None) :
        query_list = []
        query_tuple = ()
        if word_id is not None :
            query_list.append("id=?")
            query_tuple += (word_id,)
        if word is not None :
            query_list.append("word=?")
            query_tuple += (word,)
        sql  = "select id, word from words"
        if len(query_list) > 0 :
            sql += " where " + " and ".join(query_list)
        try :
            return HiddenMarkovModel.__CON.execute(sql, query_tuple).fetchone()
        except sqlite3.Error as e :
            print(e)
            return None

    def __insert_word(self, word) :
        selected = self.__select_word_by(word=word)
        if selected :
            return selected[0]
        try :
            cursor = HiddenMarkovModel.__CON.cursor()
            cursor.execute("insert into words(word) values (?)", (word,))
            word_id = cursor.lastrowid
            HiddenMarkovModel.__CON.commit()
            return word_id
        except sqlite3.Error as e :
            print(e)
            return None

    def __init_chains(self) :
        for i in range(HiddenMarkovModel.MIN_CHAIN, HiddenMarkovModel.MAX_CHAIN+1) :
            sql = "delete from chains" + str(i)
            try :
                HiddenMarkovModel.__CON.execute(sql)
                HiddenMarkovModel.__CON.commit()
            except sqlite3.Error as e :
                print(e)

    def __select_chains(self, **queries) :
        query_list = []
        query_tuple = ()
        for key, value in queries.items() :
            query_list.append(key + "=?")
            query_tuple += (value,)
        sql = "select"
        for i in range(1, self.__chain+1) :
            sql += " pre_word_id" + str(i) + ", "
        sql += " next_word_id, word_count"
        sql += " from chains" + str(self.__chain)
        if len(query_list) > 0 :
            sql += " where " + " and ".join(query_list)
        sql += " order by word_count"
        try :
            return HiddenMarkovModel.__CON.execute(sql, query_tuple).fetchall()
        except sqlite3.Error as e :
            print(e)
            return []

    def __insert_chains(self, **data) :
        selected = self.__select_chains(**data)
        if len(selected) > 0 :
            query_list = []
            query_tuple = (selected[0][self.__chain+1]+1,)
            for i in range(0, self.__chain) :
                query_list.append("pre_word_id" + str(i+1) + "=?")
                query_tuple += (selected[0][i],)
            query_list.append("next_word_id=?")
            query_tuple += (selected[0][self.__chain], )
            sql = "update chains" + str(self.__chain)
            sql += " set word_count=?"
            sql += " where " + " and ".join(query_list)
            try : 
                HiddenMarkovModel.__CON.execute(sql, query_tuple)
                HiddenMarkovModel.__CON.commit()
            except sqlite3.Error as e :
                print(e)
        else :
            query_list1 = []
            query_list2 = []
            query_tuple = ()
            for key, value in data.items() :
                query_list1.append(key)
                query_list2.append("?")
                query_tuple += (value,)
            sql =  "insert into chains" + str(self.__chain)
            sql += "(" + ", ".join(query_list1) + ")"
            sql += " values(" + ", ".join(query_list2) + ")"
            try :
                HiddenMarkovModel.__CON.execute(sql, query_tuple)
                HiddenMarkovModel.__CON.commit()
            except sqlite3.Error as e :
                print(e)

    def __insert_sentences(self, sentence) :
        try : 
            HiddenMarkovModel.__CON.execute("insert into sentences(id_sentence) values (?)", (sentence,))
            HiddenMarkovModel.__CON.commit()
        except sqlite3.Error as e :
            print(e)

