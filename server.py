import socket
import sys
from thread import *

HOST = '' 	#means all available interfaces
PORT = 8888	#Arbitrary non-priviledged port

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Socket created'

#bind socket to local host/port
try:
    s.bind((HOST, PORT))
except socket.error , msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + 'Message ' + msg[1]
    sys.exit()

print 'Socket bind complete'

s.listen(10)
print 'Socket now listening'

myList = []

users = ["billie", "bob", "jo"]
passes = ["hello", "hi", "bye"]
online = []
usernames_dict = {'billie' : 0, 'bob' : 1, 'jo' : 2}
posted = [[] for i in range(3)]
inbox = [[]for i in range(3)]
subscriptions = [[] for i in range(3)]
followers = [[] for i in range(3)]

#def login():
#    conn.sendall('Enter your username: ')
#    username = conn.recv(1024).strip()
#    print "username: " + username
#    conn.sendall('Enter your password: ')
#    password = conn.recv(1024).strip()
#    print "password: " + password
#    if username not in users or password not in passes:
#	conn.sendall('Username/password does not exist\n')
#	return (False, username)
#    elif users.index(username) != passes.index(password):
#	conn.sendall('Username/password not correct!\n')
#	return (False, username)
#    else:
#	conn.sendall('Welcome back ' + username + '!\n')
#	online.append(username)
#	return (True, username)

#def print_menu():
#    conn.sendall('Fake Twitter Menu\n')
#    conn.sendall('1) See Offline Messages\n')
#    conn.sendall('2) Edit Subscriptions\n')
#    conn.sendall('3) Post a Message\n')
#    conn.sendall('4) Logout\n')
#    conn.sendall('5) Hashtag Search\n')
#    conn.sendall('6) See Followers\n')
#    conn.sendall('========================================\n')
#    conn.sendall('Enter option number and press enter\n')

def clientthread(conn):
    #send message to connected client
    is_login = False
    while is_login == False:
	conn.sendall('Enter your username: ')
    	username = conn.recv(1024).strip()
   	print "username: " + username
    	conn.sendall('Enter your password: ')
    	password = conn.recv(1024).strip()
    	print "password: " + password
    	if username not in users or password not in passes:
        	conn.sendall('Username/password does not exist\n')
       	 	is_login = False
    	elif users.index(username) != passes.index(password):
        	conn.sendall('Username/password not correct!\n')
        	is_login = False
    	else:
        	conn.sendall('Welcome back ' + username + '!\n')
        	online.append((username, conn))
        	is_login = True

    u = username
    #conn.sendall(str(online[0][1]) + '\n')

    #while user hasn't quit session
    conn.sendall('You have ' + str(len(inbox[usernames_dict[u]])) + ' unread messages\n\n')
    while True:
	#print_menu()
	conn.sendall('Fake Twitter Menu\n')
    	conn.sendall('1) See Offline Messages\n')
    	conn.sendall('2) Edit Subscriptions\n')
    	conn.sendall('3) Post a Message\n')
    	conn.sendall('4) Logout\n')
    	conn.sendall('5) Hashtag Search\n')
    	conn.sendall('6) See Followers\n')
    	conn.sendall('========================================\n')
    	conn.sendall('Enter option number and press enter\n')

	#Receiving from client
	menu_response = conn.recv(1024)
	if menu_response == '1\r\n':
	    conn.sendall('Read offline messages\n')
	    conn.sendall('a) Read messages from specific subscription\n')
	    conn.sendall('b) Read all unread messages\n')
	    conn.sendall('c) Return to menu\n')
	    read = conn.recv(1024)
	    if read == 'a\r\n':
		conn.sendall('Enter username to read messages from: ')
		add_username = conn.recv(1024).strip()
		conn.sendall(add_username + "'s messages\n")
		i = 0
		while i < len(inbox[usernames_dict[u]]):
		    if inbox[usernames_dict[u]][i][0] == add_username:
			conn.sendall(inbox[usernames_dict[u]][i][1] + ', ' + inbox[usernames_dict[u]][i][2] + '\n')
			popped = inbox[usernames_dict[u]].pop(i)
		    else:
			i = i + 1
		conn.sendall('\n')

	    elif read == 'b\r\n':
		conn.sendall('All messages:\n')
		for i in range(len(inbox[usernames_dict[u]])):
		    conn.sendall(inbox[usernames_dict[u]][i][0] + ": " + inbox[usernames_dict[u]][i][1] + ", " + inbox[usernames_dict[u]][i][2] + '\n')
		conn.sendall('\n')
		inbox[usernames_dict[u]] = []
	    elif read == 'c\r\n':
		conn.sendall('Returning to menu\n\n')
		continue

	elif menu_response == '2\r\n':
	    conn.sendall('Edit your Subscriptions\n')
	    conn.sendall('a) Add a subscription\n')
	    conn.sendall('b) Drop a subscription\n')
	    conn.sendall('c) Return to menu\n')
	    edit = conn.recv(1024)
	    if edit == 'a\r\n':
		conn.sendall('Enter username to add subscription to: ')
		add_username = conn.recv(1024).strip()
		if add_username != u and add_username in users:
		    subscriptions[usernames_dict[u]].append(add_username)
		    followers[usernames_dict[add_username]].append(u)
		    conn.sendall('Adding to subscriptions.\n\n')
		    print subscriptions[usernames_dict[u]]
		    print followers[usernames_dict[add_username]]
		else:
		    conn.sendall('Username not valid.\n\n')
		    continue
	    elif edit == 'b\r\n':
		conn.sendall('Current subscriptions available to drop:\n')
		for i in range(len(subscriptions[usernames_dict[u]])):
		    conn.sendall(subscriptions[usernames_dict[u]][i] + '\n')
		conn.sendall('Enter username to drop subscription from: ')
		drop_username = conn.recv(1024).strip()
		if drop_username in subscriptions[usernames_dict[u]]:
		    subscriptions[usernames_dict[u]].remove(drop_username)
		    followers[usernames_dict[drop_username]].remove(u)
		    conn.sendall('Dropping from subscriptions.\n\n')
		    print subscriptions[usernames_dict[u]]
		    print subscriptions[usernames_dict[drop_username]]
		else:
		    conn.sendall('Cannot drop user if not subscribed.\n\n')
		    continue
	    elif edit == 'c\r\n':
		conn.sendall('Returning to menu\n\n')
		continue

	    else:
		conn.sendall('Invalid menu option\n\n')
		continue

	elif menu_response == '3\r\n':
	    conn.sendall('Post tweet: ')
	    tweet = conn.recv(1024).strip()
	    if len(tweet) > 140:
		conn.sendall('Cannot post tweet longer than 140 characters.\n\n')
		continue
	    conn.sendall('Add hashtags: ')
	    hashtags = conn.recv(1024).strip()
	    posted[usernames_dict[u]].append((tweet, hashtags))
	    for i in range(len(followers[usernames_dict[u]])):
		#if (followers[usernames_dict[u]][i],) in online:
		flag = 0
		for j in range(len(online)):
		     if online[j][0] == followers[usernames_dict[u]][i]:
			online[j][1].sendall(u + ": " + tweet + ", " + hashtags + '\n')
			flag = 1
		if flag == 0:
		    inbox[usernames_dict[followers[usernames_dict[u]][i]]].append((u, tweet, hashtags))
	    #for i in range(len(followers[usernames_dict[u]])):
	    #	inbox[usernames_dict[followers[usernames_dict[u]][i]]].append((u, tweet, hashtags))
	    conn.sendall('Tweet posted.\n\n')
	    print posted[usernames_dict[u]]
	    for i in range(len(followers[usernames_dict[u]])):
		print inbox[usernames_dict[followers[usernames_dict[u]][i]]]

	elif menu_response == '4\r\n':
	    conn.sendall('Bye ' + u + '!\n\n')
	    online.remove((u, conn))
	    clientthread(conn)

	elif menu_response == '5\r\n':
	    conn.sendall('Search by hashtag!\n')
	    conn.sendall('a) Type in a hashtag\n')
	    conn.sendall('b) Return to menu\n')
	    hashtag = conn.recv(1024)
	    if hashtag == 'a\r\n':
		conn.sendall('Type in the hashtag you want to search for!\n')
		tag = conn.recv(1024).strip()
		found = 0
		for i in reversed(range(len(inbox[usernames_dict[u]]))):
		    if inbox[usernames_dict[u]][i][2] == tag:
			found = found + 1
			conn.sendall(inbox[usernames_dict[u]][i][0] + ": " + inbox[usernames_dict[u]][i][1] + ", " + inbox[usernames_dict[u]][i][2] + '\n')
		    if found == 10:
			conn.sendall('\n')
			break;
		conn.sendall('\n')

	elif menu_response == '6\r\n':
	    conn.sendall('Followers:\n')
	    for i in range(len(followers[usernames_dict[u]])):
		conn.sendall(followers[usernames_dict[u]][i] + '\n')
	    conn.sendall('\n')
	  
	#if_sendall = data.find('!sendall')
	#if if_sendall != -1:
	#    for member in myList:
	# 	member.sendall(data[if_sendall + 9:])
	#reply = 'OK...' + menu_response
	#if not menu_response:
	#   break
	
	#conn.sendall(reply)

    #came out of loop
    conn.close()

#keep talking with client
#myList = []
while 1:
    #wait to accept connection - blocking call
    conn, addr = s.accept()
    myList.append(conn)
    print 'Connected with ' + addr[0] + ':' + str(addr[1])

    #start new thread takes 1st arg as function name to be run, second is tuple of args to function
    start_new_thread(clientthread ,(conn,))

s.close()
