from encoding import encodeState

def openRecorder(filepath,whiteToken):
    return gameRecorder(open(filepath,'wb'),whiteToken)

class gameRecorder:
    def __init__(self,stream,whiteToken):
        self._file = stream
        self.tokenW = whiteToken
    def record(self,board,move,nextplay):
        towrite = bytearray(encodeState(board,move,whiteToken,nextplay))
        self._file.write(towrite)
    def __exit__(self, exc_type, exc_value, traceback):
        self._file.close()