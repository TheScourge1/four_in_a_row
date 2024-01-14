import pygame

from game_logic import GameState

BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
CELL_SIZE = 80
FOOTER_COLOR = (0,0,0,50)
SCORE_COLOR = "gold"

TEXT_FONTSIZE = 35
PLAYERNAME_FONTSIZE= 50
BUTTON_COLOR = "white"
BUTTON_TEXT_COLOR = "white"

ACTIVE_PLAYER_NAME_COLOR = 'light green'
INACTIVE_PLAYER_NAME_COLOR = 'light gray'
BOARD_COLOR = 'dark blue'
BUTTON_COLOR_1 = YELLOW
BUTTON_COLOR_2 = RED

FOOTER_HEIGHT = 75


class Button:
    def __init__(self, color, text_color, text_size, width, height, text):
        self.color = color
        self.width = width
        self.height = height
        self.text = text

        self.text_font = pygame.font.Font(None, text_size)
        self.label = self.text_font.render(text, False, text_color)
        self.surf = pygame.Surface((width,height),pygame.SRCALPHA)
        pygame.draw.rect(self.surf, color, (0, 0, width, height),2, border_radius=15)
        self.rect = self.surf.get_rect()
        self.surf.blit(self.label, self.label.get_rect(center=self.surf.get_rect().center))

        self.invisi_surf = pygame.Surface((width, height), pygame.SRCALPHA)
        self.invisi_surf.fill(color)
        self.invisi_surf.blit(self.surf, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)
        mask = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        pygame.draw.rect(mask, color, (0, 0, self.width, self.height), 0, border_radius=15)
        self.invisi_surf.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

    def draw(self, surf: pygame.Surface, location: tuple[int,int],mouse_location=(-1,-1)):
        if self.rect.collidepoint(mouse_location):
            self.rect = self.invisi_surf.get_rect(topleft=location)
            surf.blit(self.invisi_surf, self.rect)
        else:
            self.rect = self.surf.get_rect(topleft=location)
            surf.blit(self.surf, self.rect)

    def draw_invisi(self, surf: pygame.Surface, location: tuple[int, int]):
        self.rect = self.invisi_surf.get_rect(topleft=location)
        surf.blit(self.invisi_surf, self.rect)


class GameScreen:
    game_state = GameState()
    board_rows = len(GameState.board)
    board_columns = len(GameState.board[0])
    mouse_pressed = False

    player_1_surf = None
    player_2_surf = None

    def __init__(self, screen: pygame.Surface):
        self.text_font = pygame.font.Font(None, TEXT_FONTSIZE)
        self.background = pygame.image.load("../img/cloud_background.jpg").convert()
        self.cup_image = pygame.image.load("../img/cup.png").convert_alpha()
        self.cup_image = pygame.transform.scale(self.cup_image, (self.cup_image.get_size()[0]/6, self.cup_image.get_size()[1]/6))

        self.screen = screen
        self.game_board_surf = pygame.Surface((CELL_SIZE * self.board_columns, CELL_SIZE * self.board_rows), pygame.SRCALPHA)
        self.game_board_rect = self.game_board_surf.get_rect(bottomleft=((screen.get_width()-self.game_board_surf.get_width())/2, screen.get_size()[1] - FOOTER_HEIGHT))

        self.above_game_board_surf = pygame.Surface((CELL_SIZE * self.board_columns, CELL_SIZE), pygame.SRCALPHA)
        self.above_game_board_rect = self.above_game_board_surf.get_rect(bottomleft=self.game_board_rect.topleft)

        self.player_names_font = pygame.font.Font(None, PLAYERNAME_FONTSIZE)

        self.player_1_surf = pygame.Surface((200,100),pygame.SRCALPHA)
        self.player_2_surf = pygame.Surface((200, 100), pygame.SRCALPHA)
        self.player_1_rect = self.player_1_surf.get_rect(topleft=(30, 20))
        self.player_2_rect = self.player_2_surf.get_rect(topright=(self.screen.get_width() - 30, 20))

        self.footer = pygame.Surface((screen.get_size()[0],FOOTER_HEIGHT),pygame.SRCALPHA)
        self.footer.fill(FOOTER_COLOR)
        self.footer_location = (0, self.screen.get_size()[1] - self.footer.get_height())

        self.exit_button = Button(BUTTON_COLOR,BUTTON_TEXT_COLOR,TEXT_FONTSIZE,150,50,"Exit")
        self.new_game_button = Button(BUTTON_COLOR, BUTTON_TEXT_COLOR, TEXT_FONTSIZE, 150, 50, "New Game")
        self.reset_score_button = Button(BUTTON_COLOR, BUTTON_TEXT_COLOR, TEXT_FONTSIZE, 150, 50, "Reset Score")


    def draw_player_data(self):
        self.player_1_surf = pygame.Surface((200, 60), pygame.SRCALPHA)
        self.player_2_surf = pygame.Surface((200, 60), pygame.SRCALPHA)

        if self.game_state.player_turn == 1:
            player_1_name_surf = self.player_names_font.render(self.game_state.get_player_name(1), True, ACTIVE_PLAYER_NAME_COLOR)
            player_2_name_surf = self.player_names_font.render(self.game_state.get_player_name(2), True, INACTIVE_PLAYER_NAME_COLOR)
        else:
            player_1_name_surf = self.player_names_font.render(self.game_state.get_player_name(1), True, INACTIVE_PLAYER_NAME_COLOR)
            player_2_name_surf = self.player_names_font.render(self.game_state.get_player_name(2), True, ACTIVE_PLAYER_NAME_COLOR)

        player_1_score = self.text_font.render(f"Wins: {self.game_state.get_score(1)}",True,SCORE_COLOR)
        player_1_score_rect = player_1_score.get_rect(midbottom=self.player_1_surf.get_rect().midbottom)
        player_2_score = self.text_font.render(f"Wins: {self.game_state.get_score(2)}",True,SCORE_COLOR)
        player_2_score_rect = player_2_score.get_rect(midbottom=self.player_2_surf.get_rect().midbottom)

        self.__draw_button(self.player_1_surf, 1, (15, 15), 15)
        self.__draw_button(self.player_2_surf, 2, (15, 15), 15)
        self.player_1_surf.blit(player_1_name_surf,(40,0))
        self.player_1_surf.blit(player_1_score, player_1_score_rect)

        self.player_2_surf.blit(player_2_name_surf, (40, 0))
        self.player_2_surf.blit(player_2_score, player_2_score_rect)


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
        if self.game_state.is_running() and self.game_state.human_player_move():
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if mouse_y >= self.above_game_board_rect.topleft[1] and mouse_y <= self.above_game_board_rect.bottomleft[1]:
                relative_x_loc = mouse_x - self.above_game_board_rect.topleft[0]
                if relative_x_loc >=0 and relative_x_loc <= self.above_game_board_rect.width:
                    active_col = relative_x_loc // CELL_SIZE
                    if mousebutton_up:
                        self.game_state.drop_button(active_col)
                    self.__draw_button(self.above_game_board_surf, self.game_state.player_turn,(active_col * CELL_SIZE + CELL_SIZE // 2,CELL_SIZE // 2), CELL_SIZE // 2 - 5)
            else:
                if self.game_state.player_turn == 1:
                    self.__draw_button(self.above_game_board_surf, self.game_state.player_turn,(CELL_SIZE // 2,CELL_SIZE // 2), CELL_SIZE // 2 - 5)
                else:
                    self.__draw_button(self.above_game_board_surf, self.game_state.player_turn,
                                       (6*CELL_SIZE+CELL_SIZE // 2, CELL_SIZE // 2), CELL_SIZE // 2 - 5)

        elif self.game_state.is_finished():
            self.above_game_board_surf.blit(self.cup_image,(0,0))
            winner_name = self.game_state.get_player_name(self.game_state.player_turn)
            winner_name_surf = self.player_names_font.render(f"{winner_name} Has Won!",True,"gold")
            self.above_game_board_surf.blit(winner_name_surf, (self.cup_image.get_size()[0]+10,20))
        elif self.game_state.is_draw():
            winner_name_surf = self.player_names_font.render("Draw!",True,"gold")
            self.above_game_board_surf.blit(winner_name_surf, (10, 20))

    def __draw_button(self, surface : pygame.Surface, player: int, center: (int,int), size:int,winning_button=False):
        if player == 1:
            button_color = BUTTON_COLOR_1
        elif player == 2:
            button_color = BUTTON_COLOR_2
        else:
            raise Exception(f"Unexpected player id: {player}")

        if winning_button:
            pygame.draw.circle(surface, "dark orange", center, size)
            pygame.draw.circle(surface, button_color, center, size-int(size / 6))
        else:
            pygame.draw.circle(surface, button_color, center, size)
            pygame.draw.circle(surface, "dark gray", center, size-int(size / 6), 2)


    def draw_menu(self,events):
        self.footer = pygame.Surface((self.screen.get_size()[0],FOOTER_HEIGHT),pygame.SRCALPHA)
        self.footer.fill(FOOTER_COLOR)
        mouse_pos = (pygame.mouse.get_pos()[0] - self.footer_location[0], pygame.mouse.get_pos()[1] - self.footer_location[1])

        height_offset = int((self.footer.get_rect().height-self.exit_button.height)/2)
        width_center = int((self.footer.get_rect().width-self.exit_button.width)/2)
        self.exit_button.draw(self.footer,(width_center-180,height_offset),mouse_pos)
        self.new_game_button.draw(self.footer,(width_center,height_offset),mouse_pos)
        self.reset_score_button.draw(self.footer, (width_center + 180, height_offset), mouse_pos)

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = (pygame.mouse.get_pos()[0]-self.footer_location[0], pygame.mouse.get_pos()[1]-self.footer_location[1])
                if self.exit_button.rect.collidepoint(mouse_pos):
                    pygame.quit()
                    exit()
                elif self.new_game_button.rect.collidepoint(mouse_pos):
                    self.game_state.new_game()
                elif self.reset_score_button.rect.collidepoint(mouse_pos):
                    self.game_state.reset_score()

    def is_finished(self):
        return self.game_state.is_finished()

    def is_running(self):
        return self.game_state.is_running()

    def draw(self, events):
        win_condition = self.game_state.check_finished_game()

        self.game_state.play_round()
        self.draw_game_board(win_condition)

        self.update_chiplocation(pygame.MOUSEBUTTONUP in [t.type for t in events])
        self.draw_player_data()

        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.footer, self.footer_location)
        self.draw_menu(events)

        self.screen.blit(self.player_1_surf, self.player_1_rect)
        self.screen.blit(self.player_2_surf, self.player_2_rect)
        self.screen.blit(self.game_board_surf, self.game_board_rect)
        self.screen.blit(self.above_game_board_surf, self.above_game_board_rect)


