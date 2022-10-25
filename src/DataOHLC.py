from abc import abstractclassmethod
import pandas as pd
from abc import ABC

class DataOHLC(ABC):

    @abstractclassmethod
    def readLocalCsvData(self, symbols, __csvPath):
        pass
