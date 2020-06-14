import sqlite3

class WordNet :

    DB_NAME = "./db/wnjpn.db"
    __CON = None

    def __init__(self) :
        if WordNet.__CON is None :
            WordNet.__CON = sqlite3.connect(WordNet.DB_NAME, check_same_thread=False)

    def get_words_by_lemma(self, lemma) :
        sql =  "select w.lemma, w.pos, w.lang, w.wordid, s.synset, ss.name "
        sql += "from word w, sense s, synset ss "
        sql += "where w.wordid=s.wordid and "
        sql += "s.synset=ss.synset and "
        sql += "w.lemma=?"
        query = (lemma,)
        try :
            return WordNet.__CON.execute(sql, query).fetchall()
        except sqlite3.Error as e :
            print(e)
            return None

    def get_words_by_synset(self, synset) :
        sql =  "select w.lemma, w.pos, w.lang, w.wordid, s.synset, ss.name "
        sql += "from word w, sense s, synset ss "
        sql += "where w.wordid=s.wordid and "
        sql += "s.synset=ss.synset and "
        sql += "s.synset=?"
        query = (synset,)
        try :
            return WordNet.__CON.execute(sql, query).fetchall()
        except sqlite3.Error as e :
            print(e)
            return None

    def get_ancestors_by_synset(self, synset) :
        sql =  "select hops, synset1, synset2 "
        sql += "from ancestor "
        sql += "where synset1=? "
        sql += "order by hops"
        query = (synset,)
        try : 
            return WordNet.__CON.execute(sql, query).fetchall()
        except sqlite3.Error as e :
            print(e)
            return None

    def get_synonyms_by_lemma(self, lemma) :
        wordnet_words = self.get_words_by_lemma(lemma)
        if wordnet_words is None :
            return None
        results = []
        for _, _, _, _, synset, _ in wordnet_words :
            temp_results = self.get_words_by_synset(synset)
            results.append([x for x in temp_results if not lemma in x])
        return results

    def get_hypernyms_by_lemma(self, lemma) :
        wordnet_words = self.get_words_by_lemma(lemma)
        if wordnet_words is None :
            return None
        results = []
        counter = 0
        for _, _, _, _, synset, _ in wordnet_words :
            ancestors = self.get_ancestors_by_synset(synset)
            results.append([])
            for hops, synset1, synset2 in ancestors :
                temp_results = self.get_words_by_synset(synset2)
                results[counter].append([(hops,) + x for x in temp_results])
            counter+=1
        return results

