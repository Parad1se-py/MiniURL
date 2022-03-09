import os
import string
import random

from dotenv import load_dotenv
from pymongo import MongoClient

from app import url

# load .env file
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")

# connection with the databse
client = MongoClient(MONGO_URI)
db = client.miniurl
collection = db.urls

def create_account(email:str, passw:str):
    """Create a new account if not already existing

    Args:
        email (str): email of the account
        passw (str): password of the account

    Returns:
        list: 0th element returns True, 1st element returns mongodb account object
    """
    if bool(db.collection.find_one( {"_id": email} )):
        return [False, 'Account already exists']
    
    obj = {
            "id_": email,
            "password": passw,
            "urls": {},
            "free": 5,
            "paid": 0
        }

    db.collection.insert_one(
        obj
    )

    return [True, obj]

def add_url(account:str, long:str, short:str, free:bool):
    """Add a new URL to the account

    Args:
        account (str): email of the account
        long (str): the actual URL
        short (str): the short version of the URL
        free (bool): True if the URL is free, False if it is paid for

    Returns:
        list: 0th element returns bool (True/False), 1st element returns statement
    """
    if not bool(db.collection.find_one( {"_id": account} )):
        return [False, 'Account not found']

    for i in db.collection.find_one( {"_id": account} )['urls']:
        if i['long'] == long:
            return [False, 'URL already exists']
        
    collection.update(
        {'email': account},
        {'$set': {f'urls.{short}': {
            'long'  : long,
            'short' : short,
            'clicks': 0
        }}}
    )

    if free:
        collection.update(
            {'email': account},
            {'$inc': {'free': -1}}
        )
    else:
        collection.update(
            {'email': account},
            {'$inc': {'paid': -1}}
        )

    return [True, 'Worked']

def delete_url(account:str, short:str, free:bool):
    """Delete a URL from the account if it exists.

    Args:
        account (str): email of the account
        short (str): the short version of the URL
        free (bool): True if the URL is free, False if it is paid for

    Returns:
        list: 0th element returns bool (True/False), 1st element returns statement
    """    
    if not bool(db.collection.find_one( {"_id": account} )):
        return [False, 'Account not found']
    
    for i in db.collection.find_one( {"_id": account} )['urls']:
        if i['short'] == short:
            collection.update(
                {'email': account},
                {'$unset': {f'urls.{short}': 1}}
            )
            if free:
                collection.update(
                    {'email': account},
                    {'$inc': {'free': 1}}
                )
            return [True, 'Worked']
        else:
            continue

    return [False, 'URL already exists']

def check_if_exists(short:str):
    """Check if the short url already exists

    Args:
        short (str): the short version of the URL

    Returns:
        bool: True if the URL exists, False if it doesn't
    """
    return any(short in i['urls'] for i in collection.find())

def create_url():
    """Creates a new random url

    Returns:
        str: the new random url
    """
    letters = string.ascii_lowercase + string.ascii_uppercase
    while True:
        rand_letters = random.choices(letters, k=3)
        rand_letters = "".join(rand_letters)
        if not check_if_exists(rand_letters):
            return rand_letters