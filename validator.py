from pieces import *
from boardstate import boardState, coortransform
from moveinterpreter import moveTypes
#TODO:turns
class validator:
    def __init__(self,whitetoken,blacktoken,size=8):
        self.board = boardState(whitetoken,blacktoken,size)
        #dictates which token should not play next, None means anyone can play next (in case of assignment)
        self.prevTurn = None
    def ValidateAppear(self,move):
        whites = filter(lambda x:x.kind==self.board.tokenW,move.appears)
        #whites = []
        #for c in move.appears:
        #    if c.kind == self.board.tokenW:
        #        whites.append(c)
        blacks = filter(lambda x:x.kind==self.board.tokenB,move.appears)
        if (not self.board.pieces is None) or len(move.appears) != 32 \
        or len(whites) != 16 \
        or len(blacks) != 16:
            return False, None
        #identify corners
        #(0,0)
        NWCorner = None
        #(0,size-1)
        NECorner = None
        #(size-1,0)
        SWCorner = None
        #(size-1,size-1)
        SECorner = None

        for appear in move.appears:
            if appear.coordinates==(0,0):
                NWCorner = appear.kind
            elif appear.coordinates==(0,self.board.size-1):
                NECorner = appear.kind
            elif appear.coordinates==(self.board.size-1,0):
                SWCorner = appear.kind
            elif appear.coordinates==(self.board.size-1,self.board.size-1):
                SECorner = appear.kind

        #all corners have to be filled
        if NWCorner is None or NECorner is None or SWCorner is None or SECorner is None:
            return False, None

        if NWCorner == NECorner and SWCorner == SECorner and NWCorner != SECorner:
            #white on north (0,x), (1,x), black on south (size-1,x) (size-2,x) (or reversed)
            for appear in move.appears:
                if appear.coordinates[0] <= 1:
                    if appear.kind == NWCorner:
                        continue
                    else:
                        return False, None
                if appear.coordinates[0] >= self.board.size-2:
                    if appear.kind == SECorner:
                        continue
                    else:
                        return False, None
                return False, None
        elif NWCorner == SWCorner and NECorner == SECorner and NWCorner != SECorner:
            #white on west (x,0), (x,1), black on south (x,size-1) (x,size-2) (or reversed)
            for appear in move.appears:
                if appear.coordinates[1] <= 1:
                    if appear.kind == NWCorner:
                        continue
                    else:
                        return False, None
                if appear.coordinates[1] >= self.board.size-2:
                    if appear.kind == SECorner:
                        continue
                    else:
                        return False, None
                return False, None
        else:
            return False,None
        #get the transform
        if NWCorner==NECorner:
            if NWCorner==self.board.tokenW:
                return True,0
            else:
                return True,2
        if NWCorner==SWCorner:
            if NWCorner==self.board.tokenW:
                return True,3
            else:
                return True,1
    def commitAppear(self,transform):
        self.board.transform = transform

        self.board.insertPiece(rook(self.board.tokenW),(0,0))
        self.board.insertPiece(rook(self.board.tokenW),(0,7))
        self.board.insertPiece(knight(self.board.tokenW),(0,1))
        self.board.insertPiece(knight(self.board.tokenW),(0,6))
        self.board.insertPiece(bishop(self.board.tokenW),(0,2))
        self.board.insertPiece(bishop(self.board.tokenW),(0,5))
        self.board.insertPiece(queen(self.board.tokenW),(0,3))
        self.board.insertPiece(king(self.board.tokenW),(0,4))

        self.board.insertPiece(rook(self.board.tokenB),(7,0))
        self.board.insertPiece(rook(self.board.tokenB),(7,7))
        self.board.insertPiece(knight(self.board.tokenB),(7,1))
        self.board.insertPiece(knight(self.board.tokenB),(7,6))
        self.board.insertPiece(bishop(self.board.tokenB),(7,2))
        self.board.insertPiece(bishop(self.board.tokenB),(7,5))
        self.board.insertPiece(queen(self.board.tokenB),(7,3))
        self.board.insertPiece(king(self.board.tokenB),(7,4))

        for i in xrange(8):
            self.board.insertPiece(pawn(self.board.tokenW,1),(1,i))
            self.board.insertPiece(pawn(self.board.tokenB,-1),(6,i))

        self.advanceTurn(None)
    def hasTurn(self,playToken):
        if self.prevTurn is None:
            return True
        return (self.prevTurn != playToken)
    def isValid(self,move):
        if move.type == moveTypes.appear:
            return self.ValidateAppear(move)
        if self.board.pieces is None:
            return False,None
        if move.type == moveTypes.regular:
            mover = self.board.occupant(move.disappears[0].coordinates, transformcoor=True)
            if not self.hasTurn(mover.token):
                return False, None
            board = self.board if mover.token==self.board.tokenW else self.board.reverse()
            targetcoor = coortransform(move.appears[0].coordinates,self.board.transform,self.board.size)
            if not mover.validMove(targetcoor,board):
                return False, None
            else:
                return True, mover
        if move.type == moveTypes.eat or move.type == moveTypes.irregularEat:
            eaten = self.board.occupant(move.disappears[0].coordinates if move.disappears[1].kind == move.appears[0].kind else move.disappears[1].coordinates, transformcoor=True)
            eatertarloc = coortransform(move.appears[0].coordinates,self.board.transform,self.board.size)
            eater = self.board.occupant(move.disappears[0].coordinates if move.disappears[0].kind == move.appears[0].kind else move.disappears[1].coordinates, transformcoor=True)
            if not self.hasTurn(eater.token):
                return False, None
            board = self.board if eater.token==self.board.tokenW else self.board.reverse()
            if not eater.validEat(eatertarloc,eaten,board):
                return False,None
            return True,(eater,eaten)
        if move.type == moveTypes.multiMove:
            pass#TODO:castling
        return False, None
    def advanceTurn(self,prevToken):
        self.prevTurn = prevToken
    def Commit(self,move,validationValue):
        if move.type == moveTypes.appear:
            self.commitAppear(validationValue)
        elif move.type == moveTypes.regular:
            self.board.assign(None,validationValue.location)
            validationValue.move(coortransform(move.appears[0].coordinates,self.board.transform,self.board.size))
            self.board.assign(validationValue,validationValue.location)
            self.advanceTurn(validationValue.token)
        elif move.type == moveTypes.eat or move.type == moveTypes.irregularEat:
            eater, eaten = validationValue
            self.board.assign(None,eaten.location)
            self.board.pieces.remove(eaten)
            self.board.assign(None,eater.location)
            eater.move(coortransform(move.appears[0].coordinates,self.board.transform,self.board.size))
            self.board.assign(eater,eater.location)
            self.advanceTurn(eater.token)
        elif move.type == moveTypes.multiMove:
            pass
        self.board.advance()

