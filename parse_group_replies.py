import asyncio
from telethon import TelegramClient
from telethon import functions, types
from telethon.errors.rpcerrorlist import MsgIdInvalidError
from datetime import datetime, timedelta
from google_sheets import write_to_google, read_all_phone_numbers
import settings

# Use your own values from my.telegram.org
api_id = settings.TELEGRAM_API_ID
api_hash = settings.TELEGRAM_API_HASH

tg_groups = [
    # 'toncoin_rus',
    # 'DeCenter',
    # 'forklog',
    # 'givemetonru',
    # 'incrypted',
    # 'kriptokondrashov',
    # 'prometheus',
    # 'MinterNetwork',
    # 'ikniga',
    # 'alexanderpalienko',
    # 'championat',
    'offsider',
    'myachPRO',
    'tribuna_by',
    'spartakkb',
    'all_about_nba',
    'united_manchester',
    'eurosportru'
]

client = TelegramClient('udovyk', api_id, api_hash)

async def main():      
    phone_numbers = set(read_all_phone_numbers())
    print(phone_numbers)
    
    for group in tg_groups:
        messages = []
        
        async for message in client.iter_messages(group, limit=3000):
            messages.append((group, message))
            
        
        for group, message in messages:
            try:
                async for reply in client.iter_messages(group, reply_to=message.id, limit=2000):
                    user = await reply.get_sender()
                    try:
                        if user.phone and user.phone not in phone_numbers:
                            print(user.phone)
                            phone_numbers.add(user.phone)
                            write_to_google(user.phone, user.username)
                    except AttributeError:
                        continue
            except MsgIdInvalidError: 
                continue

with client:
    client.loop.run_until_complete(main())
