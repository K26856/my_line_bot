import sqlite3
from random import choice

class WordNet :

    DB_NAME = "./db/wnjpn.db"
    __CON = None

    def __init__(self, lang=None) :
        if WordNet.__CON is None :
            WordNet.__CON = sqlite3.connect(WordNet.DB_NAME, check_same_thread=False)
        self.lang = lang

    def get_words_by_lemma(self, lemma) :
        sql =  "select w.lemma, w.pos, w.lang, w.wordid, s.synset, ss.name "
        sql += "from word w, sense s, synset ss "
        sql += "where w.wordid=s.wordid and "
        sql += "s.synset=ss.synset and "
        sql += "w.lemma=?"
        query = (lemma,)
        if self.lang is not None :
            sql += " and w.lang=?"
            query += (self.lang,)
        try :
            return WordNet.__CON.execute(sql, query).fetchall()
        except sqlite3.Error as e :
            print(e)
            return []

    def get_words_by_synset(self, synset) :
        sql =  "select w.lemma, w.pos, w.lang, w.wordid, s.synset, ss.name "
        sql += "from word w, sense s, synset ss "
        sql += "where w.wordid=s.wordid and "
        sql += "s.synset=ss.synset and "
        sql += "s.synset=?"
        query = (synset,)
        if self.lang is not None :
            sql += " and w.lang=?"
            query += (self.lang,)
        try :
            return WordNet.__CON.execute(sql, query).fetchall()
        except sqlite3.Error as e :
            print(e)
            return []

    def get_synsets_by_name(self, name) :
        sql =  "select synset, name from synset where name=?"
        query = (name,)
        try :
            return WordNet.__CON.execute(sql, query).fetchall()
        except sqlite3.Error as e :
            print(e)
            return []

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
            return []

    def __get_descendants_one_hop_by_synset(self, synset) :
        sql =  "select synset1, synset2, link "
        sql += "from synlink "
        sql += "where synset1=? and "
        sql += "link='hypo'"
        query = (synset,)
        try : 
            results = WordNet.__CON.execute(sql, query).fetchall()
            return [synset2 for _, synset2, _ in results]
        except sqlite3.Error as e :
            print(e)
            return []

    def get_descendants_by_synset(self, synset) :
        results = []
        to_searches = []
        searched = []
        # init
        temp_descendants = self.__get_descendants_one_hop_by_synset(synset)
        if len(temp_descendants) > 0 :
            searched.append(synset)
            to_searches.extend(temp_descendants)
        else :
            return []
        # search
        while len(to_searches) > 0 :
            to_search = to_searches.pop(0)
            if to_search in searched :
                continue
            temp_descendants = self.__get_descendants_one_hop_by_synset(to_search)
            if len(temp_descendants) > 0 :
                if not to_search in searched :
                    searched.append(to_search)
                to_searches.extend(temp_descendants)
            else :
                if not to_search in results :
                    results.append(to_search)
        return results

    def get_descendant_randomly_by_synset(self, synset) :
        result = None
        temp_descendants = self.__get_descendants_one_hop_by_synset(synset)

        while len(temp_descendants) > 0 :
            result = choice(temp_descendants)
            temp_descendants = self.__get_descendants_one_hop_by_synset(result)
        return result

    def get_synonyms_by_lemma(self, lemma) :
        results = {}
        wordnet_words = self.get_words_by_lemma(lemma)
        if len(wordnet_words) == 0 :
            return results
        for _, _, _, _, synset, name in wordnet_words :
            temp_results = self.get_words_by_synset(synset)
            if not name in results.keys() :
                results[name] = []
            results[name].extend([x for x in temp_results if not lemma in x])
        return results

    def get_hypernyms_by_lemma(self, lemma) :
        results = {}
        wordnet_words = self.get_words_by_lemma(lemma)
        if len(wordnet_words) == 0 :
            return results
        for _, _, _, _, synset, name in wordnet_words :
            ancestors = self.get_ancestors_by_synset(synset)
            if not name in results.keys() :
                results[name] = {}
            for hops, synset1, synset2 in ancestors :
                temp_results = self.get_words_by_synset(synset2)
                if not hops in results[name].keys() :
                    results[name][hops] = []
                results[name][hops].extend(temp_results)
        return results

    def get_hyponyms_by_synset(self, synset) :
        results = []
        descendants = self.get_descendants_by_synset(synset)
        for synset in descendants :
            results.extend(self.get_words_by_synset(synset))
        return results

    def get_hyponyms_by_synset_name(self, synset_name) :
        results = []
        synsets = self.get_synsets_by_name(synset_name)
        for synset, _ in synsets :
            results.extend(self.get_hyponyms_by_synset(synset))
        return results

    def get_hyponyms_by_lemma(self, lemma) :
        results = []
        wordnet_words = self.get_words_by_lemma(lemma)
        if len(wordnet_words) == 0 :
            return results
        for _, _, _, _, synset, _ in wordnet_words :
            results.extend(self.get_hyponyms_by_synset(synset))
        return results

    def get_hyponym_randomly_by_synset(self, synset) :
        result = None
        hyponym_synset = self.get_descendant_randomly_by_synset(synset)
        choiced_words = self.get_words_by_synset(hyponym_synset)
        if len(choiced_words) == 0 :
            return result
        result = choice(choiced_words)
        return result

    def get_hyponym_randomly_by_synset_name(self, synset_name) :
        result = None
        synsets = self.get_synsets_by_name(synset_name)
        hyponyms = []
        for synset, _ in synsets :
            hyponym = self.get_hyponym_randomly_by_synset(synset)
            if hyponym is not None : 
                hyponyms.append(hyponym)
        if len(hyponyms) == 0 :
            return result
        result = choice(hyponyms)
        return result

    def get_hyponym_randomly_by_lemma(self, lemma) :
        result = None
        wordnet_words = self.get_words_by_lemma(lemma)
        hyponyms = []
        for _, _, _, _, synset, _ in wordnet_words :
            hyponym = self.get_hyponym_randomly_by_synset(synset)
            if hyponyms is not None :
                hyponyms.append(hyponym)
        if len(hyponyms) == 0 :
            return result
        result = choice(hyponyms)
        return result
