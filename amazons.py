#!/usr/bin/env python3
# -*- coding: utf-8 -
__author__ = "Oliver Sick"

import sys
import random

class Amazons:
    
    empty_sq="·"
    block_sq="▒"
    w_amazon_sq="w"
    b_amazon_sq="b"

    def __init__(self, boardsize: int):
        self.boardsize=boardsize
        self.init_board()
        self.pieces={Amazons.b_amazon_sq:[],Amazons.w_amazon_sq:[]}
        self.active=Amazons.w_amazon_sq

        
    def init_board(self):
        self.board = list(range(self.boardsize+2))
        self.board[0]=["╔═"]
        for i in range((self.boardsize-1)): self.board[0].append("═")
        self.board[0].append("═╗")
        for k in range(self.boardsize):
            self.board[k+1]=["║"]
            for i in range((self.boardsize)): self.board[k+1].append(Amazons.empty_sq)
            self.board[k+1].append("║")
        self.board[self.boardsize+1]=["╚═"]
        for i in range((self.boardsize-1)): self.board[self.boardsize+1].append("═")
        self.board[self.boardsize+1].append("═╝")


    def set_amazon(self,x,y,color=""):
        self.clear_sq(x,y)
        if color=="b": 
            self.board[x][y]=Amazons.b_amazon_sq
            self.pieces[Amazons.b_amazon_sq].append(f"{x},{y}")
        if color=="w": 
            self.board[x][y]=Amazons.w_amazon_sq
            self.pieces[Amazons.w_amazon_sq].append(f"{x},{y}")
        if color=="":  
            self.board[x][y]=self.active
            self.pieces[self.active].append(f"{x},{y}")


    def clear_sq(self,x,y):
        if self.board[x][y]==Amazons.b_amazon_sq or self.board[x][y]==Amazons.w_amazon_sq:
            self.pieces.remove(self.pieces[self.board[x][y]].index(f"{x},{y}"))
        self.board[x][y]=Amazons.empty_sq


    def set_block(self,x,y):
        self.board[x][y]=Amazons.block_sq


    def get_moves(self,x,y):
        moves=[]
        moves.extend(self.iter_moves(x,y, 1, 0))    
        moves.extend(self.iter_moves(x,y, 1, 1))    
        moves.extend(self.iter_moves(x,y, 0, 1))
        moves.extend(self.iter_moves(x,y,-1, 1))
        moves.extend(self.iter_moves(x,y,-1, 0))
        moves.extend(self.iter_moves(x,y,-1,-1))
        moves.extend(self.iter_moves(x,y, 0,-1))
        moves.extend(self.iter_moves(x,y, 1,-1))
        return moves


    def iter_moves(self,x,y,dir_x,dir_y):
        itermoves=[]
        sq_from=f"{x},{y}"
        x+=dir_x
        y+=dir_y
        try:
            while self.board[x][y]==Amazons.empty_sq:
                itermoves.append(f"{sq_from}-{x},{y}")
                x+=dir_x
                y+=dir_y
        except: pass
        return itermoves


    def can_move(self,x,y):
        return self.board[x][y]==self.active


    def move(self,x_from,y_from,x_to,y_to,x_block,y_block):
        if self.get_moves(x_from,y_from).count(f"{x_from},{y_from}-{x_to},{y_to}")>0 and self.get_moves(x_to,y_to).count(f"{x_to},{y_to}-{x_block},{y_block}")>0 and self.can_move(x_from,y_from):
            self.clear_sq(x_from,y_from)
            self.set_amazon(x_to,y_to)
            self.set_block(x_block,y_block)
            self.active=Amazons.b_amazon_sq if self.active==Amazons.w_amazon_sq else Amazons.w_amazon_sq

    def print(self):
        print("═".join(self.board[0]))
        for i in range(self.boardsize,0,-1): print(" ".join(self.board[i]))
        print("═".join(self.board[self.boardsize+1]))

    def play(self,type="random"):
        active_moves=[]
        for amazon in self.pieces:
            x_from=amazon.split(",")[0]
            y_from=amazon.split(",")[1]
            active_moves.extend(self.get_moves(self.pieces[self.active]))
        while len(active_moves)>0:
            active_moves


#######################################################################################################################
# main
#######################################################################################################################

if __name__ == "__main__":
    test=True

    am = Amazons(6)
    am.set_amazon(1,2,"b")
    am.set_amazon(3,3,"w")
    am.set_block(2,4)
    print(len(am.get_moves(1,2)))
    am.print()
    am.move(3,3,5,5,4,4)
    am.print()
    sys.exit()