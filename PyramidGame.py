import sys
import logging
from copy import deepcopy
import re
import random

Version = '0.1.0'
MinAcceptableProbability = 96


class Point(object):
    def __init__(self, Y, X):
        self.__Y = Y
        self.__X = X

    def getX(self):
        return self.__X

    def getY(self):
        return self.__Y

    def show(self):
        print(self.toString())

    def toString(self):
        result = str(PointList.index(self))
        if len(result) == 1:
            result = '0' + result
        return result

    def __eq__(self, other):
        return self.__Y == other.getY() and self.__X == other.getX()

    def __lt__(self, other):
        if self.__Y < other.getY():
            return True
        if self.__X < other.getX():
            return True
        return False


class Line(object):
    def __init__(self, PointList):
        self.__Line = PointList
        self.__Line = sorted(self.__Line)

    def getLine(self):
        return self.__Line

    def show(self):
        print(self.toString())

    def toString(self):
        result = 'Line: '
        for P in self.__Line:
            result += P.toString() + ' '
        return result

    def __eq__(self, other):
        if other is None:
            return False
        if len(self.__Line) != len(other.getLine()):
            return False
        for i in range(len(self.__Line)):
            if self.__Line[i] != other.getLine()[i]:
                return False
        return True

    def __lt__(self, other):
        if len(self.__Line) < len(other.getLine()):
            return True
        return False


class Pyramid(object):

    __PlayerMode_Me = 1
    __PlayerMode_Other = 2
    __PlayerMode_Mask = 3

    def __init__(self):

        self.__ComputerLose = False

        self.__Pyramid = [
            [False],
            [False, False],
            [False, False, False],
            [False, False, False, False],
            [False, False, False, False, False],
        ]

        self.__LegalMove = []

        LegalMoveTemp = []

        # length: 1
        for i in range(5):
            for ii in range(i + 1):
                P = Point(i, ii)
                L = Line([P])
                LegalMoveTemp.append(L)
        # length: 2
        for Y in range(5):
            for X in range(Y + 1):

                StartP = Point(Y, X)
                P = Point(Y, X + 1)
                L = Line([P])
                if L in LegalMoveTemp:
                    NewLine = Line([StartP, P])
                    LegalMoveTemp.append(NewLine)

                P = Point(Y + 1, X)
                L = Line([P])
                if L in LegalMoveTemp:
                    NewLine = Line([StartP, P])
                    LegalMoveTemp.append(NewLine)

                P = Point(Y + 1, X + 1)
                L = Line([P])
                if L in LegalMoveTemp:
                    NewLine = Line([StartP, P])
                    LegalMoveTemp.append(NewLine)

        for lineObj in LegalMoveTemp:
            line = lineObj.getLine()
            if len(line) != 2:
                continue
            # lineObj.show()

            P0 = line[0]
            P1 = line[1]

            if P0.getY() == P1.getY() and P0.getX() + 1 == P1.getX():
                P2 = Point(P1.getY(), P1.getX() + 1)
                L = Line([P2])
                if L in LegalMoveTemp:
                    NewLine = Line([P0, P1, P2])
                    LegalMoveTemp.append(NewLine)
            if P0.getY() + 1 == P1.getY() and P0.getX() == P1.getX():
                P2 = Point(P1.getY() + 1, P1.getX())
                L = Line([P2])
                if L in LegalMoveTemp:
                    NewLine = Line([P0, P1, P2])
                    LegalMoveTemp.append(NewLine)
            if P0.getY() + 1 == P1.getY() and P0.getX() + 1 == P1.getX():
                P2 = Point(P1.getY() + 1, P1.getX() + 1)
                L = Line([P2])
                if L in LegalMoveTemp:
                    NewLine = Line([P0, P1, P2])
                    LegalMoveTemp.append(NewLine)

        # for LineTemp in LegalMoveTemp:
        #     LineTemp.show()
        LegalMoveTemp = sorted(LegalMoveTemp, reverse=True)

        self.__LegalMove = LegalMoveTemp

    def show(self):

        N = 0

        for i in range(5):
            for ii in range(5 - i):
                print(' ', end='')

            for ii in self.__Pyramid[i]:
                if not ii:
                    print('O ', end='')
                else:
                    print('X ', end='')

            for ii in range(5 - i):
                print(' ', end='')
            for ii in range(5 - i):
                print('  ', end='')
            for ii in self.__Pyramid[i]:
                if not ii:
                    Number = str(N)
                    if len(Number) == 1:
                        Number = '0' + Number
                    print(Number + '  ', end='')
                else:
                    print('XX  ', end='')
                N += 1
            print('')

    def setLine(self, Line):
        if Line not in self.__LegalMove:
            print('[Error] Not in Legal move')
            return

        RemoveList = []

        for P in Line.getLine():
            # P.show()
            self.__Pyramid[P.getY()][P.getX()] = True

            for LineObj in self.__LegalMove:
                # LineObj.show()
                LegalLine = LineObj.getLine()
                if P in LegalLine and LineObj not in RemoveList:
                    # LegalMove.remove(LineObj)
                    RemoveList.append(LineObj)
                    # print('Remove!!!!')

        for RemoveLine in RemoveList:
            # RemoveLine.show()
            self.__LegalMove.remove(RemoveLine)

    def __nextMoveRecursive(self, Mode, Level=-1, PlayerFirst=False):

        global WinCount
        global LoseCount

        # True 我方獲勝
        if (len(self.__LegalMove) == 1 and len(self.__LegalMove[0].getLine()) == 1):
            # 只剩下最後一格的情況
            if Mode == self.__PlayerMode_Me:
                # 如果是我方，則輸 False
                return False
            else:
                # 如果是對方，則贏 True
                return True
        elif len(self.__LegalMove) == 0:
            # 已經沒有圈圈可以畫了，表示上一輪就結束了
            if Mode == self.__PlayerMode_Me:
                # 如果是我方，則贏 True
                return True
            else:
                # 如果是對方，則輸 False
                return False

        for PossibleLine in self.__LegalMove:

            PyramidTemp = deepcopy(self)
            PyramidTemp.setLine(PossibleLine)

            result = PyramidTemp.__nextMoveRecursive(
                self.__PlayerMode_Mask - Mode, Level=(Level + 1))

            if Level == 0:
                # 遞迴第一層紀錄一下可以獲勝的事件
                if result:
                    WinCount += 1
                else:
                    LoseCount += 1

            if Mode == self.__PlayerMode_Me and result:
                # 如果是換我方下 目標是找到 True (我方獲勝)
                return True
            elif Mode == self.__PlayerMode_Other and not result:
                # 如果是換對方下 目標是找到 False (我方失敗)
                return False

        if Mode == self.__PlayerMode_Me:
            # 如果我方都找不到獲勝的下一步，則回傳 False
            return False
        elif Mode == self.__PlayerMode_Other:
            # 如果對方都找不到讓我方失敗的下一步，則回傳 True (我方獲勝)
            return True

    def isFinish(self):
        Condition0 = len(self.__LegalMove) == 1 and len(
            self.__LegalMove[0].getLine()) == 1
        Condition1 = len(self.__LegalMove) == 0
        Condition2 = self.__ComputerLose
        return Condition0 or Condition1 or Condition2

    def nextMove(self, LastLine=None, PlayerFirst=False):

        global WinCount
        global LoseCount
        global PointList

        if LastLine is not None:
            self.setLine(LastLine)
            self.show()

        if len(self.__LegalMove) == 1:
            return None

        if len(self.__LegalMove) == 63:
            # 先手的話就下必勝路徑的第一手
            # 九種開場隨便挑，都 100 %
            FirstLineList = []
            FirstLineList.append(Line([PointList[0]]))
            FirstLineList.append(Line([PointList[10]]))
            FirstLineList.append(Line([PointList[14]]))
            FirstLineList.append(Line([PointList[3]]))
            FirstLineList.append(Line([PointList[4]]))
            FirstLineList.append(Line([PointList[5]]))
            FirstLineList.append(Line([PointList[7]]))
            FirstLineList.append(Line([PointList[8]]))
            FirstLineList.append(Line([PointList[12]]))

            FirstLineIndex = random.randint(0, len(FirstLineList))

            LineTemp = FirstLineList[FirstLineIndex]
            # 就是這麼霸氣，直接給出勝率 100 % 的答案
            print(LineTemp.toString() + '獲勝機率為 100 %')
            self.setLine(LineTemp)
            return LineTemp

        if PlayerFirst:

            MaxRate = 0
            MaxRateMove = None

        print('開始分析獲勝機率')
        for PossibleLine in self.__LegalMove:

            WinCount = 0
            LoseCount = 0

            PyramidTemp = deepcopy(self)

            PyramidTemp.setLine(PossibleLine)
            print(PossibleLine.toString(), end='')

            RecursiveResult = PyramidTemp.__nextMoveRecursive(
                self.__PlayerMode_Other, Level=0, PlayerFirst=PlayerFirst)
            if (WinCount + LoseCount) == 0:
                # 表示這一層的嘗試就分出勝負了
                if RecursiveResult:
                    Rate = 1
                else:
                    Rate = 0
            else:
                Rate = WinCount / (WinCount + LoseCount)

            if PlayerFirst:
                # 只有玩家先行才有可能，所有嘗試都沒有 100 % 勝率，
                # 才需要紀錄最大勝率
                if Rate > MaxRate:
                    MaxRate = Rate
                    MaxRateMove = PossibleLine
                # 判斷可接受勝率，所有可能跑完其實蠻慢的 QQ
                if (Rate * 100) >= MinAcceptableProbability and not RecursiveResult:
                    print('發現可接受獲勝機率為 ' + str(int(Rate * 100)) + ' %')
                    self.setLine(PossibleLine)
                    return PossibleLine

            print('獲勝機率為 ' + str(int(Rate * 100)) + ' %')

            if RecursiveResult:
                self.setLine(PossibleLine)
                return PossibleLine
            else:
                pass

        if PlayerFirst:
            if MaxRateMove is None:
                self.__ComputerLose = True
            else:
                self.setLine(MaxRateMove)
            return MaxRateMove

        return None

    def getInputLine(self):
        while True:
            LineStr = input('請按照右邊的編號輸入你想要畫的線 1 ~ 3 個: ')
            NumberList = re.findall(r'\d+', LineStr)
            NumberList = list(map(int, NumberList))

            if len(NumberList) < 1 or 3 < len(NumberList):
                print('輸入錯誤')
                continue

            InputOK = True
            for N in NumberList:
                if N < 0 or 14 < N:
                    print('請輸入 0 ~ 14 之間的數字')
                    InputOK = False
            if not InputOK:
                continue

            List = []
            for N in NumberList:
                List.append(PointList[N])
            result = Line(List)

            if result not in self.__LegalMove:
                print('不合法的輸入')
                continue
            break

        return Line(List)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    logging.info('Welcome to PyramidGame v ' + Version)

    WinCount = 0
    LoseCount = 0
    PointList = []

    for i in range(5):
        for ii in range(i + 1):
            P = Point(i, ii)
            PointList.append(P)

    pyramid = Pyramid()
    pyramid.show()
    InputLine = None
    PlayerFirst = False
    try:
        while True:
            C = input('你要先下嗎? [Y/n] ')
            if C == '' or C.lower() == 'y':
                print('選擇先下')

                MinAcceptableProbability = 0
                while True:
                    try:
                        MinAcceptableProbability = input(
                            '請輸入電腦可接受獲勝機率 (0~100): ')
                        MinAcceptableProbability = int(
                            MinAcceptableProbability)
                        if 0 <= MinAcceptableProbability <= 100:
                            break
                        print('參數有誤，請重新輸入')
                    except Exception:
                        MinAcceptableProbability = 0

                PlayerFirst = True
                InputLine = pyramid.getInputLine()

                break
            elif C == 'n'.lower():
                print('選擇後下')
                break
            else:
                print('錯誤的輸入，請重新輸入')

        while not pyramid.isFinish():
            ComputerMove = pyramid.nextMove(
                LastLine=InputLine, PlayerFirst=PlayerFirst)
            if ComputerMove is None:
                print('電腦認輸')
                break
            pyramid.show()
            print('電腦選擇 ', end='')
            for P in ComputerMove.getLine():
                Pstr = str(PointList.index(P))
                if len(Pstr) == 1:
                    Pstr = '0' + Pstr
                print(Pstr + ' ', end='')
            print('')

            if pyramid.isFinish():
                print('電腦獲勝')
                break
            InputLine = pyramid.getInputLine()
    except KeyboardInterrupt:
        print('使用者中斷')

    print('遊戲結束')
