import sqlite3
import random
from janome.tokenizer import Tokenizer

class HiddenMarkovModel :

    WAKATI_TOKENIZER = Tokenizer(wakati=True)
    DB_NAME = "./db/linebot.sqlite3"
    START_WORD = "%START%"
    END_WORD = "%END%"

    def __init__(self) :
        self.__con = sqlite3.connect(HiddenMarkovModel.DB_NAME)
        self.__con.execute("pragma foreign_keys='ON'")
        self.__sword_id, _ = self.__select_word_by_word(HiddenMarkovModel.START_WORD)
        self.__eword_id, _ = self.__select_word_by_word(HiddenMarkovModel.END_WORD)

    def __del__(self) :
        self.__con.close()

    def make_sentence(self, start_with="", keyword="", max_length=20) :
        sentence = []
        sentence_ids = []
        keyword_id, _ = self.__select_word_by_word(keyword)
        pre_word_id = self.__sword_id
        pre_word2_id, _ = self.__select_word_by_word(start_with)
        next_word_id = None
        counter = 0

        if pre_word2_id :
            sentence.append(start_with)
            sentence_ids.append(pre_word_id)
            counter += 1

        while pre_word2_id != self.__eword_id and counter < max_length :
            markovs = self.__select_markovs(pre_word_id, pre_word2_id)
            if counter == 0 :
                pre_word_id, pre_word2_id, next_word_id, _ = self.__choice_markovs(keyword_id, markovs)
                _, word = self.__select_word_by_id(pre_word2_id)
                sentence.append(word)
                sentence_ids.append(pre_word2_id)
                counter += 1
            else :
                pre_word_id, pre_word2_id, next_word_id, _ = self.__random_markovs(keyword_id, markovs, sentence_ids)
            _, word = self.__select_word_by_id(next_word_id)
            sentence.append(word)
            sentence_ids.append(next_word_id)
            counter += 1
            pre_word_id = pre_word2_id
            pre_word2_id = next_word_id
        sentence.pop(-1)
        return "".join(sentence)

    def __random_markovs(self, keyword_id, markovs, sentence_ids) :
        rand_num = random.randrange(start=0, stop=1050, step=1)/1000
        if keyword_id :
            for markov in markovs :
                if keyword_id in markov :
                    return markov
        for markov in markovs :
            if markov[3]-rand_num <= 0.0 and not(markov[2] in sentence_ids):
                return markov
        return markovs[0]

    def __choice_markovs(self, keyword_id, markovs) :
        if keyword_id :
            for markov in markovs :
                if keyword_id in markov :
                    return markov
        return random.choice(markovs)

    def study_from_line(self, line) : 
        wakati_text = HiddenMarkovModel.WAKATI_TOKENIZER.tokenize(line.strip())

        wakati_text_id = []
        for word in wakati_text :
            word_id = self.__insert_word(word)
            wakati_text_id.append(word_id)
        wakati_text_id.append(self.__eword_id)

        pre_word_id = self.__sword_id
        pre_word2_id = self.__sword_id
        next_word_id = self.__sword_id
        counter = 1
        for word_id in wakati_text_id :
            pre_word_id = pre_word2_id
            pre_word2_id = next_word_id
            next_word_id = word_id
            if counter != 1 :
                self.__insert_markov(pre_word_id, pre_word2_id, next_word_id)
            counter += 1

    def study_from_file(self, filename) :
        with open(filename, mode="r") as f:
            for line in f:
                if line :
                    self.study_from_line(line)

    def __select_word_by_id(self, word_id) :
        try : 
            results = self.__con.execute("select id, word from words where id=?", (word_id,)).fetchone()
            return results if results else (None, None)
        except sqlite3.Error as e :
            print(e)
            return (None, None)

    def __select_word_by_word(self, word) :
        try : 
            results = self.__con.execute("select id, word from words where word=?", (word,)).fetchone()
            return results if results else (None, None)
        except sqlite3.Error as e :
            print(e)
            return (None, None)

    def __insert_word(self, word) :
        word_id, _ = self.__select_word_by_word(word)
        if word_id :
            return word_id
        try :
            self.__con.execute("insert into words(word) values (?)", (word,))
            self.__con.commit()
            word_id, _ = self.__select_word_by_word(word)
            return word_id
        except sqlite3.Error as e :
            print(e)

    def __select_markovs(self, pre_word_id=None, pre_word2_id=None) :
        pre_word_id = pre_word_id if pre_word_id else self.__sword_id
        if pre_word2_id :
            try : 
                query = "select a.pre_word, a.pre_word2, a.next_word, cast(a.word_count as real)/b.sum as ratio "
                query += "from markov as a, "
                query += "  (select pre_word, pre_word2, sum(word_count) as sum from markov "
                query += "   where pre_word=? and pre_word2=? group by pre_word, pre_word2) as b "
                query += "where a.pre_word=? and a.pre_word2=? and a.pre_word=b.pre_word and a.pre_word2=b.pre_word2 "
                query += "order by ratio desc"
                results = self.__con.execute(query, (pre_word_id, pre_word2_id, pre_word_id, pre_word2_id)).fetchall()
                return results if results else []
            except sqlite3.Error as e :
                print(e)
                return []
        else :
            try : 
                query = "select a.pre_word, a.pre_word2, a.next_word, cast(a.word_count as real)/b.sum as ratio "
                query += "from markov as a, "
                query += "  (select pre_word, pre_word2, sum(word_count) as sum from markov "
                query += "   where pre_word=? group by pre_word, pre_word2) as b "
                query += "where a.pre_word=? and a.pre_word=b.pre_word and a.pre_word2=b.pre_word2 "
                query += "order by ratio desc"
                results = self.__con.execute(query, (pre_word_id, pre_word_id)).fetchall()
                return results if results else []
            except sqlite3.Error as e :
                print(e)
                return []

    def __select_markov(self, pre_word_id, pre_word2_id, next_word_id) :
        try :
            results = self.__con.execute(
                "select pre_word, pre_word2, next_word, word_count " + 
                "from markov " +
                "where pre_word=? and pre_word2=? and next_word=?", 
                (pre_word_id, pre_word2_id, next_word_id)
            ).fetchone()
            return results if results else (None, None, None, None)
        except sqlite3.Error as e :
            print(e)
            return (None, None, None, None)

    def __insert_markov(self, pre_word_id, pre_word2_id, next_word_id) :
        _, _, _, word_count = self.__select_markov(pre_word_id, pre_word2_id, next_word_id)
        if word_count :
            try :
                self.__con.execute(
                    "update markov "+
                    "set word_count=? " +
                    "where pre_word=? and pre_word2=? and next_word=?",
                    (word_count+1, pre_word_id, pre_word2_id, next_word_id)
                )
                self.__con.commit()
            except sqlite3.Error as e :
                print(e)
                print("{}, {}, {}, {}".format(pre_word_id, pre_word2_id, next_word_id, word_count+1))
        else : 
            try :
                self.__con.execute(
                    "insert into markov(pre_word, pre_word2, next_word) values (?, ?, ?)", 
                    (pre_word_id, pre_word2_id, next_word_id)
                )
                self.__con.commit()
            except sqlite3.Error as e :
                print(e)
                print("{}, {}, {}".format(pre_word_id, pre_word2_id, next_word_id))
