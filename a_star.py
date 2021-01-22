# Ideas used from https://www.youtube.com/watch?v=JtiK0DOeI4A&t=3613s
import pygame
import math
from queue import PriorityQueue

WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A* Path Finding Algorithm")

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

def Node():
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

    def reset():
        self.color = WHITE

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x,self.y, self.width, self.width))



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
        drawGrid(WIN, 20, WIDTH)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        pygame.display.update()
    pygame.quit()

main()

