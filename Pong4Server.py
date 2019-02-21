import socket
import threading
import socketserver as SocketServer
import pygame
import marshal,json
import GameState as gs

if __name__ == "__main__":    
    game_state = gs.GameState() 
       
    class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):

        def handle(self):
            data = str(self.request.recv(4096), 'ascii')        
            cur_thread = threading.current_thread()                
            print("Recieved:", "{}: {}".format(cur_thread.name, data))

            if (data == "GameState"):
                game_state_str = game_state.toJSON().encode('ascii')
                self.request.sendall(game_state_str)

    class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
        pass

    HOST, PORT = socket.gethostname(), 9009
    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
    ip, port = server.server_address

    # start a thread with the server. 
    # the thread will then start one more thread for each request.
    server_thread = threading.Thread(target=server.serve_forever)

    # exit the server thread when the main thread terminates
    server_thread.daemon = True
    server_thread.start()
    print("Pong 4 server loop running in thread:", server_thread.name)

    #client(ip, port,  "Hello World 1".encode('ascii'))
    #client(ip, port, "Hello World 2")
    #client(ip, port, "Hello World 3")

    #server.shutdown()       
    
    ### Constants
    game_state.W = 600 # Width of the game table
    game_state.H = game_state.W # Height of the game table Game should be a square always to be fair for 4 player game

    game_state.FourPlayers = True ## 2 Players or 4 Players mode    

    while True:
        pass
