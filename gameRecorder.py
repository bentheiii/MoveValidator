from encoding import encodeState
import os
import platform

class osStream:
    def __init__(self,filepath):
        if platform.system()=='Windows':
            self.descriptor = os.open(filepath,os.O_TRUNC | os.O_SEQUENTIAL | os.O_WRONLY,0777)
        else:
            self.descriptor = os.open(filepath,os.O_TRUNC | os.O_CREAT | os.O_WRONLY,0777)
    def write(self,text):
        os.write(self.descriptor,text)
    def close(self):
        os.close(self.descriptor)

def openRecorder(filepath,whiteToken):
    dirpath = os.path.dirname(filepath)
    if not os.path.exists(dirpath):
        os.makedirs(dirpath)
    return gameRecorder(osStream(filepath),whiteToken)

class gameRecorder:
    def __init__(self,stream,whiteToken):
        self._file = stream
        self.tokenW = whiteToken
    def record(self,board,move,nextplay):
        towrite = bytearray(encodeState(board,move,self.tokenW,nextplay))
        self._file.write(towrite)
    def __del__(self):
        self._file.close()