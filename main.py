from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
import re

app = Flask(__name__)

def fetch_and_process_data(url, enrollment):
    try:
        payload = {'eno': enrollment, 'myhide': 'OK'}
        response = requests.post(url, data=payload)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table')

        enrol_pattern = r'Enrolment Number:\s*(\d+)'
        enrol_match = re.search(enrol_pattern, response.text)[1]

        program_pattern = r'Program:\s*([A-Z]+)'
        program_match = re.search(program_pattern, response.text)[1]

        title = soup.find('title').text.strip()
        status = soup.find('font', size='-1').text.strip()

        additional_info = {
            "title": title,
            "status": status,
            "enrollment_number": enrol_match,
            "program": program_match
        }

        if not table:
            return None, None
        table_rows = table.find_all('tr')
        header_row = [col.text.strip() for col in table_rows[0].find_all('td')]
        data = []
        for row in table_rows[1:]:
            row_data = [col.text.strip() for col in row.find_all('td')]
            row_dict = dict(zip(header_row, row_data))
            data.append(row_dict)
        return data, additional_info
    except Exception as e:
        print(f"Error occurred: {e}")
        return None, None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/fetch_data', methods=['POST'])
def fetch_data():
    try:
        url = request.form['url']
        enrollment = request.form['enrollment']
        data, additional_info = fetch_and_process_data(url, enrollment)
        if data is None:
            return "Error occurred while fetching result."
        return render_template('result.html', data=data, additional_info=additional_info)
    except Exception as e:
        return f"Error occurred while processing result: {e}"

if __name__ == '__main__':
    app.run(debug=True)
