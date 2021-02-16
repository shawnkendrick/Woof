#!/usr/bin/env python3

import requests
import datetime
import smtplib, ssl
from bs4 import BeautifulSoup


search_distance = '50'
apa_dog_listing = []
apa_listings_text = []
apa_listings_links = []
apa_query_url = 'https://petharbor.com/results.asp?searchtype=ADOPT&zip=63101&miles=' + search_distance + '&shelterlist=%27APMO%27&where=type_DOG&PAGE=1'

def getAPASoup():
    try:
        apa_req = requests.get(apa_query_url)
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)  
    apa_soup = BeautifulSoup(apa_req.text, 'html.parser')
    apa_dog_listing = []
    table = apa_soup.find('table', {'class': 'ResultsTable'}) 
    rows = table.find_all('tr') 
    apa_listing_email = ''
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        apa_dog_listing.append([ele for ele in cols if ele]) 
    for i in apa_dog_listing:
        apa_listing_email += 'Name: ' + i[1] + '\n' + 'Gender: ' + i[2] + '\n' + 'Color: ' + i[3] + '\n' + 'Breed: ' + i[4] + '\n\n'
    sendEmail(apa_listing_email)                        

def sendEmail(apa_listing_email):    
    port = 465  
    smtp_server = "smtp.gmail.com"
    sender_email = "mymail@gmail.com" 
    receiver_email = "mymail@gmail.com" 
    password = input("Type your password and press enter: ")
    message = apa_listing_email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)


getAPASoup()         