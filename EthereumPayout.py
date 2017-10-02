import requests, bs4, ctypes, re

#Scrapes DwarfPool's HTML page for a given wallet address
dwarfRes = requests.get('http://dwarfpool.com/eth/address?wallet=0x737C57933Ba27aD9e5B048B497c04aBC3750295B')
dwarfRes.raise_for_status()
dwarfSoup = bs4.BeautifulSoup(dwarfRes.text, "html.parser")
ethRegex = re.compile(r'\d.\d{8} ')

#Scrapes EthereumPrice's HTML page for the current price in USD
priceRes = requests.get('https://ethereumprice.org/')
priceRes.raise_for_status()
priceSoup = bs4.BeautifulSoup(priceRes.text, "html.parser")
priceRegex = re.compile(r'\d{3}.\d{2}')

#Accesses classes of the HTML containing the data and searches for regex matches
priceElem = priceSoup.select('.rp')
priceMatch = priceRegex.search(str(priceElem))
ethPrice = priceMatch.group()
dwarfElem = dwarfSoup.select('.badge-money')
dwarfMatches = ethRegex.findall(str(dwarfElem))

#The following is a band-aid fix for DwarfPool adding additional HTML elements sometimes
if len(dwarfMatches) < 6:
	currentBalance = dwarfMatches[0]
	confirmedNotBalance = 0
	alreadyPaid = dwarfMatches[1]
	unconfirmed = dwarfMatches[2]
	earnings24hr = dwarfMatches[3]
else:
	currentBalance = float(dwarfMatches[0])
	confirmedNotBalance = float(dwarfMatches[1])
	alreadyPaid = float(dwarfMatches [2])
	unconfirmed = float(dwarfMatches[3])
	earnings24hr = float(dwarfMatches [4])
	
totalEth = float(currentBalance) + float(unconfirmed)
usdAmount = float(totalEth) * float(ethPrice)
walletBal = (float(totalEth) + float(alreadyPaid)) * float(ethPrice)

#Formats and outputs a string containing the data
outputString = ''
outputString += ("Current Balance: %.5f" % float(currentBalance) + " ETH\n")
outputString += ("Pending Balance: %.5f" % float(unconfirmed) + " ETH\n")
outputString += ("Total: %.5f" % totalEth + " ETH\n")
outputString += ("USD Payout: $%.3f" % usdAmount + "\n\n\n") 
outputString += ("Wallet Balace: %.5f" % (float(walletBal)/float(ethPrice)) + " ETH\n")
outputString += ("USD Balance: $%.3f" % walletBal + "\n")
ctypes.windll.user32.MessageBoxW(0, outputString, "Ethereum Payout ($" + ethPrice + ")", 1)