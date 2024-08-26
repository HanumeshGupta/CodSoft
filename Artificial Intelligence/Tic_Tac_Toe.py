import sys 
import pygame
import copy
import random
import numpy as np


width = 600
height = 600

Rows = 3
Cols = 3

sqsize = width/Cols

line_width = 15
radius = sqsize//4
cir_width = 15

cross_width= 20
offset = 50

# Colors

cross_col= (66,66,66)
cir_color = (239,231,200)
bg_color = (28, 170 ,156)
line_color = (23, 145, 135)


#Pygame Setup


pygame.init()
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption("Tic Tac Toe AI")
screen.fill(bg_color)

class Board:

  def __init__(self):

    self.squares = np.zeros((Rows,Cols))
    self.empty_sqrs = self.squares  #List of Squares
    self.marked_sqrs = 0

  def final_state(self,show = False):
    '''
    @return 0 if there is no win yet
    @return 1 if player 1 wins
    @return 2 if player 2 wins

    '''

    #Vertical Wins
    for col in range(Cols):
      if self.squares[0][col] == self.squares[1][col] == self.squares[2][col] != 0:
        if show :
          color = cir_color if self.squares[0][col] == 2 else cross_col
          iPos = (col*sqsize+sqsize//2,20)
          fPos = (col*sqsize+sqsize//2,height-20)
          pygame.draw.line(screen,color,iPos,fPos,line_width)
        return self.squares[0][col]

    #Horizontal Wins
    for row in range(Rows):
      if self.squares[row][0] == self.squares[row][1] == self.squares[row][2] != 0:

        if show:
          color = cir_color if self.squares[row][0] == 2 else cross_col
          iPos = (20,row*sqsize+sqsize//2)
          fPos = (width-20,row*sqsize+sqsize//2)
          pygame.draw.line(screen,color,iPos,fPos,line_width)
        return self.squares[row][0]


    # Desc diagonal Wins
    if self.squares[0][0] == self.squares[1][1] == self.squares[2][2] != 0:
        if show:
            color = cir_color if self.squares[0][0] == 2 else cross_col
            iPos = (20, 20)
            fPos = (width - 20, height - 20)
            pygame.draw.line(screen, color, iPos, fPos, cross_width)
        return self.squares[1][1]

    # Asc diagonal Wins
    if self.squares[2][0] == self.squares[1][1] == self.squares[0][2] != 0:
        if show:
            color = cir_color if self.squares[2][0] == 2 else cross_col
            iPos = (20, height - 20)
            fPos = (width - 20, 20)
            pygame.draw.line(screen, color, iPos, fPos, cross_width)
        return self.squares[1][1]

    # No wins
    return 0





  def marked_sqr(self,row,col,player):
    self.squares[row][col] = player
    self.marked_sqrs += 1



  def empty_sqr(self,row,col):
    return self.squares[row][col] == 0


  def get_empty_sqr(self):
    empty_sqrs = []
    for row in range(Rows):
      for col in range(Cols):
        if self.empty_sqr(row,col):
          empty_sqrs.append((row,col))


    return empty_sqrs


  def isfull(self):
    return self.marked_sqrs == 9


  def isempty(self):
    return self.marked_sqrs == 0



class AI:

  def __init__(self,level=1,player=2):
    self.level = level
    self.player = player


  def rnd(self,board):
    empty_sqrs = board.get_empty_sqr()
    idx = random.randrange(0,len(empty_sqrs))

    return empty_sqrs[idx] #Row and Col


  def minimax(self,board,maximizing):

    #Terminal Case
    case= board.final_state() != 0 or board.isfull()
  

    #Player 1 Won
    if case == 1:
      return 1,None  #eval,Mobe

    #Player 2 Won
    if case == 2:
      return -1,None

    #Draw
    elif board.isfull():
      return 0,None


    if maximizing:
      max_eval = -100
      best_move = None
      empty_sqrs = board.get_empty_sqr()

      for (row,col) in empty_sqrs:
        temp_board = copy.deepcopy(board)
        temp_board.marked_sqr(row,col,1)
        eval = self.minimax(temp_board,False)[0]

        if eval > max_eval:
          max_eval = eval
          best_move = (row,col)

      return max_eval,best_move

    elif not maximizing:
      min_eval = 100
      best_move = None
      empty_sqrs = board.get_empty_sqr()

      for (row,col) in empty_sqrs:
        temp_board = copy.deepcopy(board)
        temp_board.marked_sqr(row,col,self.player)
        eval = self.minimax(temp_board,True)[0]

        if eval < min_eval:
          min_eval = eval
          best_move = (row,col)

      return min_eval,best_move


  def eval(self,main_board):
    if self.level == 0:
      #Random choice
      eval = 'random'
      move = self.rnd(main_board)
      sqr = random.choice(main_board.get_empty_sqr())

    else:
      #Minimax Algo
      eval, move =self.minimax(main_board,False)


    print(f'AI has chosen to mark the square in pos {move} with an eval of {eval}')


    return move #row,col



class Game:
  def __init__(self):
    self.board = Board()
    self.ai = AI()
    self.player = 1  # Player 1 make cross and Player 2 will make circle
    self.gamemode = 'ai' #pvp or ai
    self.running = True
    self.show_lines()


  def make_move(self,row,col):
    self.board.marked_sqr(row,col,self.player)
    self.draw_fig(row,col)
    self.next_turn()




  def show_lines(self):
    # bg color
    screen.fill(bg_color)


    #vertival Lines
    pygame.draw.line(screen,line_color,(sqsize,0),(sqsize,height),line_width)
    pygame.draw.line(screen,line_color,(width - sqsize,0),(width - sqsize,height),line_width)


    #horizontal Lines
    pygame.draw.line(screen,line_color,(0,sqsize),(width,sqsize),line_width)
    pygame.draw.line(screen,line_color,(0,height-sqsize),(width,height-sqsize),line_width)





  def draw_fig(self,row,col):
    # Draw the figure on the board
    if self.player == 1:
        #Draw Cross
        start_desc = (col*sqsize+offset,row*sqsize+offset)
        end_desc = (col*sqsize+sqsize-offset,row*sqsize+sqsize-offset)
        start_asc = (col*sqsize+offset,row*sqsize+sqsize-offset)
        end_asc = (col*sqsize+sqsize-offset,row*sqsize+offset)
        pygame.draw.line(screen,cross_col,start_desc,end_desc, cross_width)
        pygame.draw.line(screen,cross_col,start_asc,end_asc, cross_width)

    elif self.player == 2 :
        #Draw Circle
        center = (col*sqsize+sqsize//2,row*sqsize+sqsize//2)
        pygame.draw.circle(screen,cir_color,center,radius,cir_width)



  def next_turn(self):
    self.player = self.player %2 +1




  def change_gamemode(self):
    self.gamemode='pvp' if self.gamemode == 'ai' else 'pvp'


  def reset(self):
    self.__init__()


  def isover(self):
    return self.board.final_state(show=True) != 0 or self.board.isfull()


  def game_over(self):
    self.running = False


def main():

  #object
  game = Game()
  board = game.board
  ai = game.ai




  # Mainloop

  print("Hello Everyone, Here are the keybinds which will be use for reseting and changing the game mode: ")
  print("R: Reset the game")
  print("G: Change the game mode to PVP")
  print("0: Change the game mode to AI level 0")
  print("1: Change the game mode to AI level 1")
  while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
          pygame.quit()
          sys.exit()


        if event.type == pygame.KEYDOWN:

          #g-gamemode

          if event.key == pygame.K_g:
            game.change_gamemode()


          # r- Restart
          if event.key == pygame.K_r:
            game.reset()
            board = game.board
            ai = game.ai

          #0-gamemode ai

          if event.key == pygame.K_0:
            ai.level = 0

          #1-gamemode ai
          if event.key == pygame.K_1:
            ai.level = 1

        if event.type == pygame.MOUSEBUTTONDOWN:
          pos = event.pos
          row = int(pos[1]//sqsize)
          col = int(pos[0] // sqsize)
          if game.board.empty_sqr(row,col) and game.running:
              game.make_move(row,col)
          if game.isover():
              game.game_over()







    if game.gamemode == 'ai' and game.player == ai.player and game.running:
      #Update the screen
      pygame.display.update()
      #AI's Turn
      row,col = ai.eval(board)
      game.make_move(row,col)  # Corrected here
      if game.isover():
          game.game_over()



    pygame.display.update()



main()