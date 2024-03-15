import requests
from bs4 import BeautifulSoup
import json
import os
import pandas as pd
from tabulate import tabulate
import sys


def fetch_data(enrollment_number, month, year):
    try:
        base_url = "https://termendresult.ignou.ac.in/"
        if month.lower() == 'december':
            month_str = 'Dec'
        else:
            month_str = month
        url = f"{base_url}TermEnd{month_str}{year[2:]}/TermEnd{month_str}{year[2:]}.asp"

        payload = {'eno': enrollment_number, 'myhide': 'OK'}
        response = requests.post(url, data=payload)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        return None

def load_existing_data():
    if os.path.exists('results.json') and os.path.getsize('results.json') > 0:
        with open('results.json', 'r') as file:
            return json.load(file)
    return []

def save_data(data):
    with open('results.json', 'w') as file:
        json.dump(data, file, indent=4)

def pretty_print(data):
    df = pd.DataFrame(data)
    print(tabulate(df, headers='keys', tablefmt='pretty', showindex=False))

enrollment_number = 'YOUR ENROLLMENT NUMBER'
month = 'SESSION - MONTH'
year = 'SESSION - YEAR'

response_text = fetch_data(enrollment_number, month, year)

if response_text is None:
    existing_data = load_existing_data()
    if existing_data:
        print("\nDISPLAYING OLD RESULTS. PLEASE CHECK YOUR INTERNET\n")
        pretty_print(existing_data)
    else:
        print("\nPLEASE CHECK YOUR INTERNET. NO OLD DATA FOUND!\n")
    sys.exit(1)

soup = BeautifulSoup(response_text, 'html.parser')

table_rows = soup.find('table').find_all('tr')
data = []
for row in table_rows:
    cols = [col.text.strip() for col in row.find_all('td')]
    data.append(cols)

existing_data = load_existing_data()

new_data = []
header_row = data[0]
for row in data[1:]:
    row_dict = dict(zip(header_row, row))
    if row_dict not in existing_data:
        new_data.append(row_dict)
existing_data.extend(new_data)

save_data(existing_data)

if new_data:
    print("\nMARKS OUT FOR THE SUBJECT(S) \n")
    pretty_print(new_data)
else:
    print("\nNO NEW MARKS ARE OUT. DISPLAYING OLD DATA...\n")
    pretty_print(existing_data)
