import socket
import sys
import config
import re
from time import sleep
from random import randrange
import os.path

messages = [config.RETURN_FILE_DATA, config.RETURN_FILE_DETAILS, config.SUCCESS, config.FAILURE]

def send_req(ip, port, data):
    # connect server
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, port)) 
    s.settimeout(2)
    s.sendall(data)

    print "From Client send_req "+"Sent: \"" + data.rstrip('\n') + "\""
    return get_req(s.recv(2048))

def get_req(msg):
    global messages
    print "From Client get_req "+ "Received: \"" + msg.rstrip('\n') + "\""
    matched_request = ""
    matched_vars = []
    for r in messages:
        m = re.match(r.replace("{}", "(.*)"), msg)
        if m:
            matched_request = r
            matched_vars = m.groups()
            
    return (matched_request, matched_vars)

# print connection instructions
print "Client Proxy Interface"
print "======================"
name = raw_input("Enter client name: ")
# get file details from directory server

raw_input("Press Enter to continue...\n")

End_condition = 'Y'
while(End_condition=='Y'):
    file_address = raw_input("Select your file address:\n")
    #file = open(file_address, 'r')
    file_store_address = raw_input("Which folder on server you want ot store in?\n")
    command = raw_input("What is ur command? W for write file; R for read file; D for delete file\n")
    if(command=='W'):
        if(not os.path.exists(file_address)): 
            print "No Such file in local address\n"
            continue

        (req, vars) = send_req("localhost", config.DIR_SERVER, config.REQUEST_FILE_DETAILS.format(file_address, file_store_address, "WRITE"))
        file_id = vars[0]
        file_ip = vars[1]
        file_port = int(vars[2])               
        file = open(file_address, 'r')
        msg = send_req(file_ip, file_port, config.WRITE_FILE.format(file_id, name, file.read()))
        print msg
        print msg
        Lock_Req = raw_input("Lock or Unlock? L for Lock; U for Unlock\n")
        if(Lock_Req=='L'):
            send_req("localhost", config.LOCK_SERVER, config.REQUEST_LOCK.format(file_id, name))
        elif(Lock_Req=='U'):
            send_req("localhost", config.LOCK_SERVER, config.REQUEST_UNLOCK.format(file_id, name))


    elif(command=='R'):
        (req, vars) = send_req("localhost", config.DIR_SERVER, config.REQUEST_FILE_DETAILS.format(file_address, file_store_address, "WRITE"))
        if(vars is None):
            print "No Such File in storage\n"
            continue;
        file_id = vars[0]
        file_ip = vars[1]
        file_port = int(vars[2])
        send_req(file_ip, file_port, config.READ_FILE.format(file_id, name))

    elif(command=='D'):
        (req, vars) = send_req("localhost", config.DIR_SERVER, config.REQUEST_FILE_DETAILS.format(file_address, file_store_address, "WRITE"))
        if(vars is None):
            print "No Such File in storage\n"
            continue;
        file_id = vars[0]
        file_ip = vars[1]
        file_port = int(vars[2])
        send_req(file_ip, file_port, config.DELETE_FILE.format(file_id, name))

    

    
    End_condition = raw_input("Y for continue, Else press any button...")


print "Thanks for using!\n"

