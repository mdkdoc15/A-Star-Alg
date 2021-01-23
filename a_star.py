# Ideas used from https://www.youtube.com/watch?v=JtiK0DOeI4A&t=3613s
import pygame
import math
from queue import PriorityQueue

WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A* Path Finding Algorithm")

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

class Node:
    def __init__(self, row, col, width, total_rows):
        self.color = WHITE
        self.row = row
        self.col = col
        self.width = width
        self.x = col * width
        self.y = row * width
        self.total_rows = total_rows
        self.neighbors = []
    
    def get_pos(self):
        return self.row, self.col
    
    def if_open(self):
        return self.color == WHITE
    
    def is_closed(self):
        return self.color == RED
    
    def is_barrier(self):
        return self.color == BLACK

    def make_start(self):
        self.color = ORANGE

    def make_end(self):
        self.color = TURQUOISE

    def make_open(self):
        self.color = WHITE
    
    def make_closed(self):
        self.color = RED
    
    def make_barrier(self):
        self.color = BLACK

    def reset(self):
        self.color = WHITE

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x,self.y, self.width, self.width))

    def update_neighbors(self, grid):
        pass    
    
    #Used when comparing 2 nodes, not sure its application
    def __lt__(self, other):
        return False


def h(p1,p2):
    #returns the manhatann distance between two points
    x1 ,y1 = p1
    x2,y2 = p2
    return abs(x1-x2) + abs(y1-y2)

def make_grid(rows, total_width):
    gap = total_width // rows
    grid = []
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, gap, rows)
            grid[i].append(node)
    
    return grid

def draw(win, grid, rows, total_width):
    gap = total_width // rows
    for row in grid:
        for col in row:
            col.draw(win)

def drawGrid(screen, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(screen, GREY, (0, i*gap), (width, i*gap))
        for j in range(rows):
            pygame.draw.line(screen, GREY, (j*gap, 0), (j*gap,width))
    


def main():
    pygame.init()

    run = True
    while run:
        WIN.fill(WHITE)
        grid = make_grid(20, WIDTH)
        draw(WIN, grid, 20, WIDTH)
        drawGrid(WIN, 20, WIDTH)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        pygame.display.update()
    pygame.quit()

main()

