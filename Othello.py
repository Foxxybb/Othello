# Caleb Richardson
# First build finished on: 11/2/2021
# Updated Heuristic on: 10/4/2023
# Othello against AI

import copy
import threading
import tkinter as tk

class Board:
    def __init__(self, main, AI):
        # mainGame is the game board that is represented by the GUI, other boards are used in the minimax tree
        self.mainGame = main
        self.AIGame = AI  # if true, player 2 is controlled by AI
        self.player = 1  # player 1 (black) goes first
        self.otherPlayer = 2 # player 2 (white) goes first
        self.moveList = []  # to hold all found moves
        self.chosenMove = (0, 0)
        self.gameover = False  # used to determine if game has ended
        self.oneScore = 0  # player 1 score
        self.twoScore = 0  # player 2 score
        self.turnCount = 0
        self.Hscore = 0  # Heuristic value used to determine which move AI chooses
        self.treeDepth = 4  # used to determine how deep the minimax tree AI uses to make a move
        self.debug = False  # if true, all possible game boards in minimax tree are printed to console
        
        self.grid = []  # game board matrix
        for x in range(8):
            self.grid.append([0, 0, 0, 0, 0, 0, 0, 0])  # empty board
        # 0s are empty spaces
        # 1s are black
        # 2s are white
        # starting pieces V
        self.grid[3][3] = 2
        self.grid[3][4] = 1
        self.grid[4][3] = 1
        self.grid[4][4] = 2
        
        self.event = threading.Event()  # for pauses
        
        # setup GUI
        if self.mainGame == True:  # only main game has GUI board
            self.window = tk.Tk()
            self.window.title('Othello')
            self.window.geometry("800x800")
            self.window.resizable(0,0)
            self.window.configure(bg='green')
            
            self.startButton=tk.Button(text="Start", command=self.takeTurn)
            self.startButton.place(x=10, y=750)

            self.depthButton=tk.Button(text="Depth: 4", command=self.toggleDepth)
            self.depthButton.place(x=300, y=750)
            
            # self.pruneButton=tk.Button(text="Prune: Off", command=self.togglePrune)
            # self.pruneButton.place(x=450, y=750)
            
            self.debugButton=tk.Button(text="Debug: Off", command=self.toggleDebug)
            self.debugButton.place(x=650, y=750)

            self.blackScoreLabel = tk.Label(text="Black Score: ")
            self.blackScoreLabel.place(x=600, y=300)

            self.whiteScoreLabel = tk.Label(text="White Score: ")
            self.whiteScoreLabel.place(x=600, y=400)
            
            self.turnLabel = tk.Label(text="PRESS START TO PLAY")
            self.turnLabel.place(x=350, y=600)
            
            self.b1=tk.Button(text="",height=4,width=8,bg="green",activebackground="grey",fg="white",command=lambda: self.insertMove(0,0))
            self.b1.grid(row=0,column=0)
            self.b2=tk.Button(text="",height=4,width=8,bg="green",activebackground="grey",fg="white",command=lambda: self.insertMove(0,1))
            self.b2.grid(row=0,column=1)
            self.b3=tk.Button(text="",height=4,width=8,bg="green",activebackground="grey",fg="white",command=lambda: self.insertMove(0,2))
            self.b3.grid(row=0,column=2)
            self.b4=tk.Button(text="",height=4,width=8,bg="green",activebackground="grey",fg="white",command=lambda: self.insertMove(0,3))
            self.b4.grid(row=0,column=3)
            self.b5=tk.Button(text="",height=4,width=8,bg="green",activebackground="grey",fg="white",command=lambda: self.insertMove(0,4))
            self.b5.grid(row=0,column=4)
            self.b6=tk.Button(text="",height=4,width=8,bg="green",activebackground="grey",fg="white",command=lambda: self.insertMove(0,5))
            self.b6.grid(row=0,column=5)
            self.b7=tk.Button(text="",height=4,width=8,bg="green",activebackground="grey",fg="white",command=lambda: self.insertMove(0,6))
            self.b7.grid(row=0,column=6)
            self.b8=tk.Button(text="",height=4,width=8,bg="green",activebackground="grey",fg="white",command=lambda: self.insertMove(0,7))
            self.b8.grid(row=0,column=7)

            self.b9=tk.Button(text="",height=4,width=8,bg="green",activebackground="grey",fg="white",command=lambda: self.insertMove(1,0))
            self.b9.grid(row=1,column=0)
            self.b10=tk.Button(text="",height=4,width=8,bg="green",activebackground="grey",fg="white",command=lambda: self.insertMove(1,1))
            self.b10.grid(row=1,column=1)
            self.b11=tk.Button(text="",height=4,width=8,bg="green",activebackground="grey",fg="white",command=lambda: self.insertMove(1,2))
            self.b11.grid(row=1,column=2)
            self.b12=tk.Button(text="",height=4,width=8,bg="green",activebackground="grey",fg="white",command=lambda: self.insertMove(1,3))
            self.b12.grid(row=1,column=3)
            self.b13=tk.Button(text="",height=4,width=8,bg="green",activebackground="grey",fg="white",command=lambda: self.insertMove(1,4))
            self.b13.grid(row=1,column=4)
            self.b14=tk.Button(text="",height=4,width=8,bg="green",activebackground="grey",fg="white",command=lambda: self.insertMove(1,5))
            self.b14.grid(row=1,column=5)
            self.b15=tk.Button(text="",height=4,width=8,bg="green",activebackground="grey",fg="white",command=lambda: self.insertMove(1,6))
            self.b15.grid(row=1,column=6)
            self.b16=tk.Button(text="",height=4,width=8,bg="green",activebackground="grey",fg="white",command=lambda: self.insertMove(1,7))
            self.b16.grid(row=1,column=7)

            self.b17=tk.Button(text="",height=4,width=8,bg="green",activebackground="grey",fg="white",command=lambda: self.insertMove(2,0))
            self.b17.grid(row=2,column=0)
            self.b18=tk.Button(text="",height=4,width=8,bg="green",activebackground="grey",fg="white",command=lambda: self.insertMove(2,1))
            self.b18.grid(row=2,column=1)
            self.b19=tk.Button(text="",height=4,width=8,bg="green",activebackground="grey",fg="white",command=lambda: self.insertMove(2,2))
            self.b19.grid(row=2,column=2)
            self.b20=tk.Button(text="",height=4,width=8,bg="green",activebackground="grey",fg="white",command=lambda: self.insertMove(2,3))
            self.b20.grid(row=2,column=3)
            self.b21=tk.Button(text="",height=4,width=8,bg="green",activebackground="grey",fg="white",command=lambda: self.insertMove(2,4))
            self.b21.grid(row=2,column=4)
            self.b22=tk.Button(text="",height=4,width=8,bg="green",activebackground="grey",fg="white",command=lambda: self.insertMove(2,5))
            self.b22.grid(row=2,column=5)
            self.b23=tk.Button(text="",height=4,width=8,bg="green",activebackground="grey",fg="white",command=lambda: self.insertMove(2,6))
            self.b23.grid(row=2,column=6)
            self.b24=tk.Button(text="",height=4,width=8,bg="green",activebackground="grey",fg="white",command=lambda: self.insertMove(2,7))
            self.b24.grid(row=2,column=7)

            self.b25=tk.Button(text="",height=4,width=8,bg="green",activebackground="grey",fg="white",command=lambda: self.insertMove(3,0))
            self.b25.grid(row=3,column=0)
            self.b26=tk.Button(text="",height=4,width=8,bg="green",activebackground="grey",fg="white",command=lambda: self.insertMove(3,1))
            self.b26.grid(row=3,column=1)
            self.b27=tk.Button(text="",height=4,width=8,bg="green",activebackground="grey",fg="white",command=lambda: self.insertMove(3,2))
            self.b27.grid(row=3,column=2)
            self.b28=tk.Button(text="",height=4,width=8,bg="green",activebackground="grey",fg="white",command=lambda: self.insertMove(3,3))
            self.b28.grid(row=3,column=3)
            self.b29=tk.Button(text="",height=4,width=8,bg="green",activebackground="grey",fg="white",command=lambda: self.insertMove(3,4))
            self.b29.grid(row=3,column=4)
            self.b30=tk.Button(text="",height=4,width=8,bg="green",activebackground="grey",fg="white",command=lambda: self.insertMove(3,5))
            self.b30.grid(row=3,column=5)
            self.b31=tk.Button(text="",height=4,width=8,bg="green",activebackground="grey",fg="white",command=lambda: self.insertMove(3,6))
            self.b31.grid(row=3,column=6)
            self.b32=tk.Button(text="",height=4,width=8,bg="green",activebackground="grey",fg="white",command=lambda: self.insertMove(3,7))
            self.b32.grid(row=3,column=7)

            self.b33=tk.Button(text="",height=4,width=8,bg="green",activebackground="grey",fg="white",command=lambda: self.insertMove(4,0))
            self.b33.grid(row=4,column=0)
            self.b34=tk.Button(text="",height=4,width=8,bg="green",activebackground="grey",fg="white",command=lambda: self.insertMove(4,1))
            self.b34.grid(row=4,column=1)
            self.b35=tk.Button(text="",height=4,width=8,bg="green",activebackground="grey",fg="white",command=lambda: self.insertMove(4,2))
            self.b35.grid(row=4,column=2)
            self.b36=tk.Button(text="",height=4,width=8,bg="green",activebackground="grey",fg="white",command=lambda: self.insertMove(4,3))
            self.b36.grid(row=4,column=3)
            self.b37=tk.Button(text="",height=4,width=8,bg="green",activebackground="grey",fg="white",command=lambda: self.insertMove(4,4))
            self.b37.grid(row=4,column=4)
            self.b38=tk.Button(text="",height=4,width=8,bg="green",activebackground="grey",fg="white",command=lambda: self.insertMove(4,5))
            self.b38.grid(row=4,column=5)
            self.b39=tk.Button(text="",height=4,width=8,bg="green",activebackground="grey",fg="white",command=lambda: self.insertMove(4,6))
            self.b39.grid(row=4,column=6)
            self.b40=tk.Button(text="",height=4,width=8,bg="green",activebackground="grey",fg="white",command=lambda: self.insertMove(4,7))
            self.b40.grid(row=4,column=7)

            self.b41=tk.Button(text="",height=4,width=8,bg="green",activebackground="grey",fg="white",command=lambda: self.insertMove(5,0))
            self.b41.grid(row=5,column=0)
            self.b42=tk.Button(text="",height=4,width=8,bg="green",activebackground="grey",fg="white",command=lambda: self.insertMove(5,1))
            self.b42.grid(row=5,column=1)
            self.b43=tk.Button(text="",height=4,width=8,bg="green",activebackground="grey",fg="white",command=lambda: self.insertMove(5,2))
            self.b43.grid(row=5,column=2)
            self.b44=tk.Button(text="",height=4,width=8,bg="green",activebackground="grey",fg="white",command=lambda: self.insertMove(5,3))
            self.b44.grid(row=5,column=3)
            self.b45=tk.Button(text="",height=4,width=8,bg="green",activebackground="grey",fg="white",command=lambda: self.insertMove(5,4))
            self.b45.grid(row=5,column=4)
            self.b46=tk.Button(text="",height=4,width=8,bg="green",activebackground="grey",fg="white",command=lambda: self.insertMove(5,5))
            self.b46.grid(row=5,column=5)
            self.b47=tk.Button(text="",height=4,width=8,bg="green",activebackground="grey",fg="white",command=lambda: self.insertMove(5,6))
            self.b47.grid(row=5,column=6)
            self.b48=tk.Button(text="",height=4,width=8,bg="green",activebackground="grey",fg="white",command=lambda: self.insertMove(5,7))
            self.b48.grid(row=5,column=7)

            self.b49=tk.Button(text="",height=4,width=8,bg="green",activebackground="grey",fg="white",command=lambda: self.insertMove(6,0))
            self.b49.grid(row=6,column=0)
            self.b50=tk.Button(text="",height=4,width=8,bg="green",activebackground="grey",fg="white",command=lambda: self.insertMove(6,1))
            self.b50.grid(row=6,column=1)
            self.b51=tk.Button(text="",height=4,width=8,bg="green",activebackground="grey",fg="white",command=lambda: self.insertMove(6,2))
            self.b51.grid(row=6,column=2)
            self.b52=tk.Button(text="",height=4,width=8,bg="green",activebackground="grey",fg="white",command=lambda: self.insertMove(6,3))
            self.b52.grid(row=6,column=3)
            self.b53=tk.Button(text="",height=4,width=8,bg="green",activebackground="grey",fg="white",command=lambda: self.insertMove(6,4))
            self.b53.grid(row=6,column=4)
            self.b54=tk.Button(text="",height=4,width=8,bg="green",activebackground="grey",fg="white",command=lambda: self.insertMove(6,5))
            self.b54.grid(row=6,column=5)
            self.b55=tk.Button(text="",height=4,width=8,bg="green",activebackground="grey",fg="white",command=lambda: self.insertMove(6,6))
            self.b55.grid(row=6,column=6)
            self.b56=tk.Button(text="",height=4,width=8,bg="green",activebackground="grey",fg="white",command=lambda: self.insertMove(6,7))
            self.b56.grid(row=6,column=7)

            self.b57=tk.Button(text="",height=4,width=8,bg="green",activebackground="grey",fg="white",command=lambda: self.insertMove(7,0))
            self.b57.grid(row=7,column=0)
            self.b58=tk.Button(text="",height=4,width=8,bg="green",activebackground="grey",fg="white",command=lambda: self.insertMove(7,1))
            self.b58.grid(row=7,column=1)
            self.b59=tk.Button(text="",height=4,width=8,bg="green",activebackground="grey",fg="white",command=lambda: self.insertMove(7,2))
            self.b59.grid(row=7,column=2)
            self.b60=tk.Button(text="",height=4,width=8,bg="green",activebackground="grey",fg="white",command=lambda: self.insertMove(7,3))
            self.b60.grid(row=7,column=3)
            self.b61=tk.Button(text="",height=4,width=8,bg="green",activebackground="grey",fg="white",command=lambda: self.insertMove(7,4))
            self.b61.grid(row=7,column=4)
            self.b62=tk.Button(text="",height=4,width=8,bg="green",activebackground="grey",fg="white",command=lambda: self.insertMove(7,5))
            self.b62.grid(row=7,column=5)
            self.b63=tk.Button(text="",height=4,width=8,bg="green",activebackground="grey",fg="white",command=lambda: self.insertMove(7,6))
            self.b63.grid(row=7,column=6)
            self.b64=tk.Button(text="",height=4,width=8,bg="green",activebackground="grey",fg="white",command=lambda: self.insertMove(7,7))
            self.b64.grid(row=7,column=7)
            
            self.buttonList = {} # matrix
            
            self.buttonList[0,0] = self.b1
            self.buttonList[0,1] = self.b2
            self.buttonList[0,2] = self.b3
            self.buttonList[0,3] = self.b4
            self.buttonList[0,4] = self.b5
            self.buttonList[0,5] = self.b6
            self.buttonList[0,6] = self.b7
            self.buttonList[0,7] = self.b8
            
            self.buttonList[1,0] = self.b9
            self.buttonList[1,1] = self.b10
            self.buttonList[1,2] = self.b11
            self.buttonList[1,3] = self.b12
            self.buttonList[1,4] = self.b13
            self.buttonList[1,5] = self.b14
            self.buttonList[1,6] = self.b15
            self.buttonList[1,7] = self.b16
            
            self.buttonList[2,0] = self.b17
            self.buttonList[2,1] = self.b18
            self.buttonList[2,2] = self.b19
            self.buttonList[2,3] = self.b20
            self.buttonList[2,4] = self.b21
            self.buttonList[2,5] = self.b22
            self.buttonList[2,6] = self.b23
            self.buttonList[2,7] = self.b24
            
            self.buttonList[3,0] = self.b25
            self.buttonList[3,1] = self.b26
            self.buttonList[3,2] = self.b27
            self.buttonList[3,3] = self.b28
            self.buttonList[3,4] = self.b29
            self.buttonList[3,5] = self.b30
            self.buttonList[3,6] = self.b31
            self.buttonList[3,7] = self.b32
            
            self.buttonList[4,0] = self.b33
            self.buttonList[4,1] = self.b34
            self.buttonList[4,2] = self.b35
            self.buttonList[4,3] = self.b36
            self.buttonList[4,4] = self.b37
            self.buttonList[4,5] = self.b38
            self.buttonList[4,6] = self.b39
            self.buttonList[4,7] = self.b40
            
            self.buttonList[5,0] = self.b41
            self.buttonList[5,1] = self.b42
            self.buttonList[5,2] = self.b43
            self.buttonList[5,3] = self.b44
            self.buttonList[5,4] = self.b45
            self.buttonList[5,5] = self.b46
            self.buttonList[5,6] = self.b47
            self.buttonList[5,7] = self.b48
            
            self.buttonList[6,0] = self.b49
            self.buttonList[6,1] = self.b50
            self.buttonList[6,2] = self.b51
            self.buttonList[6,3] = self.b52
            self.buttonList[6,4] = self.b53
            self.buttonList[6,5] = self.b54
            self.buttonList[6,6] = self.b55
            self.buttonList[6,7] = self.b56
            
            self.buttonList[7,0] = self.b57
            self.buttonList[7,1] = self.b58
            self.buttonList[7,2] = self.b59
            self.buttonList[7,3] = self.b60
            self.buttonList[7,4] = self.b61
            self.buttonList[7,5] = self.b62
            self.buttonList[7,6] = self.b63
            self.buttonList[7,7] = self.b64
            
    def updateButtons(self):  # update GUI
        # take main game info and update colors and functions on each button
        if self.mainGame == True:
            for x in range(8):
                for y in range(8):
                    if self.grid[x][y] == 0:
                        self.buttonList[x, y].config(bg='green')
                    elif self.grid[x][y] == 1:
                        self.buttonList[x, y].config(bg='black')
                    elif self.grid[x][y] == 2:
                        self.buttonList[x, y].config(bg='white')
            # set grey buttons with moveList
            for moveRow, moveCol in self.moveList:
                self.buttonList[moveRow, moveCol].config(bg='grey')
                 
    def toggleDepth(self):  # function for depth toggle button
        if self.treeDepth == 2:
            self.depthButton['text'] = 'Depth: 4'
            self.treeDepth = 4
        elif self.treeDepth == 4:
            self.depthButton['text'] = 'Depth: 6'
            self.treeDepth = 6
        elif self.treeDepth == 6:
            self.depthButton['text'] = 'Depth: 2'
            self.treeDepth = 2
    
    def togglePrune(self):  # function for depth prune button
        if myAI.pruningEnabled == False:
            myAI.pruningEnabled = True
            self.pruneButton['text'] = 'Prune: On'
        elif myAI.pruningEnabled == True:
            myAI.pruningEnabled = False
            self.pruneButton['text'] = 'Prune: Off'
    
    def toggleDebug(self):
        if self.debug == False:
            self.debug = True
            self.debugButton['text'] = 'Debug: On'
        elif self.debug == True:
            self.debug = False
            self.debugButton['text'] = 'Debug: Off'

    def moveCheck(self, row, col): # function to find possible moves from piece
        
        # check adjacent pieces
        # check top piece : (row-1) , (col)
        if (row-1) >= 0:
            if (self.grid[row-1][col] == self.otherPlayer):
                nextRow = row-1
                nextCol = col
                # while still in board range
                while (nextRow >= 0):
                    # another otherPlayer piece found
                    if (self.grid[nextRow][nextCol] == self.otherPlayer):
                        nextRow -= 1
                    # player piece found
                    elif (self.grid[nextRow][nextCol] == self.player):
                        break
                    # empty space found
                    elif (self.grid[nextRow][nextCol] == 0):
                        if (nextRow,nextCol) not in self.moveList:
                            self.moveList.append((nextRow,nextCol))
                            #self.grid[nextRow][nextCol] = 3
                        break
        
        # check bottom piece : (row+1) , (col)
        if (row+1) <= 7:
            if (self.grid[row+1][col] == self.otherPlayer):
                nextRow = row+1
                nextCol = col
                # while still in board range
                while (nextRow <= 7):
                    # another otherPlayer piece found
                    if (self.grid[nextRow][nextCol] == self.otherPlayer):
                        nextRow += 1
                    # player piece found
                    elif (self.grid[nextRow][nextCol] == self.player):
                        break
                    # empty space found
                    elif (self.grid[nextRow][nextCol] == 0):
                        if (nextRow,nextCol) not in self.moveList:
                            self.moveList.append((nextRow,nextCol))
                            #self.grid[nextRow][nextCol] = 3
                        break
        
        # check left piece : (row) , (col-1)
        if (col-1) >= 0:
            if (self.grid[row][col-1] == self.otherPlayer):
                nextRow = row
                nextCol = col-1
                # while still in board range
                while (nextCol >= 0):
                    # another otherPlayer piece found
                    if (self.grid[nextRow][nextCol] == self.otherPlayer):
                        nextCol -= 1
                    # player piece found
                    elif (self.grid[nextRow][nextCol] == self.player):
                        break
                    # empty space found
                    elif (self.grid[nextRow][nextCol] == 0):
                        if (nextRow,nextCol) not in self.moveList:
                            self.moveList.append((nextRow,nextCol))
                            #self.grid[nextRow][nextCol] = 3
                        break
        
        # check right piece : (row) , (col+1)
        if (col+1) <= 7:
            if (self.grid[row][col+1] == self.otherPlayer):
                nextRow = row
                nextCol = col+1
                # while still in board range
                while (nextCol <= 7):
                    # another otherPlayer piece found
                    if (self.grid[nextRow][nextCol] == self.otherPlayer):
                        nextCol += 1
                    # player piece found
                    elif (self.grid[nextRow][nextCol] == self.player):
                        break
                    # empty space found
                    elif (self.grid[nextRow][nextCol] == 0):
                        if (nextRow,nextCol) not in self.moveList:
                            self.moveList.append((nextRow,nextCol))
                            #self.grid[nextRow][nextCol] = 3
                        break
        
        # check top-left piece : (row-1) , (col-1)
        if ((row-1) >= 0) and ((col-1) >= 0):
            if (self.grid[row-1][col-1] == self.otherPlayer):
                nextRow = row-1
                nextCol = col-1
                # while still in board range
                while (nextRow >= 0) and (nextCol >= 0):
                    # another otherPlayer piece found
                    if (self.grid[nextRow][nextCol] == self.otherPlayer):
                        nextRow -= 1
                        nextCol -= 1
                    # player piece found
                    elif (self.grid[nextRow][nextCol] == self.player):
                        break
                    # empty space found
                    elif (self.grid[nextRow][nextCol] == 0):
                        if (nextRow,nextCol) not in self.moveList:
                            self.moveList.append((nextRow,nextCol))
                            #self.grid[nextRow][nextCol] = 3
                        break
        
        # check top-right piece : (row-1) , (col+1)
        if ((row-1) >= 0) and ((col+1) <= 7):
            if (self.grid[row-1][col+1] == self.otherPlayer):
                nextRow = row-1
                nextCol = col+1
                # while still in board range
                while (nextRow >= 0) and (nextCol <= 7):
                    # another otherPlayer piece found
                    if (self.grid[nextRow][nextCol] == self.otherPlayer):
                        nextRow -= 1
                        nextCol += 1
                    # player piece found
                    elif (self.grid[nextRow][nextCol] == self.player):
                        break
                    # empty space found
                    elif (self.grid[nextRow][nextCol] == 0):
                        if (nextRow,nextCol) not in self.moveList:
                            self.moveList.append((nextRow,nextCol))
                            #self.grid[nextRow][nextCol] = 3
                        break
        
        # check bot-left piece : (row+1) , (col-1)
        if ((row+1) <= 7) and ((col-1) >= 0):
            if (self.grid[row+1][col-1] == self.otherPlayer):
                nextRow = row+1
                nextCol = col-1
                # while still in board range
                while (nextRow <= 7) and (nextCol >= 0):
                    # another otherPlayer piece found
                    if (self.grid[nextRow][nextCol] == self.otherPlayer):
                        nextRow += 1
                        nextCol -= 1
                    # player piece found
                    elif (self.grid[nextRow][nextCol] == self.player):
                        break
                    # empty space found
                    elif (self.grid[nextRow][nextCol] == 0):
                        if (nextRow,nextCol) not in self.moveList:
                            self.moveList.append((nextRow,nextCol))
                            #self.grid[nextRow][nextCol] = 3
                        break
        
        # check bot-right piece : (row+1) , (col+1)
        if ((row+1) <= 7) and ((col+1) <= 7):
            if (self.grid[row+1][col+1] == self.otherPlayer):
                nextRow = row+1
                nextCol = col+1
                # while still in board range
                while (nextRow <= 7) and (nextCol <= 7):
                    # another otherPlayer piece found
                    if (self.grid[nextRow][nextCol] == self.otherPlayer):
                        nextRow += 1
                        nextCol += 1
                    # player piece found
                    elif (self.grid[nextRow][nextCol] == self.player):
                        break
                    # empty space found
                    elif (self.grid[nextRow][nextCol] == 0):
                        if (nextRow,nextCol) not in self.moveList:
                            self.moveList.append((nextRow,nextCol))
                            #self.grid[nextRow][nextCol] = 3
                        break

    def capturePieces(self, row, col):
        # check adjacent pieces
        # check top piece : (row-1) , (col)
        if (row-1) >= 0:
            if (self.grid[row-1][col] == self.otherPlayer):
                nextRow = row-1
                nextCol = col
                capList = [] # used to mark coords of capturable pieces
                # while still in board range
                while (nextRow >= 0):
                    # another otherPlayer piece found
                    if (self.grid[nextRow][nextCol] == self.otherPlayer):
                        # add to list of cappable pieces
                        capList.append((nextRow, nextCol))
                        nextRow -= 1
                    # player piece found
                    elif (self.grid[nextRow][nextCol] == self.player):
                        # capture pieces
                        for (rowC,colC) in capList:
                            self.grid[rowC][colC] = self.player
                        break
                    # empty space found
                    elif (self.grid[nextRow][nextCol] == 0):
                        break

        # check bottom piece : (row+1) , (col)
        if (row+1) <= 7:
            if (self.grid[row+1][col] == self.otherPlayer):
                nextRow = row+1
                nextCol = col
                capList = [] # used to mark coords of capturable pieces
                # while still in board range
                while (nextRow <= 7):
                    # another otherPlayer piece found
                    if (self.grid[nextRow][nextCol] == self.otherPlayer):
                        capList.append((nextRow, nextCol))
                        nextRow += 1
                    # player piece found
                    elif (self.grid[nextRow][nextCol] == self.player):
                        # capture pieces
                        for (rowC,colC) in capList:
                            self.grid[rowC][colC] = self.player
                        break
                    # empty space found
                    elif (self.grid[nextRow][nextCol] == 0):
                        break

        # check left piece : (row) , (col-1)
        if (col-1) >= 0:
            if (self.grid[row][col-1] == self.otherPlayer):
                nextRow = row
                nextCol = col-1
                capList = [] # used to mark coords of capturable pieces
                # while still in board range
                while (nextCol >= 0):
                    # another otherPlayer piece found
                    if (self.grid[nextRow][nextCol] == self.otherPlayer):
                        capList.append((nextRow, nextCol))
                        nextCol -= 1
                    # player piece found
                    elif (self.grid[nextRow][nextCol] == self.player):
                        for (rowC,colC) in capList:
                            self.grid[rowC][colC] = self.player
                        break
                    # empty space found
                    elif (self.grid[nextRow][nextCol] == 0):
                        break

        # check right piece : (row) , (col+1)
        if (col+1) <= 7:
            if (self.grid[row][col+1] == self.otherPlayer):
                nextRow = row
                nextCol = col+1
                capList = [] # used to mark coords of capturable pieces
                # while still in board range
                while (nextCol <= 7):
                    # another otherPlayer piece found
                    if (self.grid[nextRow][nextCol] == self.otherPlayer):
                        capList.append((nextRow, nextCol))
                        nextCol += 1
                    # player piece found
                    elif (self.grid[nextRow][nextCol] == self.player):
                        # capture pieces
                        for (rowC,colC) in capList:
                            self.grid[rowC][colC] = self.player
                        break
                    # empty space found
                    elif (self.grid[nextRow][nextCol] == 0):
                        break

        # check top-left piece : (row-1) , (col-1)
        if ((row-1) >= 0) and ((col-1) >= 0):
            if (self.grid[row-1][col-1] == self.otherPlayer):
                nextRow = row-1
                nextCol = col-1
                capList = [] # used to mark coords of capturable pieces
                # while still in board range
                while (nextRow >= 0) and (nextCol >= 0):
                    # another otherPlayer piece found
                    if (self.grid[nextRow][nextCol] == self.otherPlayer):
                        capList.append((nextRow, nextCol))
                        nextRow -= 1
                        nextCol -= 1
                    # player piece found
                    elif (self.grid[nextRow][nextCol] == self.player):
                        # capture pieces
                        for (rowC,colC) in capList:
                            self.grid[rowC][colC] = self.player
                        break
                    # empty space found
                    elif (self.grid[nextRow][nextCol] == 0):
                        break

        # check top-right piece : (row-1) , (col+1)
        if ((row-1) >= 0) and ((col+1) <= 7):
            if (self.grid[row-1][col+1] == self.otherPlayer):
                nextRow = row-1
                nextCol = col+1
                capList = [] # used to mark coords of capturable pieces
                # while still in board range
                while (nextRow >= 0) and (nextCol <= 7):
                    # another otherPlayer piece found
                    if (self.grid[nextRow][nextCol] == self.otherPlayer):
                        capList.append((nextRow, nextCol))
                        nextRow -= 1
                        nextCol += 1
                    # player piece found
                    elif (self.grid[nextRow][nextCol] == self.player):
                        # capture pieces
                        for (rowC,colC) in capList:
                            self.grid[rowC][colC] = self.player
                        break
                    # empty space found
                    elif (self.grid[nextRow][nextCol] == 0):
                        break

        # check bot-left piece : (row+1) , (col-1)
        if ((row+1) <= 7) and ((col-1) >= 0):
            if (self.grid[row+1][col-1] == self.otherPlayer):
                nextRow = row+1
                nextCol = col-1
                capList = [] # used to mark coords of capturable pieces
                # while still in board range
                while (nextRow <= 7) and (nextCol >= 0):
                    # another otherPlayer piece found
                    if (self.grid[nextRow][nextCol] == self.otherPlayer):
                        capList.append((nextRow, nextCol))
                        nextRow += 1
                        nextCol -= 1
                    # player piece found
                    elif (self.grid[nextRow][nextCol] == self.player):
                        # capture pieces
                        for (rowC,colC) in capList:
                            self.grid[rowC][colC] = self.player
                        break
                    # empty space found
                    elif (self.grid[nextRow][nextCol] == 0):
                        break

        # check bot-right piece : (row+1) , (col+1)
        if ((row+1) <= 7) and ((col+1) <= 7):
            if (self.grid[row+1][col+1] == self.otherPlayer):
                nextRow = row+1
                nextCol = col+1
                capList = [] # used to mark coords of capturable pieces
                # while still in board range
                while (nextRow <= 7) and (nextCol <= 7):
                    # another otherPlayer piece found
                    if (self.grid[nextRow][nextCol] == self.otherPlayer):
                        capList.append((nextRow, nextCol))
                        nextRow += 1
                        nextCol += 1
                    # player piece found
                    elif (self.grid[nextRow][nextCol] == self.player):
                        # capture pieces
                        for (rowC,colC) in capList:
                            self.grid[rowC][colC] = self.player
                        break
                    # empty space found
                    elif (self.grid[nextRow][nextCol] == 0):
                        break
       
    def makeMove(self):
        # need to reset 3s so moves are done correctly
        
        # if no valid moves, switch players
        if not self.moveList:
            print ("No valid moves, switching players")
            self.swapPlayers()
            self.displayMoves()
            if (self.AIGame == True) and (self.player == 2):
                self.AITurn()
            # if both players have no moves, end game
            if not self.moveList:
                print ("no moves for both players, ending game")
                self.gameover = True
                return
        
        
        #print(self.chosenMove) # chosenMove determined by button press or AI input
        moveRow = self.chosenMove[0]
        moveCol = self.chosenMove[1]
        # place piece
        self.grid[moveRow][moveCol] = self.player
        # capture pieces
        self.capturePieces(moveRow, moveCol)
        self.swapPlayers()
            
    def insertMove(self,row,col): # contains makeMove() and takeTurn() and triggers next turn loop
        # if button is pressed and is in move list, set to chosenMove
        if (row,col) in self.moveList:
            self.chosenMove = (row,col)
            #print("chosen move is " + str(self.chosenMove))
            # make move with chosenMove
            self.makeMove()
            self.takeTurn()
        
    def displayBoard(self):
        for x in range(8):
            print (str(x) + str(self.grid[x]))
    
    def displayMoves(self):
        
        pieces = [] # coords of current players pieces
        # reset movelist for current turn
        self.moveList = [] # coords of playable spaces
        
        # first find pieces of active player
        for row in range(8):
            # if piece is in row
            if self.player in self.grid[row]:
                #print ("found piece in " + str(row))
                for col in range(8):
                    # if piece is in col
                    if self.player == self.grid[row][col]:
                        #print ("found piece in " + str(row) + " " + str(col))
                        pieces.append((row,col))                
        #print ("pieces found in:")
        #print (pieces)
        for row,col in pieces:
            # implement moveCheck here
            self.moveCheck(row, col)
        if self.mainGame:
            print ("possible moves:")
            print (self.moveList)  

    def swapPlayers(self):
        if self.player == 1:
            self.player = 2
            self.otherPlayer = 1
        elif self.player == 2:
            self.player = 1
            self.otherPlayer = 2

    def getScore(self):  # handles score for GUI and H value for search
        oneScore = 0
        twoScore = 0
        
        for row in range(8):
            for col in range(8):
                if self.grid[row][col] == 1:
                    oneScore += 1
                elif self.grid[row][col] == 2:
                    twoScore += 1
        self.oneScore = oneScore
        self.twoScore = twoScore
        # IF main game board, update GUI
        if self.mainGame == True:
            # print ("Player 1 score: " + str(oneScore))
            mainGame.blackScoreLabel.config(text='Black Score: ' + str(oneScore))
            # print ("Player 2 score: " + str(twoScore))
            mainGame.whiteScoreLabel.config(text='White Score: ' + str(twoScore))
        
        # H VALUE CALCULATION
        # all captured spaces are 1
        # all captured spaces in center 4x4 are 2 - (row 2-5) through (col 2-5)
        # all captured spaces in corners are 3

        # get AI Hscore
        AIHscore = 0
        for rowH in range(8):
            for colH in range(8):
                # corners (+3)
                if (self.grid[rowH][colH] == 2) and ((rowH == 0 and colH == 0) or (rowH == 0 and colH == 7) or (rowH == 7 and colH == 0) or (rowH == 7 and colH == 7)):
                    # print ("added 3 to score at " + str(rowH) + str(colH))
                    AIHscore += 3
                # edges
                elif (self.grid[rowH][colH] == 2) and (rowH == 0 or rowH == 7 or colH == 0 or colH == 7):
                    AIHscore += 2
                # middle 4x4 (+2)
                elif (self.grid[rowH][colH] == 2) and (rowH in range(2, 6)) and (colH in range(2, 6)):
                    # print ("added 2 to score at " + str(rowH) + str(colH))
                    AIHscore += 2
                # all other spaces (+1)
                elif self.grid[rowH][colH] == 2:
                    # print ("added 1 to score at " + str(rowH) + str(colH))
                    AIHscore += 1

        # get human Hscore
        humanHscore = 0
        for rowH in range(8):
            for colH in range(8):
                # corners (+3)
                if (self.grid[rowH][colH] == 1) and ((rowH == 0 and colH == 0) or (rowH == 0 and colH == 7) or (rowH == 7 and colH == 0) or (rowH == 7 and colH == 7)):
                    # print ("added 3 to score at " + str(rowH) + str(colH))
                    humanHscore += 3
                # edges
                elif (self.grid[rowH][colH] == 1) and (rowH == 0 or rowH == 7 or colH == 0 or colH == 7):
                    humanHscore += 2
                # middle 4x4 (+2)
                elif (self.grid[rowH][colH] == 1) and (rowH in range(2, 6)) and (colH in range(2, 6)):
                    # print ("added 2 to score at " + str(rowH) + str(colH))
                    humanHscore += 2
                # all other spaces (+1)
                elif self.grid[rowH][colH] == 1:
                    # print ("added 1 to score at " + str(rowH) + str(colH))
                    humanHscore += 1

        # update board Hscore with difference
        self.Hscore = AIHscore - humanHscore
        # print("H value for current gamestate is: " + str(self.Hscore))

        # HSCORE UPDATE: calculate H score for both players and use difference

    def displayTurn(self): # handles turn announcement and gameover announcement
        if self.mainGame == True:
            if self.player == 1:
                print("It's Player 1's turn.")
                self.turnLabel.config(text='BLACK turn')
            elif self.player == 2:
                print("It's Player 2's turn.")
                self.turnLabel.config(text='WHITE turn')
            if not self.moveList:
                print("Game Over")
                if self.oneScore > self.twoScore:
                    self.turnLabel.config(text='BLACK WINS!!!')
                elif self.oneScore < self.twoScore:
                    self.turnLabel.config(text='WHITE WINS!!!')
                elif self.oneScore == self.twoScore:
                    self.turnLabel.config(text='DRAW GAME!!!')
                
    def emptyFunc(self):
        pass
    
    def takeTurn(self):  # take a turn
        if self.debug == True and self.mainGame == True:
            self.displayBoard()
        self.displayMoves()
        self.getScore()
        self.displayTurn()
        self.updateButtons()
        if self.mainGame == True:
            self.window.update()
        # insertMove from button press triggers next loop
        # if AI is player 2, trigger loop with calculated input automatically
        #print ("") # neat and tidy
        if (self.AIGame == True) and (self.player == 2):
            print("Thinking...")
            self.AITurn()
            
    def AITurn(self):
        # create root for minimax tree based on current mainGame state
        treeRootState = Board(False, False)  # makes a copy of main gamestate so main game isn't affected
        treeRootState.grid = copy.deepcopy(self.grid)  # update new board with current gameState
        treeRootState.moveList = copy.deepcopy(self.moveList)  # update new board with movelist
        treeRootState.player = copy.deepcopy(self.player)
        treeRootState.otherPlayer = copy.deepcopy(self.otherPlayer)
        
        # create tree to do miniMax search for most OPTIMAL move
        miniMaxTree = Tree(treeRootState, self.treeDepth)  # root of tree
        miniMaxTree.branchOut(0)  # 0 is starting depth
        
        aiMove = (0, 0)  # AI move to be chosen by search
        maxHScore = -1000  # used to compare with other branches in first layer to find best move
        eval = 0
        prunEval = 0  # flag for pruning
        
        if myAI.pruningEnabled == True:
            for child in miniMaxTree.children: # search for every layer 1 branch
                # -1 depth because search starts at layer 1 (alpha,beta)
                prunEval = myAI.miniMaxPrune(child, self.treeDepth - 1, -200, 200, False)
                
                if (prunEval[0] > maxHScore):
                    #print("passing on move: " + str(child.gameState.chosenMove))
                    aiMove = child.gameState.chosenMove
                    maxHScore = prunEval[0]  # starts with minimizing player on layer 1 (False)
                    
                if prunEval[2] >= prunEval[1]:  # if beta >= alpha
                    break
                    
        elif myAI.pruningEnabled == False:
            for child in miniMaxTree.children: # search for every layer 1 branch
                eval = myAI.miniMax(child, self.treeDepth - 1, False) # -1 depth because search starts at layer 1 (alpha,beta)
                print("Hscore: " + str(eval) + " for move " + str(child.gameState.chosenMove))
                if (eval > maxHScore):
                    # print("passing on move: " + str(child.gameState.chosenMove))
                    aiMove = child.gameState.chosenMove
                    maxHScore = eval  # starts with minimizing player on layer 1 (False)

        # print("Main Game State: ")
        print("AI move is: " + str(aiMove))
        self.insertMove(aiMove[0], aiMove[1])

class AI:
    def __init__(self, prune):
        # need to make toggle
        self.pruningEnabled = prune  # toggle for alpha/beta pruning
        # self.depth = 2 # depth of tree creation and search
        self.chosenMove = (0, 0)  # will result after calculation

    def miniMax(self, tree, depth, maximPlayer): # (mainGame.grid, layers of minMax 2-6?, true)
        # first call is different, need to run separate search for every tree in first layer after root
        if (depth == 0) or tree.gameState.gameover:
            # print("returning Hscore: " + str(tree.gameState.Hscore) + " and move: " + str(tree.gameState.chosenMove))
            return tree.gameState.Hscore
        if maximPlayer == True:
            maxEval = -200 
            for child in tree.children:
                eval = self.miniMax(child,depth-1,False)
                maxEval = max(eval, maxEval)
            return maxEval
        else:
            minEval = 200
            for child in tree.children:
                eval = self.miniMax(child,depth-1,True)
                minEval = min(eval,minEval)
            return minEval
        
    def miniMaxPrune(self, tree, depth, alpha, beta, maximPlayer): # (mainGame.grid, layers of minMax 2-6?, true)
        
        if (depth == 0) or tree.gameState.gameover:
            return tree.gameState.Hscore,alpha,beta # boolean for breaking outer loop "pruning"
        if maximPlayer == True:
            maxEval = -200
            for child in tree.children:
                eval = self.miniMaxPrune(child,depth-1,alpha,beta,False)
                maxEval = max(maxEval,eval[0])
                alpha = max(alpha,eval[0])
                #if beta <= alpha:
                #    break
            return maxEval,alpha,beta
        else:
            minEval = 200
            for child in tree.children:
                eval = self.miniMaxPrune(child,depth-1,alpha,beta,True)
                minEval = min(minEval,eval[0])
                beta = min(beta,eval[0])
                #if beta <= alpha:
                #    break
            return minEval,alpha,beta

class Tree:
    def __init__(self, gameState, maxDepth):
    
        self.children = []  # list of game boards
        self.gameState = gameState  # will probably be Board object
        self.maxDepth = maxDepth  # used to count layers to branch
        
    def branchOut(self, currentDepth):  # create children from gamestate using board functions
        if self.gameState.moveList:  # if there are possible moves
            if mainGame.debug == True:
                print("Branching movelist:")
                print(self.gameState.moveList)
            for move in self.gameState.moveList:  # create new tree for each possible move
                
                newGameState = Board(False, False) # new board to copy grid and movelist to
                newGameState.grid = copy.deepcopy(self.gameState.grid) # update new board with current gameState
                # need to add IF statement IF moveList is EMPTY to STOP BRANCH?
                newGameState.moveList = copy.deepcopy(self.gameState.moveList) # update new board with movelist
                newGameState.player = copy.deepcopy(self.gameState.player)
                newGameState.otherPlayer = copy.deepcopy(self.gameState.otherPlayer)
                # code to progress forward in gamestate
                # print("inserting move: " + str(move))
                newGameState.insertMove(move[0], move[1])
                
                # add new board to list of children
                treeToAdd = Tree(newGameState, self.maxDepth)  # new Tree with gamestate
                self.children.append(treeToAdd)  # add new tree to child list
                # print("Child added with H value of: " + str(treeToAdd.gameState.Hscore))
                  
        else:
            print("Tried to branch empty movelist ")
            
        newDepth = currentDepth + 1 
        #print ("depth is: " + str(newDepth))
        if newDepth != self.maxDepth:  # if depth is not met, loop branching for all children
            for child in self.children:  # branchout for each child
                child.branchOut(newDepth)
        
        else:
            # print("TREE LAYER COMPLETE")
            pass

# MAIN #########################

mainGame = Board(True,True) # (mainGame, AIgame)

myAI = AI(False)  # (prune)

mainGame.window.mainloop()

