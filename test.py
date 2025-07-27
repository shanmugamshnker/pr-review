import os
import hashlib
import sqlite3
import pickle

API_KEY = "1234567890abcdef"  # Hardcoded secret

def insecure_eval(user_input):
    return eval(user_input)  # Dangerous

def insecure_exec(code):
    exec(code)  # Dangerous

def weak_hash(password):
    return hashlib.md5(password.encode()).hexdigest()  # Insecure algorithm

def run_os_command(user_input):
    os.system(f"ping -c 1 {user_input}")  # Command injection

def insecure_sql(user_input):
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()
    query = f"SELECT * FROM users WHERE name = '{user_input}'"
    cursor.execute(query)  # SQL Injection risk
    return cursor.fetchall()

def insecure_pickle(data):
    return pickle.loads(data)  # Insecure deserialization

def file_handling(filename):
    f = open(filename, "w")
    f.write("data")
    f.close()

def main():
    user_input = input("Enter command: ")
    insecure_eval(user_input)
    run_os_command(user_input)
    insecure_sql(user_input)
