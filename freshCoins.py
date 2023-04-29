#!/usr/bin/env python3

import requests, re, time, os, chime, subprocess
from termcolor import colored
import json as ijson

yourCoinMarketCapAPIKey = 'Your API KEYYY'
sleepTime = 120 # seconds
numberOfTokens = 3 # n + n To fit on screen

try:
	subprocess.run(['aplay','--version'], check = True)
except (OSError, subprocess.SubprocessError, subprocess.CalledProcessError):
	print ('aplay is missing. please install alsa-utils')
	exit()

chime.theme('zelda')

newCoinGeckoTracker = ""
newCoinNccTracker = ""

nccHeaders = {
	'Accepts': 'application/json',
	'X-CMC_PRO_API_KEY': yourCoinMarketCapAPIKey
}

scrapeHeaders = {
	'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
}

nccSession = requests.Session()
nccSession.headers.update(nccHeaders)

scrapeSession = requests.Session()
scrapeSession.headers.update(scrapeHeaders)

def fetchCoinMarketCap(itter):

	print( colored( "\n<< CoinMarketCap\n", 'green', attrs=["bold"] ) )

	global nccSession
	global scrapeSession
	global newCoinNccTracker

	nccurl = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/map'

	nccparam = {
		'listing_status':'active',
		'aux':'platform'
	}

	try:
		nccRes = nccSession.get(nccurl, params=nccparam)
		coins = ijson.loads(nccRes.text)['data']
	except (requests.exceptions.ConnectionError, requests.exceptions.Timeout, requests.exceptions.TooManyRedirects) as er:
		print(er)

	cnt = 0

	try:
		nccScrapeRes = scrapeSession.get('https://coinmarketcap.com/new/').text
	except (requests.exceptions.ConnectionError, requests.exceptions.Timeout, requests.exceptions.TooManyRedirects) as er:
		print(er)

	for line in nccScrapeRes.splitlines():

		if 'sc-4984dd93-0 kKpPOn' in line:

			sNames = re.findall(r'kKpPOn\">(.+?)<\/p>',line)

			for scrapedName in sNames:

				if cnt < numberOfTokens:
					
					for coin in coins:

						if coin['name'] == scrapedName and coin['platform'] and coin['platform']['name'] == 'BNB':

							if cnt == 0:
								if itter == 0:
									newCoinNccTracker = coin['name']
								else:
									if newCoinNccTracker != coin['name']:
										chime.success()
										newCoinNccTracker = coin['name']

							cnt += 1
							ctract = coin['platform']['token_address']
							
							print( '\t' + colored( str(cnt) + ". " + coin['name'], 'blue', attrs=["bold"] ) )
							print( '\t\t' + colored( ctract, 'yellow', attrs=["bold"] ) )
							print( '\t\t' + colored( 'https://www.geckoterminal.com/bsc/pools/' + ctract, 'yellow', attrs=["bold"] ) )

def fetchCoinGecko(itter):

	print( colored( "\n<< CoinGecko\n", 'green', attrs=["bold"] ) )

	global scrapeSession
	global newCoinGeckoTracker

	cnt = 0

	coins = requests.get('https://api.coingecko.com/api/v3/coins/list?include_platform=true').json()

	try:
		nccScrapeRes = scrapeSession.get('https://www.coingecko.com/en/new-cryptocurrencies').text
	except (requests.exceptions.ConnectionError, requests.exceptions.Timeout, requests.exceptions.TooManyRedirects) as er:
		print(er)

	for line in nccScrapeRes.splitlines():

		if 'py-0 coin-name' in line:

			res = re.search(r'data-sort=\'(.+?)\'>',line)

			if cnt < numberOfTokens:
				
				for coin in coins:

					if coin['name'] == res.group(1) and 'binance-smart-chain' in coin['platforms']:

						r = requests.get('https://api.coingecko.com/api/v3/coins/'+coin['id']).json()

						if cnt == 0:
							if itter == 0:
								newCoinGeckoTracker = coin['name']
							else:
								if newCoinGeckoTracker != coin['name']:
									chime.success()
									newCoinGeckoTracker = coin['name']

						cnt += 1
						ctract = r['platforms']['binance-smart-chain']
						
						print( '\t' + colored( str(cnt) + ". " + coin['name'], 'blue', attrs=["bold"] ) )
						print( '\t\t' + colored( ctract, 'yellow', attrs=["bold"] ) )
						print( '\t\t' + colored( 'https://www.geckoterminal.com/bsc/pools/' + ctract, 'yellow', attrs=["bold"] ) )

itt = 0

while True:
	os.system('cls' if os.name == 'nt' else 'clear')
	print( colored( 'New BSC Tokens', 'yellow', attrs=["bold"] ) )
	fetchCoinMarketCap(itt)
	fetchCoinGecko(itt)
	time.sleep(sleepTime)
	itt += 1