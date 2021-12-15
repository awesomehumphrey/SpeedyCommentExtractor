import os
import csv
import re
import json
import tempfile
import chardet
from typing import TypeVar, Generic, List, NewType

T = TypeVar("T")

class keywordFilter():
    allLines = []
    dictLocation = "./keyword-dictionaries/keywords-maxed-out.JSON"
    dictionary = ""

    def __init__(self, csvfile: str) -> None:
        self.file = csvfile
        self.openFile()
        self.getKeywords()
        words = (self.getAntonyms("choosing own goals"))
        print(self.checkWordsInLine(words, "You are cool"))
        print(self.checkWordsInLine(words, "You should not eat"))

    def checkWordsInLine(self, words: str, line: str) -> bool:
        filter = ""
        for word in words:
            filter += word + "|"

        filteredWords = re.findall(filter, line, flags=re.IGNORECASE)

        res = []
        for string in filteredWords:
            if string != "":
                res.append(string)

        return len(res) > 0


    def lineToWords(self, sentence: str) -> List[T]:
        words = re.findall('([a-z]+)', sentence, flags=re.IGNORECASE)
        return words

    def getSynonyms(self, value: str) -> str:
        return self.dictionary[value]["synonyms"]

    def getAntonyms(self, value: str) -> str:
        return self.dictionary[value]["antonyms"]

    def getKeywords(self) -> List[T]:
        with open(self.dictLocation, encoding="utf-8") as dictionaryFile:
            self.dictionary = json.load(dictionaryFile)


    def openFile(self) -> None:
        with open(self.file, encoding="utf-8") as file:
            lines = file.readlines()
            for line in lines:
                self.allLines.append(line.strip("\n"))

a = keywordFilter("file.csv")
a.openFile()
