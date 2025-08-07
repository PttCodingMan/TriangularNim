import json
import os
import random
import re
from argparse import ArgumentParser
from copy import deepcopy
from typing import List, Optional, Tuple, Set

version = '0.2.3'  # Bump version for the changes

# The real path to the directory containing this script
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))


class Point:
    """Represents a single point on the triangular board."""
    all_point_list: List['Point'] = []

    def __init__(self, y: int, x: int):
        self.y = y
        self.x = x

    def show(self) -> None:
        print(self)

    def __str__(self) -> str:
        try:
            index = Point.all_point_list.index(self)
            return f'{index:02}'
        except (ValueError, AttributeError):
            return '??'

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Point):
            return NotImplemented
        return self.y == other.y and self.x == other.x

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Point):
            return NotImplemented
        if self.y != other.y:
            return self.y < other.y
        return self.x < other.x

    def __hash__(self) -> int:
        return hash((self.y, self.x))


class Line:
    """Represents a line of 1 to 3 points that can be drawn in a move."""
    def __init__(self, point_list: List[Point]):
        self.line: List[Point] = sorted(point_list)

    def show(self) -> None:
        print(self)

    def __str__(self) -> str:
        return f'Line: {" ".join([str(x) for x in self.line])}'

    def __eq__(self, other: object) -> bool:
        if other is None:
            return False
        if not isinstance(other, Line):
            return NotImplemented
        if len(self.line) != len(other.line):
            return False
        return self.line == other.line

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Line):
            return NotImplemented
        if len(self.line) != len(other.line):
            return len(self.line) < len(other.line)
        return self.line < other.line

    def __hash__(self) -> int:
        return hash(tuple(self.line))


class TriangularNim(object):
    """Encapsulates the entire game logic for Triangular Nim."""
    player_mode_me: int = 1
    player_mode_other: int = 2
    player_mode_mask: int = 3

    BOARD_SIZE: int = 5
    NUM_POINTS: int = 15

    def __init__(self):
        self.player_first: bool = False
        self.map: List[List[bool]] = [[False for _ in range(i + 1)] for i in range(self.BOARD_SIZE)]

        self.all_point_list: List[Point] = []
        for i in range(self.BOARD_SIZE):
            for ii in range(i + 1):
                p = Point(i, ii)
                self.all_point_list.append(p)
        Point.all_point_list = self.all_point_list

        try:
            with open(os.path.join(__location__, 'cache.json')) as f:
                self.cache_map: dict = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.cache_map = {}

        self.win_count: int = 0
        self.lose_count: int = 0
        self.legal_move: List[Line] = self._generate_legal_moves()

    def _generate_legal_moves(self) -> List[Line]:
        """Generates all possible lines that can be drawn on the board."""
        legal_move_temp: List[Line] = []
        
        # --- Generate lines of length 1 ---
        for p in self.all_point_list:
            legal_move_temp.append(Line([p]))

        all_points_set: Set[Point] = set(self.all_point_list)

        # --- Generate lines of length 2 ---
        for y in range(self.BOARD_SIZE):
            for x in range(y + 1):
                start_p = Point(y, x)
                # Horizontal
                if Point(y, x + 1) in all_points_set:
                    legal_move_temp.append(Line([start_p, Point(y, x + 1)]))
                # Diagonal down-left
                if Point(y + 1, x) in all_points_set:
                    legal_move_temp.append(Line([start_p, Point(y + 1, x)]))
                # Diagonal down-right
                if Point(y + 1, x + 1) in all_points_set:
                    legal_move_temp.append(Line([start_p, Point(y + 1, x + 1)]))

        # --- Generate lines of length 3 ---
        temp_len_2_lines = [l for l in legal_move_temp if len(l.line) == 2]
        for line_obj in temp_len_2_lines:
            p0, p1 = line_obj.line[0], line_obj.line[1]
            # Horizontal
            if p0.y == p1.y and p0.x + 1 == p1.x and Point(p1.y, p1.x + 1) in all_points_set:
                legal_move_temp.append(Line([p0, p1, Point(p1.y, p1.x + 1)]))
            # Diagonal down-left
            if p0.y + 1 == p1.y and p0.x == p1.x and Point(p1.y + 1, p1.x) in all_points_set:
                legal_move_temp.append(Line([p0, p1, Point(p1.y + 1, p1.x)]))
            # Diagonal down-right
            if p0.y + 1 == p1.y and p0.x + 1 == p1.x and Point(p1.y + 1, p1.x + 1) in all_points_set:
                legal_move_temp.append(Line([p0, p1, Point(p1.y + 1, p1.x + 1)]))

        # Use a set to remove duplicates before sorting
        return sorted(list(set(legal_move_temp)), reverse=True)

    def __str__(self) -> str:
        result = ''
        size = 2
        index = 0
        for i in range(self.BOARD_SIZE):
            result += ' ' * ((self.BOARD_SIZE - i - 1) * size)
            line_items = []
            for ii in range(i + 1):
                if self.map[i][ii]:
                    line_items.append('__')
                else:
                    line_items.append(f'{index:02}')
                index += 1
            result += '  '.join(line_items) + '\n'
        return result

    def show(self) -> None:
        print(self)

    def set_line(self, line: Line) -> None:
        if line not in self.legal_move:
            print('[Error] Not in Legal move')
            return
        for p in line.line:
            self.map[p.y][p.x] = True
        self.legal_move = [m for m in self.legal_move if not any(p in m.line for p in line.line)]

    def count_value(self) -> str:
        result = 0
        p = 1
        for row in self.map:
            for cell in row:
                result += (1 * p if cell else 0)
                p *= 2
        return str(result)

    def next_move_recursive(self, mode: int, level: int = -1) -> Tuple[bool, int, int]:
        if len(self.legal_move) == 1 and len(self.legal_move[0].line) == 1:
            return (mode == self.player_mode_other, 1, 0) if mode == self.player_mode_other else (False, 0, 1)
        elif not self.legal_move:
            return (mode == self.player_mode_me, 1, 0) if mode == self.player_mode_me else (False, 0, 1)

        for possible_line in self.legal_move:
            next_move_map = deepcopy(self)
            next_move_map.set_line(possible_line)
            next_move_value = next_move_map.count_value()

            if next_move_value in self.cache_map:
                temp_list = self.cache_map[next_move_value]
                restore_mode, restore_result = temp_list[0], temp_list[1]
                result = (restore_result if mode == restore_mode else not restore_result)
            else:
                result, _, _ = next_move_map.next_move_recursive(self.player_mode_mask - mode, level + 1)

            if level == 0:
                if result: self.win_count += 1
                else: self.lose_count += 1

            if next_move_value not in self.cache_map:
                self.cache_map[next_move_value] = [mode, result]

            if mode == self.player_mode_me and result:
                return True, self.win_count, self.lose_count
            elif mode == self.player_mode_other and not result:
                return False, self.win_count, self.lose_count

        return (mode == self.player_mode_other, self.win_count, self.lose_count)

    def is_finish(self) -> bool:
        return not self.legal_move

    def next_move(self, last_line: Optional[Line] = None) -> Optional[Line]:
        if last_line:
            self.set_line(last_line)
            self.show()
        if self.is_finish():
            return None

        if not args.demo and not self.player_first and len(self.legal_move) == 63:
            best_move_list = [Line([self.all_point_list[i]]) for i in [0, 10, 14, 3, 4, 5, 7, 8, 12]]
            line_temp = random.choice(best_move_list)
            if args.probability:
                print(f'{line_temp} 獲勝機率為 100 %')
            self.set_line(line_temp)
            return line_temp

        max_rate = -1.0
        max_rate_move: Optional[Line] = None
        winning_move: Optional[Line] = None

        print('分析所有可能第一手獲勝機率' if args.demo else '開始分析...')
        for possible_line in self.legal_move:
            pyramid_temp = deepcopy(self)
            pyramid_temp.cache_map = self.cache_map  # Ensure the cache is shared, not copied
            pyramid_temp.set_line(possible_line)
            if args.demo or args.probability:
                print(possible_line, end='')

            pyramid_temp.win_count, pyramid_temp.lose_count = 0, 0
            win_in_recursive, win_count, lose_count = pyramid_temp.next_move_recursive(self.player_mode_other, level=0)
            
            rate = win_count / (win_count + lose_count) if (win_count + lose_count) > 0 else (1.0 if win_in_recursive else 0.0)

            if args.demo or args.probability:
                print(f' 獲勝機率為 {int(rate * 100)} %')

            if rate > max_rate:
                max_rate = rate
                max_rate_move = possible_line

            if not args.demo and not args.probability and win_in_recursive:
                winning_move = possible_line
                break
        
        best_move = winning_move if winning_move else max_rate_move
        if best_move:
            self.set_line(best_move)
        return best_move

    def get_input_line(self) -> Optional[Line]:
        while True:
            prompt = '請按照上方的編號輸入你想要畫的線 1 ~ 3 個'
            if len(self.legal_move) == 63:
                prompt += ' (Enter 電腦先下): '
                line_str = input(prompt)
                if line_str == '': return None
                self.player_first = True
            else:
                line_str = input(prompt + ': ')

            try:
                number_list = [int(n) for n in re.findall(r'\d+', line_str)]
                if not (1 <= len(number_list) <= 3): raise ValueError("僅能輸入 1 到 3 個數字")
                if not all(0 <= n < self.NUM_POINTS for n in number_list): raise ValueError(f"請輸入 0 ~ {self.NUM_POINTS - 1} 之間的數字")
                
                point_list = [self.all_point_list[n] for n in number_list]
                result = Line(point_list)
                if result not in self.legal_move: raise ValueError("不合法的輸入")
                
                return result
            except ValueError as e:
                print(e)
                continue

if __name__ == '__main__':
    print(f'Welcome to TriangularNim version {version}')

    parser = ArgumentParser()
    parser.add_argument('-D', '--demo', help="count best move demo", action="store_true")
    parser.add_argument('-P', '--probability', help="show probability", action="store_true")
    args = parser.parse_args()

    nim = TriangularNim()
    try:
        if args.demo:
            nim.show()
            nim.next_move()
        else:
            nim.show()
            input_line = nim.get_input_line()
            # Main game loop
            while not nim.is_finish():
                computer_move = nim.next_move(last_line=input_line)
                if not computer_move:
                    print('您拿走了最後的棋子，您輸了！')
                    break
                
                move_indices = [str(nim.all_point_list.index(p)) for p in computer_move.line]
                print(f"電腦下: {' '.join(move_indices)}")
                nim.show()

                if nim.is_finish():
                    print('電腦拿走了最後的棋子，您獲勝了！')
                    break
                
                input_line = nim.get_input_line()
    except KeyboardInterrupt:
        print('\n使用者中斷')
    except Exception as e:
        print(f"發生未預期的錯誤: {e}")
    finally:
        print('遊戲結束')
        if args.demo and nim.cache_map:
            print('正在儲存快取...')
            with open(os.path.join(__location__, 'cache.json'), 'w') as f:
                json.dump(nim.cache_map, f, indent=2)
            print('快取已儲存。')
