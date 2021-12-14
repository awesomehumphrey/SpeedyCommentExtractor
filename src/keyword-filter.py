import os
import csv
import tempfile
import chardet
import json
from typing import TypeVar, Generic, List, NewType

T = TypeVar("T")

class keywordFilter():
    allLines = []
    dictLocation = "./keyword-dictionaries/keywords-maxed-out.JSON"

    def __init__(self, csvfile: str) -> None:
        self.file = csvfile
        self.openFile()
        self.getKeywords()

    def getKeywords(self) -> List[T]:
        with open(self.dictLocation, encoding="utf-8") as dictionaryFile:
            dictionary = json.load(dictionaryFile)
            print(dictionary)


    def openFile(self) -> None:
        with open(self.file, encoding="utf-8") as file:
            lines = file.readlines()
            for line in lines:
                self.allLines.append(line.strip("\n"))

a = keywordFilter("file.csv")
a.openFile()
