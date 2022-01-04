import random
import re
from copy import deepcopy

from SingleLog.log import Logger

Version = '0.2.0'
MinAcceptableProbability = 96


class Point(object):
    def __init__(self, y, x):
        self.y = y
        self.x = x

    def show(self):
        print(self.toString())

    def toString(self):
        result = str(PointList.index(self))
        if len(result) == 1:
            result = '0' + result
        return result

    def __eq__(self, other):
        return self.y == other.y and self.x == other.x

    def __lt__(self, other):
        if self.y < other.y:
            return True
        if self.x < other.x:
            return True
        return False


class Line(object):
    def __init__(self, point_list):
        self.line = sorted(point_list)

    def show(self):
        print(self.toString())

    def toString(self):
        result = 'Line: '
        for p in self.line:
            result += p.toString() + ' '
        return result

    def __eq__(self, other):
        if other is None:
            return False
        if len(self.line) != len(other.line):
            return False
        for i in range(len(self.line)):
            if self.line[i] != other.line[i]:
                return False
        return True

    def __lt__(self, other):
        if len(self.line) < len(other.line):
            return True
        return False


class Pyramid(object):
    player_mode_me = 1
    player_mode_other = 2
    player_mode_mask = 3

    def __init__(self):

        self.computer_lose = False

        self.map = [
            [False],
            [False, False],
            [False, False, False],
            [False, False, False, False],
            [False, False, False, False, False],
        ]

        self.legal_move = []

        legal_move_temp = []

        # length: 1
        for i in range(5):
            for ii in range(i + 1):
                p = Point(i, ii)
                l = Line([p])
                legal_move_temp.append(l)
        # length: 2
        for y in range(5):
            for x in range(y + 1):

                start_p = Point(y, x)
                p = Point(y, x + 1)
                l = Line([p])
                if l in legal_move_temp:
                    new_line = Line([start_p, p])
                    legal_move_temp.append(new_line)

                p = Point(y + 1, x)
                l = Line([p])
                if l in legal_move_temp:
                    new_line = Line([start_p, p])
                    legal_move_temp.append(new_line)

                p = Point(y + 1, x + 1)
                l = Line([p])
                if l in legal_move_temp:
                    new_line = Line([start_p, p])
                    legal_move_temp.append(new_line)

        for line_obj in legal_move_temp:
            line = line_obj.line
            if len(line) != 2:
                continue
            # line_obj.show()

            p0 = line[0]
            p1 = line[1]

            if p0.y == p1.y and p0.x + 1 == p1.x:
                p2 = Point(p1.y, p1.x + 1)
                l = Line([p2])
                if l in legal_move_temp:
                    new_line = Line([p0, p1, p2])
                    legal_move_temp.append(new_line)
            if p0.y + 1 == p1.y and p0.x == p1.x:
                p2 = Point(p1.y + 1, p1.x)
                l = Line([p2])
                if l in legal_move_temp:
                    new_line = Line([p0, p1, p2])
                    legal_move_temp.append(new_line)
            if p0.y + 1 == p1.y and p0.x + 1 == p1.x:
                p2 = Point(p1.y + 1, p1.x + 1)
                l = Line([p2])
                if l in legal_move_temp:
                    new_line = Line([p0, p1, p2])
                    legal_move_temp.append(new_line)

        # for LineTemp in legal_move_temp:
        #     LineTemp.show()
        legal_move_temp = sorted(legal_move_temp, reverse=True)

        self.legal_move = legal_move_temp

    def show(self):

        N = 0

        for i in range(5):
            for ii in range(5 - i):
                print(' ', end='')

            for ii in self.map[i]:
                if not ii:
                    print('O ', end='')
                else:
                    print('X ', end='')

            for ii in range(5 - i):
                print(' ', end='')
            for ii in range(5 - i):
                print('  ', end='')
            for ii in self.map[i]:
                if not ii:
                    Number = str(N)
                    if len(Number) == 1:
                        Number = '0' + Number
                    print(Number + '  ', end='')
                else:
                    print('XX  ', end='')
                N += 1
            print('')

    def setLine(self, line):
        if line not in self.legal_move:
            print('[Error] Not in Legal move')
            return

        remove_list = []

        for p in line.line:
            # p.show()
            self.map[p.y][p.x] = True

            for line_obj in self.legal_move:
                # line_obj.show()
                legal_line = line_obj.line
                if p in legal_line and line_obj not in remove_list:
                    # LegalMove.remove(line_obj)
                    remove_list.append(line_obj)
                    # print('Remove!!!!')

        for remove_line in remove_list:
            # remove_line.show()
            self.legal_move.remove(remove_line)

    def next_move_recursive(self, mode, level=-1):

        global win_count
        global lose_count

        # True 我方獲勝
        if len(self.legal_move) == 1 and len(self.legal_move[0].line) == 1:
            # 只剩下最後一格的情況
            if mode == self.player_mode_me:
                # 如果是我方，則輸 False
                return False
            else:
                # 如果是對方，則贏 True
                return True
        elif len(self.legal_move) == 0:
            # 已經沒有圈圈可以畫了，表示上一輪就結束了
            if mode == self.player_mode_me:
                # 如果是我方，則贏 True
                return True
            else:
                # 如果是對方，則輸 False
                return False

        for possible_line in self.legal_move:

            map_temp = deepcopy(self)
            map_temp.setLine(possible_line)

            result = map_temp.next_move_recursive(
                self.player_mode_mask - mode, level=(level + 1))

            if level == 0:
                # 遞迴第一層紀錄一下可以獲勝的事件
                if result:
                    win_count += 1
                else:
                    lose_count += 1

            if mode == self.player_mode_me and result:
                # 如果是換我方下 目標是找到 True (我方獲勝)
                return True
            elif mode == self.player_mode_other and not result:
                # 如果是換對方下 目標是找到 False (我方失敗)
                return False

        if mode == self.player_mode_me:
            # 如果我方都找不到獲勝的下一步，則回傳 False
            return False
        elif mode == self.player_mode_other:
            # 如果對方都找不到讓我方失敗的下一步，則回傳 True (我方獲勝)
            return True

    def is_finish(self):
        condition0 = len(self.legal_move) == 1 and len(
            self.legal_move[0].line) == 1
        condition1 = len(self.legal_move) == 0
        condition2 = self.computer_lose
        return condition0 or condition1 or condition2

    def next_move(self, last_line=None, player_first=False):

        global win_count
        global lose_count
        global PointList

        if last_line is not None:
            self.setLine(last_line)
            self.show()

        if len(self.legal_move) == 1:
            return None

        if len(self.legal_move) == 63:
            # 先手的話就下必勝路徑的第一手
            # 九種開場隨便挑，都 100 %
            first_line_list = [
                Line([PointList[0]]),
                Line([PointList[10]]),
                Line([PointList[14]]),
                Line([PointList[3]]),
                Line([PointList[4]]),
                Line([PointList[5]]),
                Line([PointList[7]]),
                Line([PointList[8]]),
                Line([PointList[12]])]

            first_line_index = random.randint(0, len(first_line_list))

            line_temp = first_line_list[first_line_index]
            # 就是這麼霸氣，直接給出勝率 100 % 的答案
            print(line_temp.toString() + '獲勝機率為 100 %')
            self.setLine(line_temp)
            return line_temp

        if player_first:
            max_rate = 0
            max_rate_move = None

        logger.info('開始分析獲勝機率')
        for PossibleLine in self.legal_move:

            win_count = 0
            lose_count = 0

            pyramid_temp = deepcopy(self)

            pyramid_temp.setLine(PossibleLine)
            print(PossibleLine.toString(), end='')

            recursive_result = pyramid_temp.next_move_recursive(
                self.player_mode_other, level=0)
            if (win_count + lose_count) == 0:
                # 表示這一層的嘗試就分出勝負了
                if recursive_result:
                    rate = 1
                else:
                    rate = 0
            else:
                rate = win_count / (win_count + lose_count)

            if player_first:
                # 只有玩家先行才有可能，所有嘗試都沒有 100 % 勝率，
                # 才需要紀錄最大勝率
                if rate > max_rate:
                    max_rate = rate
                    max_rate_move = PossibleLine
                # 判斷可接受勝率，所有可能跑完其實蠻慢的 QQ
                if (rate * 100) >= MinAcceptableProbability and not recursive_result:
                    print('發現可接受獲勝機率為 ' + str(int(rate * 100)) + ' %')
                    self.setLine(PossibleLine)
                    return PossibleLine

            print('獲勝機率為 ' + str(int(rate * 100)) + ' %')

            if recursive_result:
                self.setLine(PossibleLine)
                return PossibleLine
            else:
                pass

        if player_first:
            if max_rate_move is None:
                self.computer_lose = True
            else:
                self.setLine(max_rate_move)
            return max_rate_move

        return None

    def getInputLine(self):
        while True:
            line_str = input('請按照右邊的編號輸入你想要畫的線 1 ~ 3 個: ')
            number_list = re.findall(r'\d+', line_str)
            number_list = list(map(int, number_list))

            if len(number_list) < 1 or 3 < len(number_list):
                logger.info('輸入錯誤')
                continue

            input_ok = True
            for n in number_list:
                if n < 0 or 14 < n:
                    logger.info('請輸入 0 ~ 14 之間的數字')
                    input_ok = False
            if not input_ok:
                continue

            point_list = []
            for n in number_list:
                point_list.append(PointList[n])
            result = Line(point_list)

            if result not in self.legal_move:
                logger.info('不合法的輸入')
                continue
            break

        return Line(point_list)


if __name__ == '__main__':
    logger = Logger('Nim')
    logger.info('Welcome to TriangularNim version', Version)

    win_count = 0
    lose_count = 0
    PointList = []

    for i in range(5):
        for ii in range(i + 1):
            p = Point(i, ii)
            PointList.append(p)

    pyramid = Pyramid()
    pyramid.show()
    input_line = None
    player_first = False
    try:
        while True:
            c = input('你要先下嗎? [Y/n] ')
            if c == '' or c.lower() == 'y':
                logger.info('選擇先下')

                MinAcceptableProbability = 0
                while True:
                    try:
                        MinAcceptableProbability = input(
                            '請輸入電腦可接受獲勝機率 (0~100): ')
                        MinAcceptableProbability = int(
                            MinAcceptableProbability)
                        if 0 <= MinAcceptableProbability <= 100:
                            break
                        logger.info('參數有誤，請重新輸入')
                    except Exception:
                        MinAcceptableProbability = 0

                player_first = True
                input_line = pyramid.getInputLine()

                break
            elif c.lower() == 'n':
                logger.info('選擇後下')
                break
            else:
                logger.info('錯誤的輸入，請重新輸入')

        while not pyramid.is_finish():
            ComputerMove = pyramid.next_move(
                last_line=input_line, player_first=player_first)
            if ComputerMove is None:
                logger.info('電腦認輸')
                break
            pyramid.show()
            print('電腦選擇 ', end='')
            for p in ComputerMove.line:
                point_str = str(PointList.index(p))
                if len(point_str) == 1:
                    point_str = '0' + point_str
                print(point_str + ' ', end='')
            print('')

            if pyramid.is_finish():
                logger.info('電腦獲勝')
                break
            input_line = pyramid.getInputLine()
    except KeyboardInterrupt:
        logger.info('使用者中斷')

    logger.info('遊戲結束')
