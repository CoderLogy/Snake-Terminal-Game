import curses
import random


class Game:
    def __init__(self, snakeX, snakeY):
        self.snakeX = snakeX
        self.snakeY = snakeY
        self.snakeBody = [[self.snakeY, self.snakeX], [self.snakeY, self.snakeX-1], [self.snakeY, self.snakeX-2]]
        self.food = [self.snakeY // 2, self.snakeX // 2] #inital food of snake
        self.screenHeight, self.screenWidth = curses.initscr().getmaxyx()
        self.window = curses.newwin(self.screenHeight, self.screenWidth, 0, 0) #creates window for me to interact with
        self.window.keypad(True) #enables keyboard input  
        self.window.timeout(100)
        self.score = 0
        curses.curs_set(0) #removes my cursor
    def initialize_game(self):
        self.initalKey = curses.KEY_RIGHT
        self.box = self.window.subwin(self.screenHeight-2,self.screenWidth-2,1,2)
        self.box.box()
        curses.start_color()
        curses.init_pair(1, curses.COLOR_GREEN,curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_RED,curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_YELLOW,curses.COLOR_BLACK)
        self.window.addch(self.food[0],self.food[1],curses.ACS_PI,curses.color_pair(2))
    def check_collisions(self):
        if (self.snakeBody[0][0] in [1,self.screenHeight - 2] 
            or self.snakeBody[0][1] in [2,self.screenWidth - 2] 
            or self.snakeBody[0] in self.snakeBody[1:]):
            print(f"Game Over! Final Score: {self.score}")
            curses.endwin()
            quit()
    def main_game(self):
        self.initialize_game()
        while not self.check_collisions():
            scoreText = f"Score: {self.score}"
            self.window.addstr(0,self.screenWidth//2 - len(scoreText)//2, scoreText,curses.color_pair(3))
            nextKey = self.window.getch()
            opposite_directions = {
                        curses.KEY_RIGHT: curses.KEY_LEFT,
                        curses.KEY_LEFT: curses.KEY_RIGHT,
                        curses.KEY_UP: curses.KEY_DOWN,
                        curses.KEY_DOWN: curses.KEY_UP
                        }

            if nextKey != -1 and nextKey != opposite_directions.get(self.initalKey,None):
                self.initalKey = nextKey
            newHead = [self.snakeBody[0][0], self.snakeBody[0][1]] #creates a newHead
            match self.initalKey: #ain't that cool
                case curses.KEY_RIGHT:
                    newHead[1]+=1
                case curses.KEY_LEFT:
                    newHead[1]-=1
                case curses.KEY_UP:
                    newHead[0]-=1
                case curses.KEY_DOWN:
                    newHead[0]+=1
            self.snakeBody.insert(0, newHead) #adds the newHead to 0 index of snake body i.e at first place
            self.window.addch(newHead[0],newHead[1], curses.ACS_CKBOARD,curses.color_pair(1)) #this the player's body shape
            if self.snakeBody[0] == self.food:
                self.food = None
                self.score+=1
                while self.food is None:
                    newFood= [
                        random.randint(1, self.screenHeight - 4),
                        random.randint(1, self.screenWidth - 4)
                    ]
                    self.food = newFood if newFood not in self.snakeBody else None
                self.window.addch(self.food[0],self.food[1],curses.ACS_PI,curses.color_pair(2))
            else:
                tail = self.snakeBody.pop()
                self.window.addch(tail[0],tail[1], ' ') 
                '''Above 3 lines gives illusion player is moving actually 
                   its just adding a new block on every r,u,l,d  keystrokes detected, '
                   'but this command deletes everything until player proves it has eaten food ''' 

if __name__ == '__main__':
    INITAL_SCREEN = curses.initscr() #initalizes terminal as pov
    screenHeight, screenWidth = INITAL_SCREEN.getmaxyx()
    snakeX = screenWidth // 4
    snakeY = screenHeight // 2
    #added custom values above so players don't go insane and snake is there on the screen
    game = Game(snakeX, snakeY)
    game.main_game()
    curses.endwin()