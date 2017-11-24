import telethon
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
from time import sleep
import multiprocessing
import json

API_ID=
API_HASH=
global client # Dirty hack.

def clientLogin(api_id: int,api_hash: str) -> object: # TODO: Support 2FA.
	client = telethon.TelegramClient(session='backup', api_id, api_hash) # Start a TelegramClient
	try:
		client.connect()
		if client.is_user_authorized():  # Check if user is logon
			return client
		else:
			print("It appears we don't have your Telegram Session, Now we will try log you in.")
			phone = input('Please enter you Telegram phone number: ')
			client.send_code_request(phone) # Request phone number
			client.sign_in(phone, input('Please enter the code you recieved')) # Login with verify code
			return client
	except Exception as e:
		print('Unexcepted error %e', e)


def getDialog() -> tuple: # Copy code from https://github.com/LonamiWebs/Telethon/wiki/Retrieving-all-dialogs

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

def dumpHistory(l: list) -> list:
	def extractMessage(dialog: object) -> list:
		try:
			t,m,s = client.get_message_history(dialog.peer,limit=None) # Assign messages to m, t is total number.
			return m
		except Exception as e:
			print(e)

	try:
		pool = multiprocessing.Pool()	# Use multiprocess pool for map operation.
		mapobj = pool.map(extractMessage,l)
		pool.close()
		return list(mapobj)
	except Exception as e:
		print(e)

def output(user: object, l: list):
	def getUsername(peer: object) -> str:
		u = client.getentity(peer)
		first_name = u.first_name
		last_name = u.last_name
		if first_name:		# Use first_name + last_name if available, otherwise use userid.
			if last_name:
				return first_name+' '+last_name
			else:
				return first_name
		elif not (first_name or last_name):
			return u.id 
		else:
			return last_name
	
	for i in list:
		filename = getUsername()
		with open(filename, mode='w') as f:
			print("Dumping ", filename)
			json.dump([j.to_dict() for j in i],default=str,ensure_ascii=False) # Encoded UTF-8 and change object into their repr.
			


if __name__ = '__main__':
	client = clientLogin(API_ID,API_HASH)
	t=getDialog()
	for i in t[0]:
		output(i.peer,dumpHistory(i))


