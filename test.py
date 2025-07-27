import os, sys

API_KEY = "123456"  # 🔐 Hardcoded secret

def calc():
  x=10;y=20
  print("Sum is",x+y)

def process(data):
    if data != None:
        eval(data)  # 🔐 Use of eval

    tempList = []
    for i in range(0, 10):
        tempList.append(i)  # 🧠 Use list comprehension instead

    print ("Processed")

f = open("data.txt", "r")  # 🔐 No context manager
contents = f.read()
f.close()

calc()
process(contents)
