import re
import os
import pathlib
from collections import defaultdict
from models.tools.analyzer import MessageAnalyzer

class Dictionary :

    DICT = {
        'random' : './models/scenario/dics/random_message.dat',
        'pattern' : './models/scenario/dics/pattern_message.dat',
        'template' : './models/scenario/dics/template_message.dat'
    }

    def __init__(self) :

        Dictionary.touch_dict()

        self.__random_messages= []
        self.__pattern_messages = []
        self.__template_messages = []
        self.load_random()
        self.load_pattern()
        self.load_template()
        

    @property
    def random_messages(self) :
        return self.__random_messages

    @property
    def pattern_messages(self) : 
        return self.__pattern_messages

    @property
    def template_messages(self) : 
        return self.__template_messages



    @staticmethod
    def touch_dict() : 
        for dic in Dictionary.DICT.values() :
            if not pathlib.Path(dic).exists() :
                pathlib.Path(dic).touch()



    def study(self, text) :
        self.study_random(text)
        self.study_pattern(text, MessageAnalyzer.analyze(text))
        self.study_template(MessageAnalyzer.analyze(text))



    def load_random(self) :
        with open(Dictionary.DICT['random'], mode='r', encoding='utf-8') as f :
            self.__random_messages = [x for x in f.read().splitlines() if x]

    def study_random(self, text) : 
        if not text in self.__random_messages : 
            self.__random_messages.append(text)
            self.save_random()

    def save_random(self) :
        with open(Dictionary.DICT['random'], mode='w', encoding='utf-8') as f : 
            f.write('\n'.join(self.__random_messages))



    def load_pattern(self) : 
        with open(Dictionary.DICT['pattern'], mode='r', encoding='utf-8') as f : 
            for line in f : 
                if line :
                    pattern, phrases = line.strip().split('\t')
                    if pattern and phrases :
                        self.__pattern_messages.append({
                            'pattern' : pattern, 
                            'phrases' : phrases.split('|')
                        })

    def study_pattern(self, text, parts) :
        for word, part in parts :
            if not MessageAnalyzer.is_keyword(part) :
                continue
            duplicated = next((p for p in self.__pattern_messages if p['pattern'] == word), None)
            if duplicated and not text in duplicated['phrases'] :
                duplicated['phrases'].append(text)
            else :
                self.__pattern_messages.append({'pattern':word, 'phrases': [text]})
        self.save_pattern()

    def save_pattern(self) :
        with open(Dictionary.DICT['pattern'], mode='w', encoding='utf-8') as f :
            f.write('\n'.join([self.pattern_to_line(pattern) for pattern in self.__pattern_messages]))

    def pattern_to_line(self, pattern) : 
        return '{}\t{}'.format(pattern['pattern'], '|'.join(pattern['phrases']))



    def load_template(self) :
        with open(Dictionary.DICT['template'], mode='r', encoding='utf-8') as f :
            self.__template_messages = defaultdict(list)
            for line in f :
                if line : 
                    count, template = line.strip().split('\t')
                    if count and template :
                        count = int(count)
                        self.__template_messages[count].append(template)

    def study_template(self, parts) :
        template = ''
        count = 0
        for word, part in parts :
            if MessageAnalyzer.is_keyword(part) :
                word = '%noun%'
                count += 1
            template += word

        if count > 0 and template and not template in self.__template_messages[count] :
            self.__template_messages[count].append(template)
            
    def save_template(self) : 
        with open(Dictionary.DICT['template'], mode='w', encoding='utf-8') as f :
            for count, templates in self.__template_messages.items() :
                for template in templates :
                    f.writelines('{}\t{}'.format(count, template))