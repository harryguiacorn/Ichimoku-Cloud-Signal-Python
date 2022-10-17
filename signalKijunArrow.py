from cmath import isnan
import pandas as pd


class KijunSignal:
    def __init__(self, symbol):
        self.symbol = symbol

    def setupPd(self, folderPath = 'data/', csvSuffix = '_cloud.csv'):
        pd.set_option('display.max_rows', None)  # print every row for debug
        pd.set_option('display.max_columns', None)  # print every column for debug
        __data = pd.read_csv(folderPath + self.symbol + csvSuffix)
        __data.index = __data.Date
        __data['Returns'] = self.getReturn(
            __data['Close'], __data['Close'].shift(1))
        __data['Kijun Direction'] = self.getKijunDirection(
            __data['kijun_sen'], __data['kijun_sen'].shift(1))
        __data['Kijun Signal Count'] = self.getKijunSignalCount(
            __data['Kijun Direction'])
        self.setColumnsSaveCsv(__data)

    def getKijunSignalCount(self, __kijunDirectionList):
        __newList = []
        __kijunDirectionCount = None
        __curKijunDirection = None
        for __i in range(len(__kijunDirectionList)):
            if pd.isna(__kijunDirectionList[__i]):
                __kijunDirectionCount = __kijunDirectionList[__i]
            elif __curKijunDirection == None:
                __curKijunDirection = __kijunDirectionList[__i]
                __kijunDirectionCount = 1
            elif not __kijunDirectionList[__i] == __curKijunDirection:
                __curKijunDirection = -__curKijunDirection
                __kijunDirectionCount = 1
            else:
                __kijunDirectionCount += 1

            __newList.append(__kijunDirectionCount)
        return __newList

    def getKijunDirection(self, __curKijun, __preKijun):
        __data = []
        __curDirection = None
        for __i in range(len(__preKijun)):
            if pd.isna(__preKijun[__i]):
                __data.append(__preKijun[__i])
            elif pd.isna(__curKijun[__i]):
                __data.append(__curKijun[__i])
            elif __curKijun[__i] > __preKijun[__i]:
                __curDirection = 1
                __data.append(1)
            elif __curKijun[__i] < __preKijun[__i]:
                __curDirection = -1
                __data.append(-1)
            else:
                __data.append(__curDirection)
        return __data

    def getReturn(self, __curClose, __preClose):
        return __curClose / __preClose - 1

    def setColumnsSaveCsv(self, __data, folderPath = 'data/' , csvSuffix = '_kijun.csv'):
        header = ["Date", "Kijun Direction", "Kijun Signal Count"]
        __data.to_csv(folderPath + self.symbol + csvSuffix,
                      columns=header, index=False)


stock = KijunSignal("AAPL")
stock.setupPd()
# stock = KijunSignal("MSFT")
# stock.setupPd()
