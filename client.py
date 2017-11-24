#!/usr/bin/env python3

import telethon
import api
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
from time import sleep


client = telethon.TelegramClient('backup', api.api_id, api.api_hash)
client.connect()

def get_chats() -> tuple:


	dialogs = []
	users = []
	chats = []

	last_date = None
	chunk_size = 20
	while True:
	    result = client(GetDialogsRequest(
	                 offset_date=last_date,
	                 offset_id=0,
	                 offset_peer=InputPeerEmpty(),
	                 limit=chunk_size
	             ))
	    dialogs.extend(result.dialogs)
	    users.extend(result.users)
	    chats.extend(result.chats)
	    if not result.messages:
	        break
	    last_date = min(msg.date for msg in result.messages)
	    sleep(2)

	return tuple(dialogs,users,chats)

def get_history(chat) -> tuple:

	total = 0
	messages = []
	senders = []

	last_date = None
	chunk_size = settings.chunk_size

	while True:
		result = client.get_message_history(chat,limit=chunk_size,offset_date=last_date,offset_peer=InputPeerEmpty())
		total += result[0]
		messages.extend(result[1])
		senders.extend(result[2])
		if not result[1]:
			break
		last_date = min(msg.date for msg in result[1])
		sleep(2)

	return tuple(total,messages,senders)