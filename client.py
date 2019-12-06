import socket	#for sockets yes
import sys	#for exit

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error, msg:
    print 'Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1]
    sys.exit();

print 'Socket Created'

host = 'www.google.com'
port = 80

try:
    remote_ip = socket.gethostbyname( host )
except socket.gaierror:
    #could not resolve
    print 'Hostname could not be resolved. Exiting'
    sys.exit()

print 'Ip address of ' + host + ' is ' + remote_ip

#connet to remote server
s.connect((remote_ip , port))

print 'Socket Connected to ' + host + ' on ip ' + remote_ip

#send some data to remote server
message = 'GET / HTTP/1.1\r\n\r\n'

try:
    #set whole string
    s.sendall(message)
except socket.error:
    #send failed
    print 'Send failed'
    sys.exit()

print 'Message send successfully'

#receive data
reply = s.recv(4096)

print reply

s.close()
