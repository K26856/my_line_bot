import sqlite3
from janome.tokenizer import Tokenizer

class HiddenMarkovModel :

    WAKATI_TOKENIZER = Tokenizer(wakati=True)
    DB_NAME = "./db/linebot.sqlite3"
    START_WORD = "%START%"
    END_WORD = "%END%"

    def __init__(self) :
        self.__con = sqlite3.connect(HiddenMarkovModel.DB_NAME)
        self.__con.execute("pragma foreign_keys='ON'")
        self.__sword_id, _ = self.__select_words(HiddenMarkovModel.START_WORD)
        self.__eword_id, _ = self.__select_words(HiddenMarkovModel.END_WORD)

    def study_from_line(self, line) : 
        wakati_text = HiddenMarkovModel.WAKATI_TOKENIZER.tokenize(line.strip())

        wakati_text_id = []
        for word in wakati_text :
            word_id = self.__insert_words(word)
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
    
    def __select_words(self, word) :
        try : 
            results = self.__con.execute("select id, word from words where word=?", (word,)).fetchone()
            return results if results else (None, None)
        except sqlite3.Error as e :
            print(e)
            return (None, None)

    def __insert_words(self, word) :
        word_id, _ = self.__select_words(word)
        if word_id :
            return word_id
        try :
            self.__con.execute("insert into words(word) values (?)", (word,))
            self.__con.commit()
            word_id, _ = self.__select_words(word)
            return word_id
        except sqlite3.Error as e :
            print(e)
            return None

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
