class Dictionary :

    DICT_RANDOM = 'dics/random_message.dat'
    DICT_PATTERN = 'dics/pattern_message.dat'

    def __init__(self) :
        self.__random_messages= []
        self.__pattern_messages = {}

        with open(Dictionary.DICT_RANDOM, mode='r', encoding='utf-8') as f :
            self.__random_messages = [x for x in f.read().splitlines if x]

        with open(Dictionary.DICT_PATTERN, mode='r', encoding='utf-8') as f : 
            for line in f : 
                pattern, phrase = line.strip().split('\t')
                if pattern and phrase :
                    self.__pattern_messages[pattern] = phrase

    @property
    def random_messages(self) :
        return self.__random_messages

    @property
    def pattern_messages(self) : 
        return self.__pattern_messages