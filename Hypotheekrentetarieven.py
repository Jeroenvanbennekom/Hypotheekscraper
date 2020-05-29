from bs4 import BeautifulSoup
import requests
from database import drop_table, create_table, insert_values, delete_duplicate_records
import random
import time 

looptijden = ("1", "2", "3", "5", "6", "7", "10", "12", "15", "17", "20", "25", "30")

#Stel een wachtperiode in van een willekeurig aantal seconden tussen 30 en 31. 
delay = 1 + random.random()


def scrape_hypotheekrentetarieven():
	for looptijd in looptijden:
		scrape_script_fixed_period(looptijd)
	scrape_script_var_period()

def scrape_script_fixed_period(looptijd):
	try:
		#Scrape results for all fixed looptijden. 
		url = f"https://www.hypotheekrente.nl/rente/{looptijd}-jaar-rentevast/nhg/#overzicht"
		page_fetch = requests.get(url, timeout = 5)
		page_content = BeautifulSoup(page_fetch.content, "html.parser")
		rows = page_content.find_all('tr')
		for row in rows:
			cols=row.find_all('td')
			cols=[x.text.strip() for x in cols]
			#Add only rows with a column for all tariffs and name of the 'verstrekker'. This is to filter empty rows and adverts. 
			if len(cols)==8:
				Hypotheekverstrekker = cols[1]
				nhg = cols[2]
				ltv60 = cols[3]
				ltv80 = cols[4]
				ltv90 = cols[5]
				ltv100 = cols[6]
				insert_values(Hypotheekverstrekker, looptijd, nhg, ltv60, ltv80, ltv90, ltv100)
		print(f'done with scraping for looptijd {looptijd}')
		#Sleep for 1.x seconds to avoid overstressing server		
		time.sleep(delay)
	except:
		# Here I should add code to send an e-mail if something is wrong. 
		print('Something went wrong with scraping for fixed period. Fix it')

def scrape_script_var_period():
	try:
		#Scrape results for variable looptijd
		url = f"https://www.hypotheekrente.nl/rente/variabele-rente/nhg/#overzicht"
		page_fetch = requests.get(url, timeout = 5)
		page_content = BeautifulSoup(page_fetch.content, "html.parser")
		rows = page_content.find_all('tr')
		for row in rows:
			cols=row.find_all('td')
			cols=[x.text.strip() for x in cols]
			#Add only rows with a column for all tariffs and name of the 'verstrekker'. This is to filter empty rows and adverts. 
			if len(cols)==8:
				looptijd = '0'
				Hypotheekverstrekker = cols[1]
				nhg = cols[2]
				ltv60 = cols[3]
				ltv80 = cols[4]
				ltv90 = cols[5]
				ltv100 = cols[6]
				insert_values(Hypotheekverstrekker, looptijd, nhg, ltv60, ltv80, ltv90, ltv100)
		print('Done with scraping for variable tariffs')
	except:
		# Here I should add code to send an e-mail if something is wrong. 
		print('Something went wrong with scraping for var period. Fix it')

# drop_table()
#create_table()
scrape_hypotheekrentetarieven()
#delete_duplicate_records()

