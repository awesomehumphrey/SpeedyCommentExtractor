import nltk
import csv
import chardet
import linecache
import inspect
import sys
import git
from typing import TypeVar, Generic, List, NewType
from nltk.tokenize import word_tokenize
from nltk import ngrams
from io import StringIO
from src.csv_file_modifier.modifier import csv_modifier as cm

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('reuters')

from nltk.corpus import stopwords as sw
from nltk.corpus import reuters
from nltk import FreqDist

T = TypeVar("T")

class preprocess():
    stopwords = sw.words('english')
    def __init__(self, csv_file: str=None) -> None:
        self.filename = csv_file
        self.modified_csv_file = cm(csv_file)
        self.fieldname = self.modified_csv_file.get_og_filenames()
        # TODO eliminate connascence of execution
        self.add_filed_to_fieldname("original comment")
        self.add_filed_to_fieldname("trigram")
        self.add_filed_to_fieldname("comment length")


    def add_filed_to_fieldname(self, new_field: str) -> None:
        self.fieldname.append(new_field)


    def tokenise(self, sentence: str) -> List[str]:
        return nltk.word_tokenize(sentence)


    def create_dist_file(self, base_file_name: str="word_frequency_dictionary") -> str:
        file_size = self.modified_csv_file.get_number_of_lines_in_file(self.filename)

        frequency_dictionary = {}
        for i in range(2, file_size):
            first_line = linecache.getline(self.filename, 1)
            other_line = linecache.getline(self.filename, i)
            f = StringIO(first_line + other_line)

            line = csv.DictReader(f)
            line = [single_line for single_line in line][0]

            freq_tri = FreqDist(self.process_comment(line))

            for keyword in freq_tri:

                if keyword in frequency_dictionary:
                    frequency_dictionary[keyword] += freq_tri[keyword]
                else:
                    frequency_dictionary.update({keyword : freq_tri[keyword]})

        if frequency_dictionary:
            newfile = self.modified_csv_file.create_csv_file(None, base_file_name, "json")

            f = open(newfile, "a", encoding="utf-8")
            f.write(str(frequency_dictionary))

            return newfile

        return None


    def process_comment(self, comment: dict) -> List[T]:
        tokens = self.tokenise(comment['line'])

        # Remove punctuation ############################################### 
        tokens = [word for word in tokens if word.isalpha()]

        # case normalisation ##########################################################
        tokens = [word.lower() for word in tokens]

        # remove stopwords #################################s #########################
        tokens = [word for word in tokens if word not in self.stopwords]

        return tokens


    def create_trigram(self, line: dict) -> List[T]:

        tokens = self.process_comment(line)

        trigram = []

        trigram.extend(list(ngrams(tokens, 3,pad_left=True, pad_right=True)))

        new_trigram = []

        for quadriplet in trigram:
            count = 0
            for word in quadriplet:
                if word is None:
                    count = 1
                else:
                    count = count or 0
            if count != 1:
                new_trigram.append(quadriplet)

        return new_trigram


    def create_new_processed_file(self) -> str:
        base_file_name = "preprocessed_comment_file"

        newfile = self.modified_csv_file.create_csv_file(self.fieldname, base_file_name)

        file_size = self.modified_csv_file.get_number_of_lines_in_file(self.filename)


        for i in range(2, file_size):
            first_line = linecache.getline(self.filename, 1)
            other_line = linecache.getline(self.filename, i)
            f = StringIO(first_line + other_line)
            line = csv.DictReader(f)
            line = [single_line for single_line in line][0]


            line['original comment'] = line['line']

            tokens = self.tokenise(line['line'])

            # Remove punctuation ############################################### 
            tokens = [word for word in tokens if word.isalpha()]

            # case normalisation ##########################################################
            tokens = [word.lower() for word in tokens]

            # remove stopwords #################################s #########################
            tokens = [word for word in tokens if word not in self.stopwords]

            trigram = self.create_trigram(line)

            line['line'] = tokens
            line['trigram'] = trigram
            line['comment length'] = len(tokens)

            row = []

            for value_name in line:
                row.append(line[ value_name ])

            if len(line['line']) >= 3:
                self.modified_csv_file.append_to_csv_file(self.fieldname, row, newfile)

        self.create_dist_file("frequency_dictionary_for_" + base_file_name)
        return base_file_name

