from moveinterpreter import board,moveInterpreter
from validator import validator
from itertools import *
from gameRecorder import openRecorder

def loadBoards(source, size=8, noneToken ='0'):
    ret = None
    row = 0
    for line in source:
        if line.startswith('#'):
            continue
        if ret is None:
            ret = board(size)
        for token, col in izip(line,xrange(size)):
            if token == noneToken:
                token = None
            ret[row,col] = token
        row+=1
        if row == size:
            yield ret
            ret = None
            row = 0

def strSigns(state,size=8,transform=False):
    ret = []
    for x in xrange(size):
        for y in xrange(size):
            #y = size-y-1
            if state.occupant(x,y,transform) is None:
                ret.append(":")
            else:
                if state.occupant(x,y,transform).token == 'l':
                    ret.append(state.occupant(x,y,transform).sign().lower())
                else:
                    ret.append(state.occupant(x,y,transform).sign())
        ret.append("\n")
    return "".join(ret)

def strTokens(state,size=8,transform=False):
    ret = []
    for x in xrange(size):
        for y in xrange(size):
            if state.occupant(x,y,transform) is None:
                ret.append(":")
            else:
                ret.append(state.occupant(x,y,transform).token)
        ret.append("\n")
    return "".join(ret)

interpreter = moveInterpreter()
movevalidator = validator('U','l',8)
recorder = openRecorder('test0.ckm',movevalidator.board.tokenW)
for b, ind in izip(loadBoards(file("validatortestingboards{}.txt".format(4))),count(1)):
    move = interpreter.nextmove(b)
    valid, valValue = movevalidator.isValid(move)
    if valid:
        interpreter.commit(b)
        movevalidator.Commit(move,valValue)
        print "#{}".format(ind)
        print strSigns(movevalidator.board,transform=True)
        print "next play: {}".format(movevalidator.nextPlay())

        #raw_input()
        #print strTokens(movevalidator.board,transform=True)
    else:
        print "#{}: bad move".format(ind)