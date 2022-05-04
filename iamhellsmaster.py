# -*- coding: utf8 -*-
from pyuseragents import random as random_useragent
from requests import Session
from msvcrt import getch
from os import system
from ctypes import windll
from urllib3 import disable_warnings
from loguru import logger
from sys import stderr, exit
from multiprocessing.dummy import Pool
from random import randint

class Wrong_Response(BaseException):
	def __init__(self, message):
		self.message = message

disable_warnings()
def clear(): return system('cls')
logger.remove()
logger.add(stderr, format="<white>{time:HH:mm:ss}</white> | <level>{level: <8}</level> | <cyan>{line}</cyan> - <white>{message}</white>")
windll.kernel32.SetConsoleTitleW('iamhellsmaster Auto Reger | by NAZAVOD')
print('Telegram channel - https://t.me/n4z4v0d\n')

def random_tor_proxy():
	proxy_auth = str(randint(1, 0x7fffffff)) + ':' + str(randint(1, 0x7fffffff))
	proxies = {'http': 'socks5://{}@localhost:9150'.format(proxy_auth), 'https': 'socks5://{}@localhost:9150'.format(proxy_auth)}
	return(proxies)

def take_proxies(length):
	proxies = []

	while len(proxies) < length:
		with open(proxy_folder, 'r') as file:
			for row in file:
				proxies.append(row.strip())

	return(proxies[:length])

def mainth(data):
	for _ in range(5):
		try:
			email = data[0]
			proxy = data[1]

			session = Session()
			session.headers.update({'user-agent': random_useragent(), 'accept': 'application/json', 'accept-language': 'ru,en;q=0.9,vi;q=0.8,es;q=0.7', 'content-type': 'application/json', 'origin': 'https://iamhellsmaster.com', 'referer': 'https://iamhellsmaster.com/', 'api-key': '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'})
			
			if proxy:
				if proxy_source == 2:
					session.proxies.update({'http': f'{proxy_type}://{proxy}', 'https': f'{proxy_type}://{proxy}'})

				else:
					session.proxies.update(random_tor_proxy())

			r = session.post('https://api.sendinblue.com/v3/contacts', json = {"listIds":[49],"updateEnabled":True,"email": email})

			if not r.ok:
				raise Wrong_Response()

		except Wrong_Response as error:
			logger.error(f'{email} | Wrong response: {str(error)}, response code: {str(r.status_code)}, response: {str(r.text)}')

		except Exception as error:
			logger.error(f'{email} | Unexpected error : {str(error)}')

		else:
			with open('registered.txt', 'a') as file:
				file.write(f'{email}\n')

			logger.success(f'{email} | Successfully registered')

			return

	with open('unregistered.txt', 'a') as file:
		file.write(f'{email}\n')

if __name__ == '__main__':
	threads = int(input('Threads: '))
	emails_directory = input('Drop .txt with emails: ')
	use_proxy = input('Use Proxies? (y/N): ').lower()

	with open(emails_directory, 'r') as file:
		emails_list = [row.strip() for row in file]
		proxies = [None for _ in range(len(emails_list))]

	if use_proxy == 'y':
		proxy_source = int(input('How take proxies? (1 - tor proxies; 2 - from file): '))

		if proxy_source == 2:
			proxy_type = str(input('Enter proxy type (http; https; socks4; socks5): '))
			proxy_folder = str(input('Drag and drop file with proxies (ip:port; user:pass@ip:port): '))

			proxies = take_proxies(len(emails_list))

	clear()
	pool = Pool(threads)
	result_list = pool.map(mainth, list(zip(emails_list, proxies)))

	logger.success('Работа успешно завершена!')
	print('\nPress Any Key To Exit..')
	getch()
	exit()