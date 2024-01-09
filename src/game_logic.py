from dataclasses import dataclass
from enum import Enum
import numpy as np

BOARD_SIZE = (6, 7) # 6 rows and 7 columns in a four in a row board

class States(Enum):
    RUNNING = 1
    FINISHED = 2

@dataclass
class GameState:
    board = np.zeros(BOARD_SIZE, dtype=int)
    player_turn = 1

    player_1_name = "Player 1"
    player_2_name = "Player 2"

    player_1_score = 0
    player_2_score = 0

    game_state = States.RUNNING

    def is_running(self):
        return self.game_state == States.RUNNING

    def is_finished(self):
        return self.game_state == States.FINISHED

    def new_game(self):
        self.game_state = States.RUNNING
        self.board = np.zeros(BOARD_SIZE, dtype=int)
        self.player_turn = 1

    def check_finished_game(self) -> list[(int, int)]:
        win_range = []

        for i in range(0, self.board.shape[0]-3):
            for j in range(0, self.board.shape[1]):
                if (self.board[i][j] != 0 and
                        self.board[i][j] == self.board[i+1][j] and
                        self.board[i][j] == self.board[i+2][j] and
                        self.board[i][j] == self.board[i+3][j]):
                    win_range = [(i+k,j) for k in range(0,4)]
        for i in range(0, self.board.shape[0]):
            for j in range(0, self.board.shape[1]-3):
                if (self.board[i][j] != 0 and
                        self.board[i][j] == self.board[i][j+1] and
                        self.board[i][j] == self.board[i][j+2] and
                        self.board[i][j] == self.board[i][j+3]):
                    win_range = [(i, j+k) for k in range(0, 4)]
        for i in range(3, self.board.shape[0]):
            for j in range(0, self.board.shape[1]-3):
                if (self.board[i][j] != 0 and
                        self.board[i][j] == self.board[i-1][j + 1] and
                        self.board[i][j] == self.board[i-2][j + 2] and
                        self.board[i][j] == self.board[i-3][j + 3]):
                    win_range = [(i - k, j + k) for k in range(0, 4)]
        for i in range(0, self.board.shape[0] - 3):
            for j in range(0, self.board.shape[1] - 3):
                if (self.board[i][j] != 0 and
                        self.board[i][j] == self.board[i + 1][j + 1] and
                        self.board[i][j] == self.board[i + 2][j + 2] and
                        self.board[i][j] == self.board[i + 3][j + 3]):
                    win_range = [(i + k, j + k) for k in range(0, 4)]

        if self.game_state != States.FINISHED and len(win_range) > 0:
            self.__set_finished()
        return win_range

    def __set_finished(self):
        self.game_state = States.FINISHED
        if self.player_turn == 1:
            self.player_1_score += 1
        else:
            self.player_2_score += 1


    #return the vertical position until where to drop
    def drop_button(self, col: int) -> int:
        if self.board[0, col] != 0:
            return -1
        for i in range(1, self.board.shape[0]+1):
            if i == self.board.shape[0] or self.board[i, col] != 0:
                self.board[i-1, col] = self.player_turn
                if self.check_finished_game() == []:
                    self.player_turn = 3 - self.player_turn
                return i-1



        
