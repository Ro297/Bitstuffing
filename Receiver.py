import struct
import sys

def divide(dividend,divisor):
    f = []
    for i in range (len(dividend)):
        f.append(int(dividend[i]))
    p = []
    for i in range (len(divisor)):
        p.append(int(divisor[i]))
        
    while len(p) <= len(f):
        c = f.pop(0)
        if c==1:
            for j in range(len(p)-1):
                if f[j] == p[j+1]:
                    f[j] = 0
                else:
                    f[j] = 1
                    
    remainder = ""
    for i in range (len(f)):
        remainder = remainder + str(f[i])           
    return remainder

poly_code = '100000100110000010001110110110111' #CRC-32 codeword

f = open("f_err.txt","r")
message = f.read()
f.close

flag = '01111110'
m = message[8:len(message)-8]    
frames = map(str, m.split('0111111001111110'))
output = map(str, m.split('0111111001111110'))

for i in range(len(frames)):
    temp = frames[i]
    frames[i] = temp.replace("111110", "11111")

ft = open("f_detect.txt","w")
for i in range(len(frames)):
    if frames[i] != "":
        remainder = divide(frames[i], poly_code)
        ft.write(flag+output[i]+flag+'\n')
        error = remainder.find("1")
        if error != -1:
            ft.write("1"+'\n')
        else:
            ft.write("0"+'\n')
        
ft.close()
