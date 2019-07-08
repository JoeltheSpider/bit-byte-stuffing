import socket

#Removes stuffed bits
def rem_bit(bits):
    out=''
    ones = 0
    for i in bits:
        if(ones == 5):
            ones = 0
            continue
        if(i=='1'):
            ones+=1
        else:
            ones=0
        out+=i
    return out

#converts binary to character
def to_char(message):
    out = ""
    for i in range(int(len(message)/8)):
        byte = message[i*8:i*8+8]
        if(byte=='01111110'):
            out+='FLAG '
        elif(byte=='10100011'):
            out+='ESC '
        else:
            byte = chr(int(byte,2))
            out+=byte+' '
    return out

#removes unwanted bytes
def to_normal(message):
    out = ""
    esc = 0
    for i in message.split():           
        if(i=='ESC'):
            if(esc==0):
                out+=i+' '
                esc = 1
            else:
                esc = 0
        elif(i=='FLAG'):
            if(esc==1):
                out = out[:-4]
            out+=i+' '
            esc = 0
        else:
            out+=i+' '
            esc = 0
    out = out[:-1]
    return out
        

server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

host = socket.gethostname()
port = 9992

server_socket.bind((host,port))
server_socket.listen(1)

client_socket,addr = server_socket.accept()

data = '' 
msg = ''
while (msg!='11111111'):
    data+=msg
    msg1 = client_socket.recv(35).decode('ascii')
    msg = msg1[:-8]
    msg = msg[8:]

print('Message received:\t',data)
msg = rem_bit(data)
print("\nUnwanted bits removed: ",msg)
msg = to_char(msg)
print("Converted to text: ",msg)
msg = to_normal(msg)
print("Unwanted ESCs removed: ",msg)

client_socket.close()