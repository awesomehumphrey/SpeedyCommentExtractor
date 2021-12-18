import os
import csv
import re
from io import StringIO
import json
import linecache
import tempfile
import chardet
import sys
import inspect
# relative imports from parent directory ######################################
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
# relative import ends ########################################################
import app
from typing import TypeVar, Generic, List, NewType

T = TypeVar("T")

class keyword_filter():
    allLines = []
    dictLocation = "./keyword-dictionaries/keywords.JSON"
    dictionary = ""

    # values = ['choosing own goals', 'freedom', 'creativity', 'independent', 'privacy', 'choice', 'curious', 'self respect', 'excitement', 'varied', 'daring', 'pleasure', 'self indulgent', 'enjoying', 'ambitious']


    def __init__(self, csvfile: str) -> None:
        self.file = csvfile
        self.open_file()
        self.get_keywords()
        self.values = self.get_keys_from_json()


    def get_keys_from_json(self) -> dict[str]:
        res = []

        for key in self.dictionary:
            res.append(key)

        return res


    def search_file(self, filename: str) -> str:
        return app.search_file(filename, "./")


    @classmethod
    def check_words_in_line(self, words: str, line: str) -> List[str]:
        filteredWords = []
        word_before = ["un", "dis", "anti", "anti-", "un-"]
        word_appendages = [ "ing", "s", "ed", "less"]
        for word in words:

            res = []

            if len( re.findall("\\bcopyright\\b", line, flags=re.IGNORECASE) ) == 0:
            # filter out copyright comments ###############################################
                filter = word

                filteredWords += re.findall("\\b" + filter + "\\b", line, flags=re.IGNORECASE)
                for appendages in word_before:
                    filteredWords += re.findall("\\b" + appendages + filter + "\\b", line, flags=re.IGNORECASE)

                for appendages in word_appendages:
                    if appendages == "ing":
                        filteredWords += re.findall("\\b" + filter[0:-1] + appendages + "\\b", line, flags=re.IGNORECASE)
                    else:
                        filteredWords += re.findall("\\b" + filter[0:-1] + appendages + "\\b", line, flags=re.IGNORECASE)

                for string in filteredWords:
                    if string != "":
                        res.append(string)

        return res

    def get_line_word_size(self, line: str) -> int:
        number_of_words = len(re.findall(r'\w+', line))
        return number_of_words


    def get_number_of_lines_in_file(self, file: str):
        with open(file, 'rb') as fp:
            c_generator = keyword_filter._count_generator(fp.raw.read)
            count = sum(buffer.count(b'\n') for buffer in c_generator)
            return count + 1

    @staticmethod
    def _count_generator(reader):
        b = reader(1024 * 1024)
        while b:
            yield b
            b = reader(1024 * 1024)

    def filter_csv_file(self, filename: str) -> None:
        new_filtered_file = self.create_csv_file()
        file_size = self.get_number_of_lines_in_file(filename)

        for i in range(1, file_size):
            first_line = linecache.getline(filename, 1)
            other_line = linecache.getline(filename, i)
            f = StringIO(first_line + other_line)
            line = csv.DictReader(f)
            line = [single_line for single_line in line][0]


            # for every line file get the language location and check against the values ##
            language = line['language']
            location = line['location']
            line = line['line']


            keywords = []
            description = ""
            has_keyword = False
            values = []
            categories = []
            for value in self.values:

                category = self.dictionary[value]['category']
                synonyms = self.get_synonyms(value)
                antonyms = self.get_antonyms(value)
                synonyms_in_line = self.check_words_in_line(synonyms, line)
                antonyms_in_line = self.check_words_in_line(antonyms, line)

                if len(synonyms_in_line) > 0 and self.get_line_word_size(line) >= 3:
                    has_keyword = True
                    description = "conforms with value"
                    keywords = keywords + synonyms_in_line
                    values.append("obeys " + value.lower())
                    categories.append(category)

                if len(antonyms_in_line) > 0 and self.get_line_word_size(line) >= 3:
                    has_keyword = True
                    if description != "":
                        description += ", value violation"
                    else:
                        description = "value violation"
                    keywords = keywords + antonyms_in_line
                    values.append("violates " + value.lower())
                    categories.append(category)

            if has_keyword:
                self.append_to_csv_file(line, values, categories, str(keywords), location, language, description, new_filtered_file)

    def get_synonyms(self, value: str) -> str:
        return self.dictionary[value]["synonyms"]


    def get_antonyms(self, value: str) -> str:
        return self.dictionary[value]["antonyms"]


    def get_all_lines(self) -> List[T]:
        return self.allLines


    def get_keywords(self) -> List[T]:
        with open(self.dictLocation, encoding="utf-8") as dictionaryFile:
            self.dictionary = json.load(dictionaryFile)


    def create_csv_file(self) -> str:
        fieldnames = ['line', 'location', 'language', 'value', 'category', "keywords", "description"]
        counter = 0
        while True:
            filename = "filtered_commentfile" + str( counter ) + ".csv"
            if len(self.search_file(filename)) == 0:
                f = open(filename, "w")
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                f.close()
                break

            counter += 1

        return filename

    def append_to_csv_file(self, lines_of_comment: str, value: str, category: str, keywords: str, location: str, language: str, description: str, filename: str) -> None:
        """
        keyword args
        lines_of_comment
        value
        category
        keywords
        location
        description
        filename
        """
        fieldnames = ['line', 'location', 'language', 'value', 'category', "keywords", "description"]
        with open(filename, "a", encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writerows([{'line': lines_of_comment, 'location': location, 'language': language, 'value': value, 'category': category, 'keywords': keywords, 'description': description}])
        file.close()


    def open_file(self) -> None:
        self.allLines = []
        with open(self.file, encoding="utf-8") as file:
            lines = file.readlines()
            for line in lines:
                self.allLines.append(line.strip("\n"))

filter = keyword_filter("./commentfile106.csv")
# # print(filter.get_keys_from_json())
filter.filter_csv_file("./commentfile107.csv")
filter.filter_csv_file("./commentfile108.csv")
filter.filter_csv_file("./commentfile109.csv")
filter.filter_csv_file("./commentfile110.csv")
filter.filter_csv_file("./commentfile114.csv")
filter.filter_csv_file("./commentfile115.csv")
filter.filter_csv_file("./commentfile116.csv")
filter.filter_csv_file("./commentfile117.csv")
