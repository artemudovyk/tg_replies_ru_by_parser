import asyncio
from telethon import TelegramClient
from telethon import functions, types
from telethon.errors.rpcerrorlist import MsgIdInvalidError
from datetime import datetime, timedelta
from google_sheets import write_to_google, read_all_phone_numbers
import settings
import requests
import time

# Use your own values from my.telegram.org
api_id = settings.TELEGRAM_API_ID
api_hash = settings.TELEGRAM_API_HASH

base_server_url = 'https://spam-okupantiv-tgbot.udovyk.dev'
# base_server_url = 'http://127.0.0.1:8000'

tg_groups = [
    'toncoin_rus',
    'DeCenter',
    'forklog',
    'givemetonru',
    'incrypted',
    'kriptokondrashov',
    'prometheus',
    'MinterNetwork',
    'ikniga',
    'alexanderpalienko',
    'championat',
    'offsider',
    'myachPRO',
    'tribuna_by',
    'spartakkb',
    'all_about_nba',
    'united_manchester',
    'eurosportru'
]

client = TelegramClient('udovyk', api_id, api_hash)

def save_to_db(phone, username):
    url = f"{base_server_url}/post_contact/"

    payload = {
        "phone": phone,
        "username": username
    }
    headers = {"Content-Type": "application/json"}

    while True:
        try:
            response = requests.request("POST", url, json=payload, headers=headers)
            break
        except requests.exceptions.ConnectTimeout:
            time.sleep(3)
            
    print(response)
    
    return response


def save_to_db_batch(users):
    url = f"{base_server_url}/post_contact_batch/"

    payload = {
        "users": users
    }
    headers = {"Content-Type": "application/json"}

    while True:
        try:
            response = requests.request("POST", url, json=payload, headers=headers)
            break
        except requests.exceptions.ConnectTimeout:
            time.sleep(3)
            
    print(response)
    
    return response


def get_all_phone_numbers():
    url = f"{base_server_url}/get_phone_numbers/"

    response = requests.request("GET", url)
    phone_numbers = response.json()['phone_numbers']

    return phone_numbers


async def main():      
    phone_numbers = set(get_all_phone_numbers())
    print(phone_numbers)
    
    for group in tg_groups:
        messages = []
        
        async for message in client.iter_messages(group, limit=3000):
            messages.append((group, message))
            
        stack_to_save_in_db = []
        for group, message in messages:
            try:
                async for reply in client.iter_messages(group, reply_to=message.id, limit=2000):
                    user = await reply.get_sender()
                    try:
                        if user.phone and user.phone not in phone_numbers and (user.phone.startswith('7') or user.phone.startswith('375')):
                            print(user.phone, user.username)
                            phone_numbers.add(user.phone)
                            stack_to_save_in_db.append({
                                "phone": user.phone, 
                                "username": user.username
                            })
                            # print(f'{user.phone} skipped')
                    except AttributeError:
                        continue
            except MsgIdInvalidError: 
                continue
            
            # Save all new contacts to db if it's not empty
            if stack_to_save_in_db:
                save_to_db_batch(stack_to_save_in_db)


if __name__ == "__main__":
    # get_all_phone_numbers()
    with client:
        client.loop.run_until_complete(main())