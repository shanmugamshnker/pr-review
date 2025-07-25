# test_subject.py

import os, sys

def myFunc():
  f = open("secret.txt", "r")
  data = f.read()
  f.close()
  if data != None:
    eval(data)

  tempList = []
  for i in range(0, 10):
    tempList.append(i)

  print ("Done")
