#import socket module
from socket import *
import sys
import threading

class Server:
    def __init__(self):
        self.port = 8080
        self.host = gethostbyname(gethostname())
        print("HOST IP: "+self.host)
        try:
            self.s = socket(AF_INET, SOCK_STREAM)
            self.s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
            print("Created socket Object...")
        except error as msg:
            print ("Failed to create socket. Error Code: "+str(msg[0] + " Message: "+msg[1]))
            sys.exit()
        try:
            self.s.bind((self.host,self.port))
            print("...Socket object bound Succesfully!")
        except error as msg:
            print("Failed to bind socket. Error Code: "+str(msg[0]+" Message: "+msg[1]))
            sys,exit()

    def listen(self):
        self.s.listen(5);
        print("Listening on Port: "+str(self.port))
        while (1):
            c,a = self.s.accept()
            print("Connected "+str(a[0])+":"+str(a[1]))
            request_ret = c.recv(1024)
            request = request_ret.decode('utf-8')
            print ("Request {}".format(request))
            try:
                filename = request.split()[1]
                output = "HTTP/1.1 200 OK\r\n\r\n"
                print("FILENAME REQUESTED: "+filename)
                f = open(filename[1:])
                for line in f:
                    output += line
                print("SENDING:\n")
                c.send(output.encode())
                c.send("\r\n\r\n".encode())
                c.close()
            except IOError:
                print("IOError: Cannot open file " +filename)
                c.send("HTTP/1.1 404 Not Found\r\n\r\n".encode())
                c.close()
            except IndexError as e:
                print ("IndexError: "+e)
                c.send("HTTP/1.1 500 Internal Server Error\r\n\r\n".encode())
                c.close()
            except Exception as e:
                print(" Unkown Exception: "+str(e))

if __name__ == "__main__":
    print("server.py started from command line")
    serv= Server()
    serv.listen()

