import math
import binascii
import numpy as np
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


def text_to_bits(text, encoding='utf-8', errors='surrogatepass'):
    bits = bin(int(binascii.hexlify(text.encode(encoding, errors)), 16))[2:]
    return bits.zfill(8 * ((len(bits) + 7) // 8))

def bit_stuffing(x):
    count = 0
    string = ""
    for i in range(0,len(x)):
        ch = x[i]
        if ch=='1':
            count += 1
            if count<5:
                string += ch
            else:
                string = string+ch+'0'
                count = 0
        else:
            string += ch
            count = 0
    return string

poly_code = '100000100110000010001110110110111' #CRC-32 codeword

f = open("F.txt","r") 
message = f.read()
f.close()

finalstring = text_to_bits(message)

n=400
upper = int(math.ceil(float(len(finalstring))/n))

output = []
flag = '01111110'
strzeros =""
strzeros = strzeros.zfill(len(poly_code)-1)

if len(finalstring)>n:    
    for i in range(0,len(finalstring),n):
        inter = finalstring[i:i+n]
        output.append(inter)
else: 
    output.append(finalstring)
     
ft = open("F_send.txt","w") 
for i in range(len(output)):
    temp = output[i] + strzeros
    res = divide(temp, poly_code)
    x = output[i] + res
    remain = divide(x, poly_code)
    body = bit_stuffing(x)
    frame = flag + body + flag
    ft.write(frame)

ft.close()