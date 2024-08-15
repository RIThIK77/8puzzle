import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Class to represent the puzzle
class Puzzle:
    def __init__(self, board):
        self.board = board

    def get_blank_position(self):
        return np.argwhere(self.board == 0)[0]

    def move(self, row, col):
        blank_row, blank_col = self.get_blank_position()
        if (abs(blank_row - row) == 1 and blank_col == col) or (abs(blank_col - col) == 1 and blank_row == row):
            self.board[blank_row, blank_col], self.board[row, col] = self.board[row, col], self.board[blank_row, blank_col]
            return True
        return False

# Function to create puzzle pieces
def create_puzzle_pieces(image_path):
    try:
        image = Image.open(image_path)
        image = image.resize((300, 300))
        pieces = []
        piece_size = 100
        for i in range(3):
            for j in range(3):
                piece = image.crop((j*piece_size, i*piece_size, (j+1)*piece_size, (i+1)*piece_size))
                pieces.append(piece)
        return pieces
    except FileNotFoundError:
        print(f"Error: Image not found at '{image_path}'")
        return None

# Function to check if the puzzle is solvable
def is_solvable(board):
    inv_count = 0
    flat_board = board.flatten()
    for i in range(8):
        for j in range(i + 1, 9):
            if flat_board[i] and flat_board[j] and flat_board[i] > flat_board[j]:
                inv_count += 1
    return inv_count % 2 == 0

# Function to generate a solvable puzzle
def generate_solvable_puzzle():
    while True:
        board = np.arange(9)
        np.random.shuffle(board)
        board = board.reshape(3, 3)
        if is_solvable(board):
            return board

# Function to display the puzzle
def display_puzzle(pieces, board, ax):
    blank_index = 8
    for i in range(3):
        for j in range(3):
            index = board[i, j]
            if index == blank_index:
                ax[i, j].imshow(np.ones((100, 100, 3)))
            else:
                ax[i, j].imshow(pieces[index])
            ax[i, j].axis('off')

# Function to handle click events
def onclick(event, puzzle, pieces, ax):
    if event.inaxes is not None:
        row, col = int(event.ydata // 100), int(event.xdata // 100)
        if puzzle.move(row, col):
            display_puzzle(pieces, puzzle.board, ax)
            fig.canvas.draw()

if __name__ == "__main__":
    image_path = 'bird-8788491_1280.jpg'  # Update with your image path

    pieces = create_puzzle_pieces(image_path)
    if pieces is None:
        exit()  # Exit if image loading failed

    initial_state = generate_solvable_puzzle()
    puzzle = Puzzle(initial_state)

    fig, ax = plt.subplots(3, 3)
    display_puzzle(pieces, puzzle.board, ax)

    cid = fig.canvas.mpl_connect('button_press_event', lambda event: onclick(event, puzzle, pieces, ax))
    plt.show()