from moveinterpreter import board,moveInterpreter
from validator import validator
from itertools import *
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

def strSigns(state,size=8):
    ret = []
    for x in xrange(size):
        for y in xrange(size):
            if state.occupant(x,y) is None:
                ret.append("#")
            else:
                ret.append(state.occupant(x,y).sign())
        ret.append("\n")
    return "".join(ret)

interpreter = moveInterpreter()
movevalidator = validator('2','1',8)
for b, ind in izip(loadBoards(file("validatortestingboards{}.txt".format(1))),count(1)):
    move = interpreter.nextmove(b)
    valid, valValue = movevalidator.isValid(move)
    if valid:
        interpreter.commit(b)
        movevalidator.Commit(move,valValue)
        print "#{}".format(ind)
        print strSigns(movevalidator.board)
    else:
        print "#{}: bad move".format(ind)