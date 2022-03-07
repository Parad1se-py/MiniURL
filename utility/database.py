from cgitb import html
import os
import random
import string

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
            "free": 5
        }

    db.collection.insert_one(
        obj
    )

    return [True, obj]

def add_url(account:str, long:str, short:str):
    """Add a new URL to the account

    Args:
        account (str): email of the account
        long (str): the actual URL
        short (str): the short version of the URL

    Returns:
        list: 0th element returns Boolean (True/False), 1st element returns statement
    """
    if not bool(db.collection.find_one( {"_id": account} )):
        return [False, 'Account not found']

    for i in db.collection.find_one( {"_id": account} )['urls']:
        if i['long'] == long:
            return [False, 'URL already exists']

    collection.update(
        {'email': account},
        {'$set': {f'urls.{short}': {
            'long':long,
            'short':short,
            'clicks':0
            }}}
    )

    return [True, 'Worked']

def delete_url(account:str, short:str):
    """Delete a URL from the account if it exists.

    Args:
        account (str): email of the account
        short (str): the short version of the URL

    Returns:
        list: 0th element returns Boolean (True/False), 1st element returns statement
    """    
    if not bool(db.collection.find_one( {"_id": account} )):
        return [False, 'Account not found']
    
    for i in db.collection.find_one( {"_id": account} )['urls']:
        if i['short'] == short:
            collection.update(
                {'email': account},
                {'$unset': {f'urls.{short}': 1}}
            )
            return [True, 'Worked']
        else:
            continue

    return [False, 'URL already exists']