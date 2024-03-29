import json
import os
import random
import re
from argparse import ArgumentParser
from copy import deepcopy

from SingleLog.log import Logger

version = '0.2.0'


def copy_func(o):
    return deepcopy(o)


all_point_list = None
player_first = False
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

with open(os.path.join(__location__, 'cache.json')) as f:
    cache_map = json.load(f)


class Point:
    def __init__(self, y, x):
        self.y = y
        self.x = x

    def show(self):
        print(self)

    def __str__(self):
        result = f'{all_point_list.index(self):02}'
        return result

    def __eq__(self, other):
        return self.y == other.y and self.x == other.x

    def __lt__(self, other):
        if self.y < other.y:
            return True
        if self.x < other.x:
            return True
        return False


class Line:
    def __init__(self, point_list):
        self.line = sorted(point_list)

    def show(self):
        print(self)

    def __str__(self):
        return f'Line: {" ".join([str(x) for x in self.line])}'

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


class TriangularNim(object):
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
            [False, False, False, False, False]]

        global all_point_list
        all_point_list = []

        for i in range(5):
            for ii in range(i + 1):
                p = Point(i, ii)
                all_point_list.append(p)

        self.win_count = 0
        self.lose_count = 0

        self.legal_move = []
        legal_move_temp = []

        # 把所有可能的步驟列出來
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

        self.legal_move = sorted(legal_move_temp, reverse=True)

    def __str__(self):
        result = ''
        size = 2

        index = 0
        for i in range(5):
            for _ in range((5 - i - 1) * size):
                result += ' '

            line = []
            for ii in range(i + 1):
                if self.map[i][ii]:
                    line.append('__')
                else:
                    line.append(f'{index:02}')
                index += 1
            result += '  '.join(line) + '\n'

        return result

    def show(self):

        print(self)

    def set_line(self, line):
        if line not in self.legal_move:
            print('[Error] Not in Legal move')
            return

        remove_list = []

        for p in line.line:
            self.map[p.y][p.x] = True

            for line_obj in self.legal_move:
                legal_line = line_obj.line
                if p in legal_line and line_obj not in remove_list:
                    remove_list.append(line_obj)

        for remove_line in remove_list:
            self.legal_move.remove(remove_line)

    def count_value(self):
        result = 0
        p = 1
        for x in [x for sublist in self.map for x in sublist]:
            result += (1 * p if x else 0)
            p *= 2

        return f'{result}'

    def next_move_recursive(self, mode, level=-1):

        global cache_map

        # True 我方獲勝
        if len(self.legal_move) == 1 and len(self.legal_move[0].line) == 1:
            # 只剩下最後一格的情況
            if mode == self.player_mode_me:
                # 如果是我方，則輸 False
                return False, 0, 1
            else:
                # 如果是對方，則贏 True
                return True, 1, 0
        elif len(self.legal_move) == 0:
            # 已經沒有圈圈可以畫了，表示上一輪就結束了
            if mode == self.player_mode_me:
                # 如果是我方，則贏 True
                return True, 1, 0
            else:
                # 如果是對方，則輸 False
                return False, 0, 1

        for possible_line in self.legal_move:

            next_move_map = copy_func(self)
            next_move_map.set_line(possible_line)

            next_move_value = next_move_map.count_value()

            if next_move_value in cache_map:
                temp_list = cache_map[next_move_value]
                restore_mode, restore_result = temp_list[0], temp_list[1]

                result = (restore_result if mode == restore_mode else not restore_result)
            else:
                result, _, _ = next_move_map.next_move_recursive(
                    self.player_mode_mask - mode, level=(level + 1))

            if level == 0:
                # 遞迴第一層紀錄一下可以獲勝的事件
                if result:
                    self.win_count += 1
                else:
                    self.lose_count += 1

            if next_move_value not in cache_map:
                cache_map[next_move_value] = [mode, result]

            if mode == self.player_mode_me and result:
                # 如果是換我方下 目標是找到 True (我方獲勝)
                return True, self.win_count, self.lose_count
            elif mode == self.player_mode_other and not result:
                # 如果是換對方下 目標是找到 False (我方失敗)
                return False, self.win_count, self.lose_count

        if mode == self.player_mode_me:
            # 如果我方都找不到獲勝的下一步，則回傳 False
            return False, self.win_count, self.lose_count
        elif mode == self.player_mode_other:
            # 如果對方都找不到讓我方失敗的下一步，則回傳 True (我方獲勝)
            return True, self.win_count, self.lose_count

    def is_finish(self):
        condition0 = len(self.legal_move) == 1 and len(
            self.legal_move[0].line) == 1
        condition1 = len(self.legal_move) == 0
        condition2 = self.computer_lose
        return condition0 or condition1 or condition2

    def next_move(self, last_line=None):

        global all_point_list
        global player_first

        if last_line is not None:
            self.set_line(last_line)
            self.show()

        if len(self.legal_move) == 1:
            return None

        if not args.demo and len(self.legal_move) == 63:
            # 先手的話就下必勝路徑的第一手
            # 九種開場隨便挑，都 100 %
            best_move_list = [
                Line([all_point_list[0]]),
                Line([all_point_list[10]]),
                Line([all_point_list[14]]),
                Line([all_point_list[3]]),
                Line([all_point_list[4]]),
                Line([all_point_list[5]]),
                Line([all_point_list[7]]),
                Line([all_point_list[8]]),
                Line([all_point_list[12]])]

            best_move_index = random.randrange(0, len(best_move_list))

            line_temp = best_move_list[best_move_index]
            # 就是這麼霸氣，直接給出勝率 100 % 的答案
            if args.probability:
                print(f'{line_temp} 獲勝機率為 100 %')
            self.set_line(line_temp)
            return line_temp

        if player_first:
            max_rate = 0
            max_rate_move = None

        if args.demo:
            logger.info('分析所有可能第一手獲勝機率')
        else:
            logger.info('開始分析')
        for possible_line in self.legal_move:

            pyramid_temp = copy_func(self)

            pyramid_temp.set_line(possible_line)
            if args.demo or args.probability:
                print(possible_line, end='')

            recursive_result, win_count, lose_count = pyramid_temp.next_move_recursive(
                self.player_mode_other, level=0)

            logger.debug('count', win_count, lose_count)
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
                    max_rate_move = possible_line
            if args.demo or args.probability:
                print(' 獲勝機率為 ' + str(int(rate * 100)) + ' %')

            if not args.demo and recursive_result:
                self.set_line(possible_line)
                return possible_line
            else:
                pass

        if not args.demo and player_first:
            if max_rate_move is None:
                self.computer_lose = True
            else:
                self.set_line(max_rate_move)
            return max_rate_move

        return None

    def get_input_line(self):
        global player_first
        while True:
            if len(self.legal_move) == 63:
                line_str = input('請按照上方的編號輸入你想要畫的線 1 ~ 3 個 (Enter 電腦先下): ')
                if line_str == '':
                    return None
                else:
                    player_first = True

            else:
                line_str = input('請按照上方的編號輸入你想要畫的線 1 ~ 3 個: ')
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
                point_list.append(all_point_list[n])
            result = Line(point_list)

            if result not in self.legal_move:
                logger.info('不合法的輸入')
                continue
            break

        return Line(point_list)


if __name__ == '__main__':
    logger = Logger('Nim')
    logger.info('Welcome to TriangularNim version', version)

    parser = ArgumentParser()
    parser.add_argument('-D', '--demo', help="count best move demo", action="store_true")
    parser.add_argument('-P', '--probability', help="show probability", action="store_true")
    args = parser.parse_args()

    nim = TriangularNim()
    nim.show()

    input_line = None
    try:
        if args.demo:
            computer_move = nim.next_move()
            # with open('src/cache.json', 'w') as f:
            #     json.dump(count_map, f)
        else:
            input_line = nim.get_input_line()
            while not nim.is_finish():
                computer_move = nim.next_move(last_line=input_line)
                if computer_move is None:
                    logger.info('認輸')
                    break

                next_move = []
                for p in computer_move.line:
                    point_str = str(all_point_list.index(p))
                    next_move.append(point_str)
                logger.info('下一步', ' '.join(next_move))

                nim.show()

                if nim.is_finish():
                    logger.info('電腦獲勝')
                    break
                input_line = nim.get_input_line()
    except KeyboardInterrupt:
        logger.info('使用者中斷')

    logger.info('遊戲結束')
