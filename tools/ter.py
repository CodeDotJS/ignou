import requests
from bs4 import BeautifulSoup
import json
import os
from dotenv import load_dotenv

load_dotenv()

payload = {'eno': os.getenv('ENO'), 'myhide': 'OK'}
response = requests.post("https://termendresult.ignou.ac.in/TermEndDec23/TermEndDec23.asp", data=payload)
soup = BeautifulSoup(response.text, 'html.parser')

table_rows = soup.find('table').find_all('tr')
data = []
for row in table_rows:
    cols = [col.text.strip() for col in row.find_all('td')]
    data.append(cols)

existing_data = []
if os.path.exists('results.json') and os.path.getsize('results.json') > 0:
    with open('results.json', 'r') as file:
        existing_data = json.load(file)

new_data = []
header_row = data[0]
for row in data[1:]:
    row_dict = dict(zip(header_row, row))
    if row_dict not in existing_data:
        new_data.append(row_dict)
existing_data.extend(new_data)

with open('results.json', 'w') as file:
    json.dump(existing_data, file, indent=4)

if new_data:
    print("New data appended to results.json.")
else:
    print("No new data found.")
