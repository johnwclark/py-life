

from tkinter import Tk, Frame, Button, Label

import threading

class Application(Frame):
    def __init__(self,master):
        Frame.__init__(self)
        self.black = True
        self.grey = False
        self.master = master
        self.width = 29
        self.height = 20
        self.make_buttons()
        self.make_board()

    def make_board(self):
        self.board = [ [None]*self.width for _ in range(self.height) ]
        self.neighbors = [ [None]*self.width for _ in range(self.height) ]
        self.buttonArray = [ [None]*self.width for _ in range(self.height) ]
        for i,row in enumerate(self.board):
            for j,column in enumerate(row):
               self.board[i][j] = self.grey
               self.neighbors[i][j] = 0
               self.L = Button(self.master ,text='    ',bg='grey')
               self.buttonArray[i][j] = self.L
               self.L.grid(row=i,column=j)
               self.L.bind('<Button-1>',lambda e,i=i,j=j: self.on_grid_click(i,j,e))

    def make_buttons(self):
        self.play = False
        self.play_pause = Button(self.master)
        self.play_pause["text"] = "Play"
        self.play_pause["command"] = self.push_play
        self.play_pause.grid(row=self.height,column=0, columnspan=3 )
        self.quit = Button(self.master, text="QUIT", fg="red", command=self.push_close)
        self.quit.grid(row=self.height,column=(self.width-4), columnspan=3 )

    def on_grid_click(self,i,j,event):
        if self.board[i][j] == False :
            self.board[i][j] = True
            self.buttonArray[i][j]["bg"] = "black"
        else:
            self.board[i][j] = False
            self.buttonArray[i][j]["bg"] = "grey"

    def push_play(self):
        # toggle state
        if self.play == True:
            self.play = False
            self.play_pause["text"] = "Play"
            self.timer.cancel()
        else:
            self.play = True
            self.play_pause["text"] = "Pause"
            self.timer = threading.Timer(1, self.advance_time )
            self.timer.start()
    
    def push_close( self ):
            self.timer.cancel()
            self.destroy()
            self.master.destroy()
    
    def check_neighbor ( self, i, j ):
        rval = 0
        if i >= 0 and i < self.height and j >= 0 and j < self.width and self.board[i][j] == self.black :
            rval = 1
        return rval

    def count_neighbors ( self, i, j ):
        rval = 0
        offset_arr = [ (-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1) ]
        for x in offset_arr :
            rval += self.check_neighbor( ( i + x[0] ), ( j + x[1] ) )
            #print ( x , " --- ", x[0] , " : ", x[1] )
        return rval

    def advance_time( self ):
        self.timer = threading.Timer(1, self.advance_time )
        self.timer.start()

        # capture the neighbor counts before we modify the board
        for i,row in enumerate(self.board):
            for j,column in enumerate(row):
                self.neighbors[i][j] = self.count_neighbors( i,j )

        # update the board using the rules of life
        for i,row in enumerate(self.board):
            for j,column in enumerate(row):
                if self.board[i][j] == self.black and self.neighbors[i][j] < 2 :
                    self.board[i][j] = self.grey
                    self.buttonArray[i][j]["bg"] = "grey"
                elif self.board[i][j] == self.black and self.neighbors[i][j] > 3 :
                    self.board[i][j] = self.grey
                    self.buttonArray[i][j]["bg"] = "grey"
                elif self.board[i][j] == self.grey and self.neighbors[i][j] == 3 :
                    self.board[i][j] = self.black
                    self.buttonArray[i][j]["bg"] = "black"


'''
https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life


Any live cell with fewer than two live neighbours dies
Any live cell with two or three live neighbours lives
Any live cell with more than three live neighbours dies
Any dead cell with exactly three live neighbours becomes a live cell

'''


def main():
    root = Tk()
    root.title("Conway's Game of Life")
    app = Application(master=root)
    app.mainloop()

if __name__ == '__main__':
    main()

