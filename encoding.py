from pieces import *
from boardstate import coortransform

ENCODINGSIZE=37
#encoding:first 32 bytes: piece locations
#       next     4 bytes: focus locations
#       next     1  byte: additional game info 
#total package size = 37bytes ,standard game ~2K, longest ~10K
#piece location:0-63 locations on the board (0,0)->0, (1,0)->1
#piece location 64: piece eaten (or otherwise missing)
#piece locations ordered by piece type as follows: PPPPPPPPRRHHBBQK
#first white pieces, then black pieces
#
#focus locations: coordinates as above, represent previous move
#except if the value is over 64, then the focus is of disappearance (location is value mod 64)
#duplicate focus locations are not allowed
#128 means both that there is no focus and that the following focus locations are 128 as well
#if first focus location is 128, initial appear has happened
#
#additional info: 0 means anyone can play next, 1 means white plays next, 2 means black plays next
#
#example board (capital is white, lower is black):
#RHBQKBHR
#PPPPPPPP
#::::::::
#::::::::
#::::::::
#::::::::
#pppppppp
#rhbqkbhr
#
#will be encoded as:
#[1,9,17,25,33,41,49,57,0,56,8,48,16,40,24,32,6,14,22,30,38,46,54,62,7,63,15,55,23,47,31,39,128,128,128,128,0]
def encodeState(board,move,whiteToken,nextplay):
    pieces = [64]*32
    for p in board.pieces:
        offset = 0
        if p.token != whiteToken:
            offset += 16
        if isinstance(p,pawn):
            pass
        elif isinstance(p,rook):
            offset += 8
        elif isinstance(p,knight):
            offset+=10
        elif isinstance(p,bishop):
            offset+=12
        elif isinstance(p,queen):
            offset+=14
        else:#king
            offset+=15
        while pieces[offset] != 64:
            offset+=1
        pieces[offset] = p.location[1]*board.size+p.location[0]
    focus = []
    if len(move.appears) + len(move.disappears) <= 4:
        for a in move.appears:
            coor = coortransform(a.coordinates,board.transform,board.size)
            focus.append(coor[1]*board.size+coor[0])
        for a in move.disappears:
            coor = coortransform(a.coordinates,board.transform,board.size)
            if coor[1]*board.size+coor[0] in focus:
                continue
            focus.append(coor[1]*board.size+coor[0]+64)
    if len(focus) < 4:
        focus = focus + [128]*(4-len(focus))
    if nextplay is None:
        adinf = 0
    elif nextplay == whiteToken:
        adinf = 1
    else:
        adinf = 2
    return pieces+focus+[adinf]