from dataclasses import dataclass
from enum import Enum
import numpy as np
import time

BOARD_SIZE = (6, 7)  # 6 rows and 7 columns in a four in a row board


class States(Enum):
    RUNNING = 1
    FINISHED = 2
    DRAW = 3


class PlayerType(Enum):
    HUMAN = 1
    AI_LEVEL_1 = 2


@dataclass
class GameState:
    board = np.zeros(BOARD_SIZE, dtype=int)
    ai_think_time = 60
    player_turn = 1

    __player_types = [PlayerType.HUMAN, PlayerType.HUMAN]
    __player_score = [0, 0]
    __player_names = ["Player 1", "Player 2"]

    game_state = States.RUNNING
    button_drop_time = 0

    def is_running(self):
        return self.game_state == States.RUNNING

    def is_finished(self):
        return self.game_state == States.FINISHED

    def is_draw(self):
        return self.game_state == States.DRAW

    def new_game(self):
        self.game_state = States.RUNNING
        self.board = np.zeros(BOARD_SIZE, dtype=int)
        self.player_turn = 1
        self.button_drop_time = 0

    def human_player_move(self) -> bool:
        return self.__player_types[self.player_turn - 1] == PlayerType.HUMAN

    def set_player_type(self, player_id, player_type: PlayerType):
        if player_id not in (1, 2):
            raise Exception(f"invalid player id: {player_id}")
        self.__player_types[player_id - 1] = player_type

    def get_score(self, player_id):
        return self.__player_score[player_id - 1]

    def get_player_name(self, player_id):
        return self.__player_names[player_id - 1]

    def check_finished_game(self) -> list[(int, int)]:
        win_range = self.__find_four_in_a_row(self.board)

        if self.game_state != States.FINISHED and len(win_range) > 0:
            self.__set_finished()
        return win_range

    def drop_button(self, col: int) -> int:
        row = self.__get_drop_location(col)
        self.board[row, col] = self.player_turn
        self.button_drop_time = time.time()
        self.check_finished_game()

        can_still_play = np.any(self.board[0] == 0)
        if not can_still_play:
            self.game_state = States.DRAW

        if self.game_state == States.RUNNING:
            self.player_turn = 3 - self.player_turn
        return row

    # execute computer move
    def play_round(self):
        if (self.game_state == States.RUNNING and not self.human_player_move() and
                self.button_drop_time != 0 and time.time() - self.button_drop_time > self.ai_think_time):
            next_move = self.find_winning_col(self.player_turn)
            if next_move < 0:
                potential_moves = [col for col in range(0, len(self.board[0])) if self.board[0, col] == 0]
                next_move = np.random.choice(potential_moves)

            self.drop_button(next_move)

    def reset_score(self):
        self.new_game()
        self.__player_score=[0,0]

    def find_winning_col(self, player_id: int) -> int:
        for col in range(0, self.board[0]):
            row = self.__get_drop_location(col)
            if row > 0:
                self.board[row][col] = player_id
                win_range = self.__find_four_in_a_row(self.board)
                self.board[row][col] = 0
                if win_range:
                    return col
        return -1

    def __find_four_in_a_row(self, grid: np.ndarray):
        win_range = []

        for i in range(0, grid.shape[0] - 3):
            for j in range(0, grid.shape[1]):
                if (grid[i][j] != 0 and
                        grid[i][j] == grid[i + 1][j] and
                        grid[i][j] == grid[i + 2][j] and
                        grid[i][j] == grid[i + 3][j]):
                    win_range = [(i + k, j) for k in range(0, 4)]
        for i in range(0, grid.shape[0]):
            for j in range(0, grid.shape[1] - 3):
                if (grid[i][j] != 0 and
                        grid[i][j] == grid[i][j + 1] and
                        grid[i][j] == grid[i][j + 2] and
                        grid[i][j] == grid[i][j + 3]):
                    win_range = [(i, j + k) for k in range(0, 4)]
        for i in range(3, grid.shape[0]):
            for j in range(0, grid.shape[1] - 3):
                if (grid[i][j] != 0 and
                        grid[i][j] == grid[i - 1][j + 1] and
                        grid[i][j] == grid[i - 2][j + 2] and
                        grid[i][j] == grid[i - 3][j + 3]):
                    win_range = [(i - k, j + k) for k in range(0, 4)]
        for i in range(0, grid.shape[0] - 3):
            for j in range(0, grid.shape[1] - 3):
                if (grid[i][j] != 0 and
                        grid[i][j] == grid[i + 1][j + 1] and
                        grid[i][j] == grid[i + 2][j + 2] and
                        grid[i][j] == grid[i + 3][j + 3]):
                    win_range = [(i + k, j + k) for k in range(0, 4)]
        return win_range

    def __set_finished(self):
        self.game_state = States.FINISHED
        self.button_drop_time = 0
        self.__player_score[self.player_turn - 1] += 1

    # return the vertical position until where to drop
    def __get_drop_location(self, col: int) -> int:
        if self.board[0, col] != 0:
            return -1

        for i in range(1, self.board.shape[0] + 1):
            if i == self.board.shape[0] or self.board[i, col] != 0:
                return i - 1

        raise Exception("No valid drop location found")
