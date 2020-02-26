import re
from janome.tokenizer import Tokenizer

class Dictionary :

    TOKENIZER = Tokenizer()
    DICT_RANDOM = './models/scenario/dics/random_message.dat'
    DICT_PATTERN = './models/scenario/dics/pattern_message.dat'

    def __init__(self) :
        self.__random_messages= []
        self.__pattern_messages = []

        with open(Dictionary.DICT_RANDOM, mode='r', encoding='utf-8') as f :
            self.__random_messages = [x for x in f.read().splitlines() if x]

        with open(Dictionary.DICT_PATTERN, mode='r', encoding='utf-8') as f : 
            for line in f : 
                if line :
                    pattern, phrases = line.strip().split('\t')
                    if pattern and phrases :
                        self.__pattern_messages.append({
                            'pattern' : pattern, 
                            'phrases' : phrases.split('|')
                        })

    @property
    def random_messages(self) :
        return self.__random_messages

    @property
    def pattern_messages(self) : 
        return self.__pattern_messages

    def study(self, text) :
        self.study_random(text)
        self.study_pattern(text, Dictionary.analyze(text))

    def study_random(self, text) : 
        if not text in self.__random_messages : 
            self.__random_messages.append(text)
            self.save_random()

    def save_random(self) :
        with open(Dictionary.DICT_RANDOM, mode='w', encoding='utf-8') as f : 
            f.write('\n'.join(self.__random_messages))

    def study_pattern(self, text, parts) :
        for word, part in parts :
            if not self.is_keyword(part) :
                continue
            duplicated = next((p for p in self.__pattern_messages if p['pattern'] == word), None)
            if duplicated and not text in duplicated['phrases'] :
                duplicated['phrases'].append(text)
            else :
                self.__pattern_messages.append({'pattern':word, 'phrases': [text]})
        self.save_pattern()

    def save_pattern(self) :
        with open(Dictionary.DICT_PATTERN, mode='w', encoding='utf-8') as f :
            f.write('\n'.join([self.pattern_to_line(pattern) for pattern in self.__pattern_messages]))
            
    def pattern_to_line(self, pattern) : 
        return '{}\t{}'.format(pattern['pattern'], '|'.join(pattern['phrases']))

    @staticmethod
    def analyze(text) : 
        return [(t.surface, t.part_of_speech) for t in Dictionary.TOKENIZER.tokenize(text)]

    @staticmethod
    def is_keyword(part) : 
        return bool(re.match(r'名詞,(一般|代名詞|固有名詞|サ変接続|形容動詞語幹)', part))
