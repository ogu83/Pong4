import socket
import json
import GameState as gs

game_state = gs.GameState()

def client(ip, port, message):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    try:        
        sock.sendall(bytes(message.encode('ascii')))
        response = sock.recv(4096)
        if (message == "GameState"):
            game_state_str = response.decode('ascii')
            game_state= gs.GameState.from_json(game_state_str)            
        pass
    finally:
        sock.close()

ip, port = socket.gethostname(), 9009
client(ip, port,  "GameState")