import pygame
import solver
import sys

# Initiate pygame
pygame.init()
resolution = width, height = 1300, 900
screen = pygame.display.set_mode(resolution)
pygame.display.set_caption("Sudoku")
font = pygame.font.Font(None, 66)
small_font = pygame.font.Font(None, 46)


class Board():

    def __init__(self):
        self.board = solver.create_puzzle(60)
        self.cell_size = 100
        self.grid_size = 9
    
    def display_board(self, x, y, highlighted_cell, font_colour):
        
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                # Draw cell border
                if (x//100)*100 == col * self.cell_size and (y//100)*100 == row * self.cell_size or (row, col) == highlighted_cell:
                    pygame.draw.rect(screen, (225, 225, 225), (col * self.cell_size, row * self.cell_size, self.cell_size, self.cell_size))
                else:
                    pygame.draw.rect(screen, (255, 255, 255), (col * self.cell_size, row * self.cell_size, self.cell_size, self.cell_size))
                # Draw cell lines
                pygame.draw.rect(screen, (200, 200, 200), (col * self.cell_size, row * self.cell_size, self.cell_size, self.cell_size), 1)

                # Draw number
                if self.board[row][col] != 0:
                    text_surface = font.render(str(self.board[row][col]), True, font_colour) 
                    screen.blit(text_surface, (col * self.cell_size + 38, row * self.cell_size + 29))            
                

        # Draw the thicker lines for the 3x3 sections
        for i in range(1, self.grid_size):
            if i % 3 == 0:  # Every third line is thicker
                pygame.draw.line(screen, (0, 0, 61), (i * self.cell_size, 0), (i * self.cell_size, 900), 5)
                pygame.draw.line(screen, (0, 0, 61), (0, i * self.cell_size), (900, i * self.cell_size), 5)


class Numpad:
    def __init__(self):
        self.buttons = []  # Stores button rects for numbers and clear button
        self.create_buttons()
        self.position = (450, 450)
    
    def create_buttons(self):
        # Create buttons for numbers 1-9 in a 3x3 grid
        button_size = 80
        padding = 10
        for i in range(9):
            row = i // 3
            col = i % 3
            x = col * (button_size + padding) + padding
            y = row * (button_size + padding) + padding
            rect = pygame.Rect(960 + x, 450 + y, button_size, button_size)
            self.buttons.append((str(i + 1), rect))

        # Create the "Clear" button below the number grid
        clear_x = padding
        clear_y = 3 * (button_size + padding) + padding
        clear_width = 100 - 2 * padding
        clear_height = button_size
        clear_rect = pygame.Rect(1050 + clear_x, 450 + clear_y, clear_width, clear_height)
        self.buttons.append(("X", clear_rect))

    def draw_numpad(self):
        # Draw each button with its label
        for label, rect in self.buttons:
            pygame.draw.rect(screen, (150, 150, 150), rect)
            pygame.draw.rect(screen, (0, 0, 0), rect, 2)  # Border
            text_surface = small_font.render(label, True, (0, 0, 0))
            text_rect = text_surface.get_rect(center=rect.center)
            screen.blit(text_surface, text_rect)
    
    def handle_click(self, pos, board, highlighted_cell, valid):
        
        row, col = highlighted_cell

        # Check if a button was clicked
        for label, rect in self.buttons:
            if rect.collidepoint(pos):
                if label == "X":
                    valid = solver.is_valid(board.board, row, col, 14)
                    board.board[row][col] = 0
                else:
                    valid = solver.is_valid(board.board, row, col, int(label))
                    board.board[row][col] = int(label)

        return board, valid


class Button:
    def __init__(self, text, x, y, width, height, color, hover_color):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.hover_color = hover_color

    def draw(self, screen):
        # Change color on hover
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, self.hover_color, self.rect)
        else:
            pygame.draw.rect(screen, self.color, self.rect)
        
        # Draw text on button
        text_surface = font.render(self.text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self, event):
        # Check if the button is clicked
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False


def main():
    board = Board()
    run = True
    highlighted_cell = None
    numpad = Numpad()
    font_colour = (0, 0, 0)
    valid = True
    new_game = Button ("New Game", 950, 50, 300, 100, (255, 255, 255), (200, 200, 200))
    show_solution = Button ("Solution", 950, 200, 300, 100, (255, 255, 255), (200, 200, 200))
    # Main game loop
    while run:

        x, y = pygame.mouse.get_pos()
        

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if highlighted_cell is not None:
                    board, valid = numpad.handle_click((x, y), board, highlighted_cell, valid)
                
                if show_solution.is_clicked(event):
                    num_count = solver.find_num_count(board.board)
                    num_count = sorted(range(1, 10), key=lambda num: num_count[num])
                    board.board = solver.solution(board.board, num_count)
                
                if new_game.is_clicked(event):
                    board = Board()
                    
                row = y // board.cell_size
                col = x // board.cell_size
                highlighted_cell = (row, col)  # Update highlighted cell

        if not valid:
            font_colour = (255, 0, 0)
        else:
            font_colour = (0, 0, 0)

        # Draw screen
        board.display_board(x, y, highlighted_cell, font_colour)
        pygame.draw.rect(screen, (60, 60, 60), (900, 0, 400, 900))
        numpad.draw_numpad()
        new_game.draw(screen)
        show_solution.draw(screen)
        pygame.display.flip()

if __name__ == "__main__":
    main()
    