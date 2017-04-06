import socket
import threading

tLock = threading.Lock()
close = False

print "Presse 'q' si vous voulez sortir de chat"

def receving(name, sock):
    while not close:
        try:
            tLock.acquire()
            while True:
                data, addr = sock.recvfrom(1024)
        except:
            pass
        finally:
            tLock.release()

host = socket.gethostname()
port = 6666

server = (host, port)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect((host, port))
s.setblocking(0)

recvT = threading.Thread(target=receving, args=("RecvThread",s))
recvT.start()

s.sendto("Cette client a entre dans la conversation",server)
message = raw_input("ecrire -> ")

while message != 'q':
    if message != '':
        s.sendto(message, server)
    tLock.acquire()
    message = raw_input("ecrire -> ")
    tLock.release()

s.sendto("Cette client a ete deconnecte",server)

close = True
recvT.join()
s.close()
