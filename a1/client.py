from socket import *
import sys

class Client:
    def __init__(self, *args):
        try:
            self.s = socket(AF_INET, SOCK_STREAM)
            self._arg_ip = args[0][1]
            self._arg_port = args[0][2]
            self._arg_filename = args[0][3]
            print("CLIENT ARGS: [IP]: "+self._arg_ip+" [PORT]:"+self._arg_port+" [FILE]: "+self._arg_filename)
        except error:
            print ("Error. could not create socket")
            sys.exit()

    def run(self):
        try:
            request = "GET /"+self._arg_filename+" HTTP/1.1"
            self.s.connect((self._arg_ip,int(self._arg_port)))
            self.s.sendto(request.encode(), (self._arg_ip, int(self._arg_port)))
        except Exception as e:
            print("send Failed: "+str(e))
            sys.exit()
        while(True):
            reply = self.s.recv(4096)
            if not reply: break
            print ("Reply from server: "+str(reply))
if __name__ == "__main__":
    client = Client(sys.argv)
    client.run()
