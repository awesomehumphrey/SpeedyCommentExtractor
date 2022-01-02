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
sys.path.append('../csv_file_modifier/')
from modifier import csv_modifier as cm

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
        self.fieldname.append("original comment")
        self.fieldname.append("trigram")


    def tokenise(self, sentence: str) -> List[str]:
        return nltk.word_tokenize(sentence)

    def create_new_processed_file(self) -> None:
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


            line['line'] = tokens
            line['trigram'] = new_trigram

            columns = []

            for value_name in line:
                columns.append(line[ value_name ])


            self.modified_csv_file.append_to_csv_file(self.fieldname, columns, newfile)


a = preprocess('filtered_commentfile3.csv')

a.create_new_processed_file()
