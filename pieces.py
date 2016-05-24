from boardstate import allClear

def locationdiff(origin,target):
    return target[0]-origin[0],target[1]-origin[1]
def sign(num):
    if num > 0:
        return 1
    if num < 0:
        return -1
    return 0
def bringCloserTo(origin, target):
    diff = locationdiff(origin,target)
    return origin[0]+sign(diff[0]),origin[1]+sign(diff[1])
def getPath(origin, target):
    origin = bringCloserTo(origin,target)
    while origin!=target:
        yield origin
        origin = bringCloserTo(origin,target)
class piece:
    def __init__(self,token):
        self.token = token
        self.location = None
        self.firstMoveTime = None
    def validMove(self, targetLocation, board):
        if not board.occupant(targetLocation) is None:
            return False
        return self.canMove(targetLocation, board)
    def canMove(self,targetLocation,board):
        raise NotImplementedError
    def validEat(self,targetLocation,targetPiece,board):
        if targetPiece.token == self.token:
            return False
        return self.canEat(targetLocation,targetPiece,board)
    def canEat(self,targetLocation,targetPiece,board):
        if targetPiece.location != targetLocation:
            return False
        return self.canMove(targetLocation,board)
    def advanceTime(self):
        if not self.firstMoveTime is None:
            self.firstMoveTime+=1
    def move(self,newLocation):
        self.location = newLocation
        if self.firstMoveTime is None:
            self.firstMoveTime = 0
    def __repr__(self):
        return "{}s {} at {}".format(self.token,self.sign(),self.location)
class pawn(piece):
    def __init__(self,token,direction):
        piece.__init__(self,token)
        self.jumpTime = None
        self.direction = direction
    def canMove(self,targetLocation,board):
        diff = locationdiff(self.location, targetLocation)
        if diff[1]!=0:
            return False
        if diff[0] == self.direction:
            return True
        if diff[0] == 2*self.direction:
            return self.firstMoveTime is None
        return False
    def canEat(self,targetLocation,targetPiece,board):
        diff = locationdiff(self.location,targetLocation)
        if diff[0] != self.direction:
            return False
        if abs(diff[1]) != 1:
            return False
        if isinstance(targetPiece,pawn) and targetPiece.jumpTime == 1:
            #chance for en passant
            eatdiff = locationdiff(self.location,targetPiece.location)
            terdiff = locationdiff(targetPiece.location, targetLocation)
            return (abs(eatdiff[1]) == 1 and eatdiff[0]==0) and (terdiff[1] == 0 and terdiff[0] == self.direction)
        return True
    def advanceTime(self):
        piece.advanceTime(self)
        if not self.jumpTime is None:
            self.jumpTime+=1
    def move(self,newLocation):
        piece.move(self,newLocation)
        diff = locationdiff(self.location,newLocation)
        if diff[1] == 2:
            self.jumpTime = 0
    @staticmethod
    def sign():
        return "P"
class knight(piece):
    def __init__(self,token):
        piece.__init__(self,token)
    def canMove(self,targetLocation,board):
        diff = locationdiff(self.location,targetLocation)
        if (abs(diff[0]) + abs(diff[1])) !=3:
            return False
        return True
    @staticmethod
    def sign():
        return "H"
class king(piece):
    def __init__(self,token):
        piece.__init__(self,token)
    def canMove(self,targetLocation,board):
        diff = locationdiff(self.location,targetLocation)
        if abs(diff[0]) > 1 or abs(diff[1])>1 :
            return False
        return True
    @staticmethod
    def sign():
        return "K"
class rook(piece):
    def __init__(self,token):
        piece.__init__(self,token)
    def canMove(self,targetLocation,board):
        diff = locationdiff(self.location,targetLocation)
        if diff[0] != 0 and diff[1] != 0:
            return False
        return allClear(board,getPath(self.location,targetLocation))
    @staticmethod
    def sign():
        return "R"
class bishop(piece):
    def __init__(self,token):
        piece.__init__(self,token)
    def canMove(self,targetLocation,board):
        diff = locationdiff(self.location,targetLocation)
        if abs(diff[0]) != abs(diff[1]):
            return False
        return allClear(board,getPath(self.location,targetLocation))
    @staticmethod
    def sign():
        return "B"
class queen(piece):
    def __init__(self,token):
        piece.__init__(self,token)
    def canMove(self,targetLocation,board):
        diff = locationdiff(self.location,targetLocation)
        if abs(diff[0]) != abs(diff[1]) and diff[0] != 0 and diff[1] != 0:
            return False
        return allClear(board,getPath(self.location,targetLocation))
    @staticmethod
    def sign():
        return "Q"