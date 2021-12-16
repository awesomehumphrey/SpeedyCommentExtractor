import os
import csv
import re
import json
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
    dictLocation = "./keyword-dictionaries/keywords-maxed-out.JSON"
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
        for word in words:
            filter = word
            # filter = word

            filteredWords += re.findall("\\b" + filter + "\\b", line, flags=re.IGNORECASE)

            res = []
            for string in filteredWords:
                if string != "":
                    res.append(string)

        return res

    def filter_csv_file(self, filename: str) -> None:
        new_filtered_file = self.create_csv_file()

        with open(filename, "r", encoding="utf-8") as file:
            csvfile = csv.DictReader(file)

            for line in csvfile:
                language = line['language']
                location = line['location']
                line = line['line']
                for value in self.values:
                    category = self.dictionary[value]['category']
                    synonyms = self.get_synonyms(value)
                    antonyms = self.get_antonyms(value)
                    synonyms_in_line = self.check_words_in_line(synonyms, line)
                    antonyms_in_line = self.check_words_in_line(antonyms, line)
                    if len(synonyms_in_line) > 0:
                        self.append_to_csv_file(line, value, category, location, str(synonyms_in_line), language, "conforms with value", new_filtered_file)
                    if len(antonyms_in_line) > 0:
                        self.append_to_csv_file(line, value, category, location, str(synonyms_in_line), language, "value violation", new_filtered_file)

            file.close()

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
        fieldnames = ['line', 'location', 'language', 'value', 'category']
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

filter = keyword_filter("./unfiltered/commentfile157.csv")
# # print(filter.get_keys_from_json())
filter.filter_csv_file("./unfiltered/commentfile157.csv")
