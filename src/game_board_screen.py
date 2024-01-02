import pygame

from game_logic import GameState

BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
CELL_SIZE = 80

ACTIVE_PLAYER_NAME_COLOR = 'light green'
INACTIVE_PLAYER_NAME_COLOR = 'light gray'
BOARD_COLOR = 'dark blue'
BUTTON_COLOR_1 = YELLOW
BUTTON_COLOR_2 = RED

FOOTER_HEIGHT = 75


class GameScreen:
    game_state = GameState()
    board_rows = len(GameState.board)
    board_columns = len(GameState.board[0])
    mouse_pressed = False

    def __init__(self, screen: pygame.Surface):
        self.background = pygame.image.load("../img/cloud_background.jpg").convert()
        self.cup_image = pygame.image.load("../img/cup.png").convert_alpha()
        self.cup_image = pygame.transform.scale(self.cup_image, (self.cup_image.get_size()[0]/6, self.cup_image.get_size()[1]/6))

        self.screen = screen
        self.game_board_surf = pygame.Surface((CELL_SIZE * self.board_columns, CELL_SIZE * self.board_rows), pygame.SRCALPHA)
        self.game_board_rect = self.game_board_surf.get_rect(bottomleft=((screen.get_width()-self.game_board_surf.get_width())/2, screen.get_size()[1] - FOOTER_HEIGHT))

        self.above_game_board_surf = pygame.Surface((CELL_SIZE * self.board_columns, CELL_SIZE), pygame.SRCALPHA)
        self.above_game_board_rect = self.above_game_board_surf.get_rect(bottomleft=self.game_board_rect.topleft)

        self.player_names = pygame.font.Font(None, 50)
        self.player_1_surf = self.player_names.render(self.game_state.player_1_name, True, INACTIVE_PLAYER_NAME_COLOR)
        self.player_1_rect = self.player_1_surf.get_rect(topleft=(30, 20))
        self.player_2_surf = self.player_names.render(self.game_state.player_2_name, True, INACTIVE_PLAYER_NAME_COLOR)
        self.player_2_rect = self.player_2_surf.get_rect(topright=(self.screen.get_width() - 30, 20))

        self.footer = pygame.Surface((screen.get_size()[0],FOOTER_HEIGHT))
        self.footer.fill('light gray')
        self.footer_location = (0, self.screen.get_size()[1] - self.footer.get_height())
        self.button_width, self.button_height = 150, 50
        self.exit_button_rect = pygame.Rect(0, 0, self.button_width, self.button_height)
        self.new_game_button_rect = pygame.Rect(200, 0, self.button_width, self.button_height)
        font = pygame.font.Font(None, 36)
        self.exit_button_label = font.render("Exit", True, (0, 0, 0))
        self.new_game_button_label = font.render("New game", True, (0, 0, 0))


    def update_player_data(self):
        if self.game_state.player_turn == 1:
            background_rect = self.player_1_rect.copy()
            background_rect = background_rect.scale_by(1.1,1.1)
            background_surf = pygame.Surface((background_rect.width,background_rect.height), pygame.SRCALPHA)
            pygame.draw.rect(background_surf,"gold",(0,0,background_rect.width,background_rect.height), border_radius=20)

            self.player_1_surf = self.player_names.render(self.game_state.player_1_name, True, ACTIVE_PLAYER_NAME_COLOR)
            self.player_2_surf = self.player_names.render(self.game_state.player_2_name, True, INACTIVE_PLAYER_NAME_COLOR)
        else:
            self.player_1_surf = self.player_names.render(self.game_state.player_1_name, True, INACTIVE_PLAYER_NAME_COLOR)
            self.player_2_surf = self.player_names.render(self.game_state.player_2_name, True, ACTIVE_PLAYER_NAME_COLOR)
            

    def draw_game_board(self,win_condition:list[(int,int)]):
        surface = self.game_board_surf
        last_row = self.board_rows-1
        last_column = self.board_columns-1

        for row in range(self.board_rows):
            for col in range(self.board_columns):
                board_rect = (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                if (row, col) == (0, 0):
                    pygame.draw.rect(surface, BOARD_COLOR, board_rect, border_top_left_radius=20)
                elif (row, col) == (last_row, 0):
                    pygame.draw.rect(surface, BOARD_COLOR, board_rect, border_bottom_left_radius=20)
                elif (row, col) == (0, last_column):
                    pygame.draw.rect(surface, BOARD_COLOR, board_rect, border_top_right_radius=20)
                elif (row, col) == (last_row, last_column):
                    pygame.draw.rect(surface, BOARD_COLOR, board_rect, border_bottom_right_radius=20)
                else:
                    pygame.draw.rect(surface, BOARD_COLOR, board_rect)

                button_center = (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2)
                button_size = CELL_SIZE // 2 - 5
                is_winning_button = (row, col) in win_condition

                if self.game_state.board[row][col] != 0:
                    self.__draw_button(surface, self.game_state.board[row][col], button_center,button_size, is_winning_button)
                elif self.game_state.board[row][col] == 0:
                    pygame.draw.circle(surface, (0, 0, 0, 0), button_center, button_size)


    def update_chiplocation(self, mousebutton_up:bool):
        self.above_game_board_surf.fill((0, 0, 0, 0))
        if self.game_state.is_running():
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if mouse_y >= self.above_game_board_rect.topleft[1] and mouse_y <= self.game_board_rect.bottomleft[1]:
                relative_x_loc = mouse_x - self.above_game_board_rect.topleft[0]
                if relative_x_loc >=0 and relative_x_loc <= self.above_game_board_rect.width:
                    active_col = relative_x_loc // CELL_SIZE
                    if mousebutton_up:
                        self.game_state.drop_button(active_col)
                    self.__draw_button(self.above_game_board_surf, self.game_state.player_turn,(active_col * CELL_SIZE + CELL_SIZE // 2,CELL_SIZE // 2), CELL_SIZE // 2 - 5)
        elif self.game_state.is_finished():
            self.above_game_board_surf.blit(self.cup_image,(0,0))
            if self.game_state.player_turn == 1:
                winner_name = self.game_state.player_1_name
            else:
                winner_name = self.game_state.player_2_name
            winner_name_surf = self.player_names.render(f"{winner_name} Has Won!",True,"gold")
            self.above_game_board_surf.blit(winner_name_surf, (self.cup_image.get_size()[0]+10,20))

    def __draw_button(self, surface : pygame.Surface, player: int, center: (int,int), size:int,winning_button=False):
        if player == 1:
            button_color = BUTTON_COLOR_1
        elif player == 2:
            button_color = BUTTON_COLOR_2
        else:
            raise Exception(f"Unexpected player id: {player}")

        if winning_button:
            pygame.draw.circle(surface, "dark orange", center, size)
            pygame.draw.circle(surface, button_color, center, size - 5)
        else:
            pygame.draw.circle(surface, button_color, center, size)
            pygame.draw.circle(surface, "dark gray", center, size - 5, 2)


    def draw_menu(self,events):
        pygame.draw.rect(self.footer,"red",self.exit_button_rect)
        self.footer.blit(self.exit_button_label,(self.exit_button_rect.x + 10, self.exit_button_rect.y + 10))
        pygame.draw.rect(self.footer,"red", self.new_game_button_rect)
        self.footer.blit(self.new_game_button_label, (self.new_game_button_rect.x + 10, self.new_game_button_rect.y + 10))

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = (pygame.mouse.get_pos()[0]-self.footer_location[0], pygame.mouse.get_pos()[1]-self.footer_location[1])
                if self.exit_button_rect.collidepoint(mouse_pos):
                    pygame.quit()
                    exit()
                elif self.new_game_button_rect.collidepoint(mouse_pos):
                    self.game_state.new_game()


    def is_finished(self):
        return self.game_state.is_finished()

    def is_running(self):
        return self.game_state.is_running()

    def draw(self, events):
        win_condition = self.game_state.check_finished_game()

        self.draw_game_board(win_condition)

        self.update_chiplocation(pygame.MOUSEBUTTONUP in [t.type for t in events])
        self.update_player_data()

        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.footer, self.footer_location)
        self.draw_menu(events)

        self.screen.blit(self.player_1_surf, self.player_1_rect)
        self.screen.blit(self.player_2_surf, self.player_2_rect)
        self.screen.blit(self.game_board_surf, self.game_board_rect)
        self.screen.blit(self.above_game_board_surf, self.above_game_board_rect)


