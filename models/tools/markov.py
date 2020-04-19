import markovify
from janome.tokenizer import Tokenizer

class HiddenMarkovModel :

    WAKATI_TOKENIZER = Tokenizer(wakati=True)

    def __init__(self) :
        with open("./models/tools/hmm_base/kokoro.txt", mode="r") as f:
            text = HiddenMarkovModel.WAKATI_TOKENIZER.tokenize(f.read())
        self.__model = markovify.NewlineText(" ".join(text))

    def make_sentence(self) : 
        sentence = self.__model.make_sentence()
        if not sentence is None :
            sentence = sentence.replace(" ", "")
        return sentence
        