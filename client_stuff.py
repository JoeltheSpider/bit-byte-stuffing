import socket

#ESC bytes are added
def byte_stuff(message):
    out = ""
    for i in message.split():
        if(i=='FLAG' or i=='ESC'):
            out+="ESC "
        out+=i+' '
    return out

#bytes are converted to binary(string in this case)
def to_bin(message):
    out = ""
    for i in message.split():
        if(i=='ESC'):
            out+='10100011'
        elif(i=='FLAG'):
            out+='01111110'
        else:
            out+='0'+bin(ord(i))[2:]
    return out

#one '0' bit is added for every 5 '1' bits to avoid confusion with FLAG
def bit_stuff(bits):
    out = ""
    ones = 0
    for i in bits:
        if(i=='1'):
            ones+=1
        else:
            ones=0
        out+=i
        if(ones==5):
            out+='0'
            ones=0
    return out

#Message is split to 16-bits per frame + 2 FLAG bytes
def to_frame(message):
    mes = []
    odd=0
    if(len(message)%16!=0):
        odd=1
    for i in range(int(len(message)/16)+odd):
        byte = '01111110'+message[i*16:i*16+16]+'01111110'
        mes.append(byte)
    mes.append('011111101111111101111110')
    return mes
        
            
client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

#Enter your host and port here
host=socket.gethostname()
port=9992

client_socket.connect((host,port))

mes = input("Enter message to send:\t")
message = byte_stuff(mes)
print("Byte stufed message is ",message)
message = to_bin(message)
for i in to_frame(message):
    print("Binary formated frame message is ",i)
    client_socket.send(i.encode('ascii'))
client_socket.close()