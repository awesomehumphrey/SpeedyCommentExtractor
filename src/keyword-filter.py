import os
import csv
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
        print(self.getSynonyms("choosing own goals"))
        print(self.getAntonyms("choosing own goals"))

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
