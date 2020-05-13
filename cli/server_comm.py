import socketio
import time
from util import Singleton
# from vlc_comm import VLCplayer
# player = VLCplayer.getInstance()
import vlc_comm


class VLC_signals(socketio.ClientNamespace): # this is used internally by ServerConnection
    def bind(self):
        pass
    def on_connect(self):
        print('connected')

    def on_disconnect(self):
        print('disconnected')

    def on_play(self,*args, **kwargs):
        vlc_comm.VLCplayer().play()
    
    def on_pause(self,*args, **kwargs):
        vlc_comm.VLCplayer().pause()

    def on_seek(self,position,*args, **kwargs):
        print("Seek signal for ",position)
        vlc_comm.VLCplayer().seek(position)

class ServerConnection():
    def __init__(self):
        # super().__init__()
        self.sio = socketio.Client()
        self.sio.connect('http://localhost:3000')

    def send(self,signal,data):
        data['last_updated'] = time.time()
        self.sio.emit(signal,data)

    def start_listening(self):
        self.signals = VLC_signals('/')
        self.signals.bind()
        self.sio.register_namespace(self.signals)


server = ServerConnection()
server.start_listening()
