# -*- coding: utf-8 -*-
"""
Created on Sat Jan  9 01:32:52 2021

@author: User
"""
import base64

def base64ToString(b):
    return base64.b64decode(b).decode('utf-8')

with open(r"C:\Users\User\Desktop\PythonBen\qrcode002.png", "rb") as imageFile:
    string = base64.b64encode(imageFile.read())
    #print (string)
    #print(type(string))
    
a = str(string)
print(a)

a_file = open(r"C:\Users\User\Desktop\PythonBen\test_qrarraybase64.txt", "w")
a_file.write(a)

a_file.close()