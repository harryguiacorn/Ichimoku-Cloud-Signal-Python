from cmath import isnan
import pandas as pd

# def getKijunSignalCount(__kijunDirectionList):
#     __kijunDirection = __kijunDirectionList[0]
#     __newList = []
#     for __i in range(len(__kijunDirectionList)):


def getKijunDirection(__curKijun, __preKijun):
    __data = []
    for __i in range(len(__preKijun)):
        if pd.isna(__preKijun[__i]):
            __data.append(__preKijun[__i])
        elif pd.isna(__curKijun[__i]):
            __data.append(__curKijun[__i])
        elif __curKijun[__i] > __preKijun[__i]:
            __data.append(1)
        elif __curKijun[__i] < __preKijun[__i]:
            __data.append(-1)
        else:
            __data.append(0)
    return __data


def getReturn(__curClose, __preClose):
    # print("testing--------------------------")
    # print(__curClose[100], type(__preClose))
    return __curClose / __preClose - 1


stockSymbol = "TSLA"
pd.set_option('display.max_rows', None)  # print every row for debug
pd.set_option('display.max_columns', None)  # print every row for debug
__data = pd.read_csv('data/' + stockSymbol + '_cloud.csv')
__data.index = __data.Date
__data['Returns'] = getReturn(__data['Close'], __data['Close'].shift(1))
__data['Kijun Direction'] = getKijunDirection(
    __data['kijun_sen'], __data['kijun_sen'].shift(1))
# __data['Kijun Signal Count'] = getKijunSignalCount(__data['Kijun Direction'])

__data.to_csv('data/' + stockSymbol + '_kijun.csv')
print(__data)