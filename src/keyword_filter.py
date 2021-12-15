import os
import csv
import re
import json
import tempfile
import chardet
from typing import TypeVar, Generic, List, NewType

T = TypeVar("T")

class keyword_filter():
    allLines = []
    dictLocation = "./keyword-dictionaries/keywords-maxed-out.JSON"
    dictionary = ""


    def __init__(self, csvfile: str) -> None:
        self.file = csvfile
        self.open_file()
        self.get_keywords()
        words = (self.get_antonyms("choosing own goals"))

    @classmethod
    def check_words_in_line(self, words: str, line: str) -> bool:
        filter = ""
        for word in words:
            filter += word + "|"

        filteredWords = re.findall(filter, line, flags=re.IGNORECASE)

        res = []
        for string in filteredWords:
            if string != "":
                res.append(string)

        return len(res) > 0


    def get_synonyms(self, value: str) -> str:
        return self.dictionary[value]["synonyms"]


    def get_antonyms(self, value: str) -> str:
        return self.dictionary[value]["antonyms"]


    def get_all_lines(self) -> List[T]:
        return self.allLines

    def get_keywords(self) -> List[T]:
        with open(self.dictLocation, encoding="utf-8") as dictionaryFile:
            self.dictionary = json.load(dictionaryFile)

    def create_csv_file(filename: str) -> None:
        fieldnames = ['line', 'location', 'language']
        f = open(filename, "w")
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        f.close()

    def append_to_csv_file(self, lines_of_comment:str, filename: str) -> None:
        fieldnames = ['line', 'location', 'language']
        with open(filename, "a", encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writerows(lines_of_comment)
        file.close()


    def open_file(self) -> None:
        self.allLines = []
        with open(self.file, encoding="utf-8") as file:
            lines = file.readlines()
            for line in lines:
                self.allLines.append(line.strip("\n"))

print(keyword_filter.check_words_in_line(['poo'], "poo poo"))
