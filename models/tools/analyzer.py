import re
from janome.tokenizer import Tokenizer

class MessageAnalyzer : 

    TOKENIZER = Tokenizer()

    @staticmethod
    def analyze(text) : 
        return [(t.surface, t.part_of_speech) for t in MessageAnalyzer.TOKENIZER.tokenize(text)]

    @staticmethod
    def is_keyword(part) : 
        return bool(re.match(r'名詞,(一般|代名詞|固有名詞|サ変接続|形容動詞語幹)', part))
