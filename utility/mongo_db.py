# -*- coding: utf-8 -*-
# Copyright (c) 2022 Arjun Ladha

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Helper functions for managing mongo-db."""

import os
import string
import random

from dotenv import load_dotenv
from pymongo import MongoClient

# load .env file
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")

# connection with the database
client = MongoClient(MONGO_URI)
db = client.miniurl
urls = db.urls

def create_account(_id:str, username:str, passw:str):
    """Create a new account if not already existing

    Args:
        _id (str): _id of the account
        username (str): username of the account
        passw (str): password of the account

    Returns:
        list: 0th element returns True, 1st element returns mongodb account object
    """
    if bool(urls.find_one( {"_id": _id} )):
        return [False, 'Account already exists']

    urls.insert_one(
        {
            "_id": _id,
            "password": passw,
            "username": username,
            "urls": {},
            "free": 5,
            "paid": 0
        }
    )

    return [True, urls.find_one( {"_id": _id} )]

def delete_account(_id:str):
    """Delete an existing account

    Args:
        _id (str): the _id of the account

    Returns:
        list: 0th element returns bool (True/False), 1st element returns statement
    """
    if not bool(urls.find_one( {"_id": _id} )):
        return [False, 'Account not found']
    
    urls.delete_one(
        { "_id": _id }
    )
    return [True, 'Account successfully deleted']

def add_url(account:str, long:str, short:str, free:bool):
    """Add a new URL to the account

    Args:
        account (str): _id of the account
        long (str): the actual URL
        short (str): the short version of the URL
        free (bool): True if the URL is free, False if it is paid for

    Returns:
        list: 0th element returns bool (True/False), 1st element returns statement
    """
    if not bool(urls.find_one( {"_id": account} )):
        return [False, 'Account not found']

    for i in urls.find_one( {"_id": account} )['urls']:
        if i['long'] == long:
            return [False, 'URL already exists']
    
    urls.update_one(
        {'_id': account},
        {'$set': 
            {f'urls.{short}': long}
        }
    )

    if free:
        urls.update_one(
            {'_id': account},
            {'$inc': 
                {'free': -1}
            }
        )
    else:
        urls.update_one(
            {'_id': account},
            {'$inc':
                {'paid': -1}
            }
        )

    print('Added')
    return [True, 'Worked']

def delete_url(account:str, short:str, free:bool):
    """Delete a URL from the account if it exists.

    Args:
        account (str): _id of the account
        short (str): the short version of the URL
        free (bool): True if the URL is free, False if it is paid for

    Returns:
        list: 0th element returns bool (True/False), 1st element returns statement
    """    
    if not bool(urls.find_one( {"_id": account} )):
        return [False, 'Account not found']

    for i in urls.find_one( {"_id": account} )['urls']:
        if i['short'] == short:
            if free:
                urls.update_one(
                    {'_id': account},
                    {'$inc': {'free': 1}}
                )
            else:
                urls.update_one(
                    {'_id': account},
                    {'$inc': {'paid': 1}}
                )
            urls.update_one(
                {'_id': account},
                {"$pull": {'urls': {'short': short}}}
            )
            return [True, 'Worked']
        else:
            continue

def check_if_exists(short:str):
    """Check if the short url already exists

    Args:
        short (str): the short version of the URL

    Returns:
        bool: True if the URL exists, False if it does not
    """
    return bool(urls.find_one( {}, {f'urls.{short}'} ))

def create_url():
    """Creates a new random url

    Returns:
        str: the new random url
    """
    letters = string.ascii_lowercase + string.ascii_uppercase + string.digits
    while True:
        rand_letters = random.choices(letters, k=5)
        rand_letters = "".join(rand_letters)
        if not check_if_exists(rand_letters):
            print(rand_letters)
            return rand_letters

def get_long_url(short:str):
    """Get the long version of the URL. Returns False if the URL does not exist

    Args:
        short (str): the short url

    Returns:
        str: the long version of the url
    """
    try:
        pair = urls.find_one({}, {f'urls.{short}'} )
        return str(pair['urls'][short])
    except KeyError:
        return False
    
def get_all_docs():
    """Returns all documents existing in the database

    Args:
        None

    Returns:
        list: all the documents existing in the database
    """
    docs = []
    doc_count = urls.count_documents({})
    for _ in range(doc_count):
        docs.extend(iter(urls.find()))
    return docs