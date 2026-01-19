from user_store import load_users
from utils.hashing import hash_algorithm
import users

def user_login():
    username = input("Enter username: ").strip().lower()
    password = input("Enter password: ")
    data = load_users()
    if username in data[users]:
        login_hashes_password = hash_algorithm(password)
        if login_hashes_password == 

