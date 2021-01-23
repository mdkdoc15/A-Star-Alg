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
        self.color = GREEN
    
    def make_closed(self):
        self.color = RED
    
    def make_barrier(self):
        self.color = BLACK
    
    def make_path(self):
        self.color = PURPLE

    def reset(self):
        self.color = WHITE

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x,self.y, self.width, self.width))

    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row < self.total_rows -1 and not grid[self.row + 1][self.col].is_barrier(): # Is the square below us free?
            self.neighbors.append(grid[self.row +1][self.col])
        if self.row > 0 and not grid[self.row-1][self.col].is_barrier(): # Is square above free?
            self.neighbors.append(grid[self.row-1][self.col])
        if self.col < self.total_rows -1 and not grid[self.row][self.col+ 1].is_barrier(): # Is the square to the right free?
            self.neighbors.append(grid[self.row][self.col+1])
        if self.col > 0 and not grid[self.row][self.col-1].is_barrier(): # Is square to the left free?
            self.neighbors.append(grid[self.row][self.col-1])


    #Used when comparing 2 nodes, not sure its application
    def __lt__(self, other):
        return False


def h(p1,p2):
    #returns the manhatann distance between two points
    x1 ,y1 = p1
    x2,y2 = p2
    return abs(x1-x2) + abs(y1-y2)

def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()

def algorithm(draw, grid, start, end):
    
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {node : float('inf') for row in grid for node in row}
    g_score[start] = 0
    f_score = {node : float('inf') for row in grid for node in row}
    f_score[start] = h(start.get_pos(), end.get_pos())

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2] # Gives us the node we want
        open_set_hash.remove(current) # Keep the hash up to date with the open set
        
        if current == end: 
            # We found the shortest path
            reconstruct_path(came_from, end, draw)
            end.make_end()
            start.make_start()
            return True
        
        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                # AKA we have found a better path
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
                
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()
                    

        draw()

        if current != start:
            current.make_closed()
            
    return False

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
    win.fill(WHITE)

    for row in grid:
        for col in row:
            col.draw(win)

    draw_grid(win, rows, total_width)
    pygame.display.update()

def draw_grid(screen, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(screen, GREY, (0, i*gap), (width, i*gap))
        for j in range(rows):
            pygame.draw.line(screen, GREY, (j*gap, 0), (j*gap,width))

def get_pos_clicked(pos, rows, width):
    x, y = pos
    gap  = width // rows
    row = y // gap
    col = x // gap
    return row, col



def main(win, width):
    ROWS = 50
    grid = make_grid(ROWS, width)

    start = None
    end = None

    run = True
    started = False

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if started:
                # If we are finding a path we only want the user to be able to exit the program, not add any more walls
                continue
            if pygame.mouse.get_pressed()[0]: #if left click add boxes
                pos = pygame.mouse.get_pos()
                row , col = get_pos_clicked(pos, ROWS, width)
                node = grid[row][col] 
                if not start and node != end:
                    start = node
                    node.make_start()
                elif not end and node != start:
                    end = node
                    node.make_end()
                elif node != start and node != end:
                    node.make_barrier()
                
            if pygame.mouse.get_pressed()[2]: #if right click remove boxes
                pos = pygame.mouse.get_pos()
                row , col = get_pos_clicked(pos, ROWS, width)
                node = grid[row][col]
                if node == start:
                    start = None
                elif node == end:
                    end = None
                node.reset()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)
                    algorithm(lambda: draw(win,grid,ROWS, width), grid, start, end)
                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)
                
        draw(WIN, grid, ROWS, WIDTH)
    pygame.quit()


main(WIN, WIDTH)

