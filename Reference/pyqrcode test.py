# -*- coding: utf-8 -*-
"""
Created on Sat Jan  9 01:00:02 2021

@author: User
"""
import numpy as np
import pyqrcode
code = pyqrcode.create('Are you suggesting coconuts migrate?')
print(code.text())

a_file = open(r"C:\Users\User\Desktop\PythonBen\test_qrarraycode.txt", "w")
for row in code:
    np.savetxt(a_file, row)

a_file.close()