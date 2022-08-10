from cmath import isnan
import pandas as pd


def getKijunSignalCount(__kijunDirectionList):
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


def getKijunDirection(__curKijun, __preKijun):
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
    # print(type(__data[60]))
    return __data


def getReturn(__curClose, __preClose):
    return __curClose / __preClose - 1


def setColumnsSaveCsv(__data):
    header = ["Date", "Kijun Direction", "Kijun Signal Count"]
    # print(__data['Kijun Direction'])
    __data.to_csv('data/' + stockSymbol + '_kijun.csv',
                  columns=header, index=False)
    # print(type(__data))


stockSymbol = "AAPL"
pd.set_option('display.max_rows', None)  # print every row for debug
pd.set_option('display.max_columns', None)  # print every row for debug
__data = pd.read_csv('data/' + stockSymbol + '_cloud.csv')
__data.index = __data.Date
__data['Returns'] = getReturn(__data['Close'], __data['Close'].shift(1))
__data['Kijun Direction'] = getKijunDirection(
    __data['kijun_sen'], __data['kijun_sen'].shift(1))
__data['Kijun Signal Count'] = getKijunSignalCount(__data['Kijun Direction'])

# print(__data['Kijun Direction'])
setColumnsSaveCsv(__data)

# print(__data)
