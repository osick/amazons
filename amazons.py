#!/usr/bin/env python3
# -*- coding: utf-8 -
__author__ = "Oliver Sick"

import sys
import random
import time
import os
import json

class Amazons:
    
    empty_sq="·"
    block_sq="▒"
    #block_sq="▉"
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
            self.pieces[self.board[x][y]].pop(self.pieces[self.board[x][y]].index(f"{x},{y}"))
        self.board[x][y]=Amazons.empty_sq


    def set_block(self,x,y):
        self.board[x][y]=Amazons.block_sq


    def get_moves(self,x,y):
        _moves=[]
        _moves.extend(self.iter_moves(x, y,  1,  0))    
        _moves.extend(self.iter_moves(x, y,  1,  1))    
        _moves.extend(self.iter_moves(x, y,  0,  1))
        _moves.extend(self.iter_moves(x, y, -1,  1))
        _moves.extend(self.iter_moves(x, y, -1,  0))
        _moves.extend(self.iter_moves(x, y, -1, -1))
        _moves.extend(self.iter_moves(x, y,  0, -1))
        _moves.extend(self.iter_moves(x, y,  1, -1))
        moves=[]
        for m in _moves:
            x1=int(m.split(",")[0])
            y1=int(m.split(",")[1])
            moves.extend(self.iter_moves(x1, y1,  1,  0, x, y))    
            moves.extend(self.iter_moves(x1, y1,  1,  1, x, y))    
            moves.extend(self.iter_moves(x1, y1,  0,  1, x, y))
            moves.extend(self.iter_moves(x1, y1, -1,  1, x, y))
            moves.extend(self.iter_moves(x1, y1, -1,  0, x, y))
            moves.extend(self.iter_moves(x1, y1, -1, -1, x, y))
            moves.extend(self.iter_moves(x1, y1,  0, -1, x, y))
            moves.extend(self.iter_moves(x1, y1,  1, -1, x, y))
        return moves


    def iter_moves(self,x,y,dir_x,dir_y,x_ignore=None,y_ignore=None):
        itermoves=[]
        x1=x+dir_x
        y1=y+dir_y
        try:
            if (x_ignore is not None and y_ignore is not None):
                while self.board[x1][y1] == Amazons.empty_sq or (x1==x_ignore and y1==y_ignore):
                    itermoves.append(f"{x_ignore},{y_ignore},{x},{y},{x1},{y1}")
                    x1+=dir_x
                    y1+=dir_y
            else:
                while self.board[x1][y1] == Amazons.empty_sq:
                    itermoves.append(f"{x1},{y1}")
                    x1+=dir_x
                    y1+=dir_y
        except: pass
        return itermoves


    def can_move(self,x,y):
        return self.board[x][y]==self.active


    def move(self, x_from, y_from, x_to, y_to, x_block, y_block):
        if self.get_moves(x_from, y_from).count(f"{x_from},{y_from},{x_to},{y_to},{x_block},{y_block}")>0 \
        and self.can_move(x_from, y_from):
            self.clear_sq(x_from,y_from)
            self.set_amazon(x_to, y_to)
            self.set_block(x_block, y_block)
            self.active=Amazons.b_amazon_sq if self.active==Amazons.w_amazon_sq else Amazons.w_amazon_sq

    def print(self):
        board="═".join(self.board[0])
        for i in range(self.boardsize,0,-1): board+="\n"+" ".join(self.board[i])
        board+="\n"+"═".join(self.board[self.boardsize+1])
        board=board.replace(Amazons.block_sq+" ",Amazons.block_sq+Amazons.block_sq)
        print(board.replace(" "+Amazons.block_sq,Amazons.block_sq+Amazons.block_sq))

    def play(self,type="random",display=False):
        active_moves=[]
        for amazon in self.pieces[self.active]:
            x_from=int(amazon.split(",")[0])
            y_from=int(amazon.split(",")[1])
            active_moves.extend(self.get_moves(x_from,y_from))
        while len(active_moves)>0:
            if display:
                os.system('cls')
                self.print()
            rnd_move=random.choice(active_moves)
            coords=[int(x) for x in rnd_move.split(",")]
            self.move(coords[0],coords[1],coords[2],coords[3],coords[4],coords[5])
            active_moves=[]
            for amazon in self.pieces[self.active]:
                x_from=int(amazon.split(",")[0])
                y_from=int(amazon.split(",")[1])
                active_moves.extend(self.get_moves(x_from,y_from))
        return self.active
        
#######################################################################################################################
# main
#######################################################################################################################

if __name__ == "__main__":
    max_size= 8 if len(sys.argv)<2 else int(sys.argv[1])
    for size in range(2,max_size+1):
        score={Amazons.b_amazon_sq:0,Amazons.w_amazon_sq:0}
        for i in range(500):
            am = Amazons(size)
            am.set_amazon(1,1,"b")
            #am.set_amazon(1,size,"b")
            #am.set_amazon(size,size,"w")
            am.set_amazon(size,1,"w")
            #if i==0: am.print()
            v=am.play()
            score[v]+=1
        #print(size, json.dumps(score))
        print(size,"white wins:",score[Amazons.w_amazon_sq]/5,"%")