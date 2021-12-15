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


    def get_keywords(self) -> List[T]:
        with open(self.dictLocation, encoding="utf-8") as dictionaryFile:
            self.dictionary = json.load(dictionaryFile)


    def open_file(self) -> None:
        with open(self.file, encoding="utf-8") as file:
            lines = file.readlines()
            for line in lines:
                self.allLines.append(line.strip("\n"))

print(keyword_filter.check_words_in_line(['poo'], "poo poo"))
