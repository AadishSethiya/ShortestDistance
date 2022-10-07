import queue
import pygame
from queue import PriorityQueue

WIDTH = 800
HEIGHT = 800
Screen = pygame.display.set_mode((WIDTH + 40, HEIGHT + 40))     #starting the screen
pygame.display.set_caption("Djikstras Path Finding Algoritm")       #setting the caption

  
PETAL = (242, 226, 224)
WHITE = (255,255,255)
BLACK = (0,0,0)
POPPY = (220, 52, 59)
STEM = (171,223,143)
GREEN = (0, 255, 127)
BLUE = (5,4,170)
PEACH = (255,218,185)
YELLOW = (255,255,0)
LAVENDER = (164, 131, 194)

class Box:
    #class to represent each cell of the matrix
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row*width + 20
        self.y = col*width + 20
        self.color = PEACH
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    def getPos(self):
        #returns the position of cell
        return self.row, self.col

    def isChecked(self):
        #checks if the cell has already been visited
        return self.color == STEM

    def isAvailable(self):
        #checks if the cell has not been visited
        return self.color == GREEN

    def isObstacle(self):
        #checks if the cell is a barrier
        return self.color == POPPY

    def isStart(self):
        #checks if the cell is starting point
        return self.color == BLUE

    def isEnd(self):
        #checks if the cell is ending point
        return self.color == YELLOW

    def Reset(self):
        #resets the cell
        self.color = PEACH
        return

    def makeChecked(self):
        #marks the cell checked
        self.color = STEM
        return

    def makeAvailable(self):
        #marks the cell available
        self.color = GREEN
        return

    def makeObstacle(self):
        #marks the cell as obstacle
        self.color = POPPY
        return

    def makeStart(self):
        #marks the cell as starting point
        self.color = BLUE
        return

    def makeEnd(self):
        #marks the cell as ending point
        self.color = YELLOW
        return

    def makePath(self):
        #makes the path between the two points
        self.color = LAVENDER
        return

    def drawBox(self, screen):
        #draws the cell
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.width))
        return

    def findNeighbors(self, matrix):
        #finds all the neighbors which aren't obstacles
        if self.row < self.total_rows - 1 and not matrix[self.row+1][self.col].isObstacle():        #condition for bottom most row
            self.neighbors.append(matrix[self.row+1][self.col])

        if self.row > 0 and not matrix[self.row-1][self.col].isObstacle():      #condition for upper most row
            self.neighbors.append(matrix[self.row-1][self.col]) 

        if self.col < self.total_rows - 1 and not matrix[self.row][self.col+1].isObstacle():        #condition for right most column
            self.neighbors.append(matrix[self.row][self.col+1])

        if self.col > 0 and not matrix[self.row][self.col-1].isObstacle():      #condition for the left most column
            self.neighbors.append(matrix[self.row][self.col-1])

    def __lt__(self,other):     #defines the less than operator for the cells
        return False


def path(prev,node,screen,matrix,rows,width):
    #function to display the shortest path
    while node in prev:
        node = prev[node]
        node.makePath()
        draw(screen,matrix,rows,width)

def Dijkstras(matrix, start, end, screen, rows, width):
    #implementation of dijkstras algorithm
    pq = PriorityQueue()        #initialization of priority queue
    distance = {box: float("inf") for row in matrix for box in row}     #initialization of all the distances
    visited = [start]       #contains the visited nodes
    prev = {}       #contains the prev nodes
    distance[start] = 0     
    pq.put((0,start))
    while not pq.empty():
        for event in pygame.event.get():        #quit of user input
            if event.type == pygame.QUIT:
                pygame.quit()
        dis, current = pq.get()
        visited.remove(current)
        if current == end:      #if we have reached end node, drw the path
            path(prev,end,screen,matrix,rows,width)
            end.makeEnd()
            return True
        for neighbor in current.neighbors:
            if distance[current] + 1 < distance[neighbor]:      #input neighbors in pq if it's actual distance is less than the assumed distance
                prev[neighbor] = current
                distance[neighbor] = distance[current] + 1
                if neighbor not in visited:
                    visited.append(neighbor)
                    pq.put((distance[neighbor],neighbor))
                    neighbor.makeAvailable()
        draw(screen, matrix, rows, width)       #visualization
        if current != start:
            current.makeChecked()

    return False


def makeMatrix(rows,width):
    #function to make matrix
    matrix = []
    dis = width // rows
    for i in range(rows):
        row = []
        for j in range(rows):
            box = Box(i,j,dis,rows)
            row.append(box)
        matrix.append(row)
    return matrix

def drawLines(screen, rows, width):
    #function to draw matrix lines
    dis = width // rows
    for i in range(rows + 1):
        pygame.draw.line(screen, POPPY, (20 + i*dis,20), (20 + i*dis,20 + width))
        pygame.draw.line(screen, POPPY, (20, 20 + i*dis), (20 + width, 20 + i*dis))

def draw(screen, matrix, rows, width):
    #function to draw the matrix
    screen.fill(PEACH)
    for row in matrix:
        for box in row:
            box.drawBox(screen)
    
    drawLines(screen,rows,width)
    pygame.display.update()

def getMouseLoc(pos, rows, width):
    #function to get the location of the point on which mouse clicked
    dif = width//rows
    y, x = pos
    row = (y - 20) // dif
    col = (x - 20) // dif
    return row, col

if __name__ == "__main__":
    ROWS = 50
    matrix = makeMatrix(ROWS,WIDTH)
    run = True
    start = None
    end = None
    started = False
    erase = False
    while run:
        draw(Screen,matrix,ROWS,WIDTH)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:       #quit on user input
                run =  False
            if started:
                continue
            if pygame.mouse.get_pressed()[0]:       #draw with left click
                    pos = pygame.mouse.get_pos()
                    row, col = getMouseLoc(pos, ROWS, WIDTH)
                    if row < ROWS and col < ROWS:
                        box = matrix[row][col]
                    if start == None and not box.isEnd():       #draw the start
                        start = box
                        start.makeStart()
                    elif end == None and not box.isStart():     #draw the end
                        end = box
                        end.makeEnd()
                    elif box != start and box != end:       #draw the barriers
                        box.makeObstacle()
            elif pygame.mouse.get_pressed()[1]:     #erase with right click
                pos = pygame.mouse.get_pos()
                row, col = getMouseLoc(pos, ROWS, WIDTH)
                box = matrix[row][col]
                if box == start:
                    start = None
                elif box == end:
                    end - None
                box.Reset()
            if event.type == pygame.KEYDOWN:        #start the algorithm
                if event.key == pygame.K_RETURN and not started:
                    started = True
                    for row in matrix:
                        for box in row:
                            box.findNeighbors(matrix)
                    Dijkstras(matrix, start, end, Screen, ROWS, WIDTH)
    pygame.quit()