import requests
from bs4 import BeautifulSoup
import json
import os
import pandas as pd
from tabulate import tabulate
import sys

enrollment_number = '' # Enter your enrollment number
month = '' # Enter session - month. Example - December
year = '' # Enter session -year. Example - 2023

def fetch_marks(enrollment_number, month, year):
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

def load_existing_marks():
    if os.path.exists('results.json') and os.path.getsize('results.json') > 0:
        with open('results.json', 'r') as file:
            return json.load(file)
    return []

def save_marks(data):
    with open('results.json', 'w') as file:
        json.dump(data, file, indent=4)

def pretty_print(data):
    df = pd.DataFrame(data)
    print(tabulate(df, headers='keys', tablefmt='pretty', showindex=False))

response_text = fetch_marks(enrollment_number, month, year)

if response_text is None:
    existing_marks = load_existing_marks()
    if existing_marks:
        print("\nDISPLAYING OLD RESULTS. PLEASE CHECK YOUR INTERNET\n")
        pretty_print(existing_marks)
    else:
        print("\nPLEASE CHECK YOUR INTERNET. NO OLD DATA FOUND!\n")
    sys.exit(1)

soup = BeautifulSoup(response_text, 'html.parser')

table_rows = soup.find('table').find_all('tr')
data = []
for row in table_rows:
    cols = [col.text.strip() for col in row.find_all('td')]
    data.append(cols)

existing_marks = load_existing_marks()

new_marks = []
header_row = data[0]
for row in data[1:]:
    row_dict = dict(zip(header_row, row))
    if row_dict not in existing_marks:
        new_marks.append(row_dict)
existing_marks.extend(new_marks)

save_marks(existing_marks)

if new_marks:
    print("\nMARKS OUT FOR THE SUBJECT(S) \n")
    pretty_print(new_marks)
else:
    print("\nNO NEW MARKS ARE OUT. DISPLAYING OLD DATA...\n")
    pretty_print(existing_marks)
