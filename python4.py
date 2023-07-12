import argparse
import requests
import csv
import pandas as pd
from datetime import datetime

url = "https://api.baubuddy.de/index.php/login"
payload = {
    "username": "365",
    "password": "1"
}
headers = {
    "Authorization": "Basic QVBJX0V4cGxvcmVyOjEyMzQ1NmlzQUxhbWVQYXNz",
    "Content-Type": "application/json"
}
response = requests.request("POST", url, json=payload, headers=headers)
data = response.json()
#print(response.text)

if "oauth" in data and "access_token" in data["oauth"]:
    access_token = data["oauth"]["access_token"]
    print("Access Token:", access_token)

    headers["Authorization"] = f"Bearer {access_token}"

else:
    print("Authorization failed. Response:", response.text)


parser = argparse.ArgumentParser()
parser.add_argument('-k', '--keys', nargs='+', type=str, help='Input keys')
parser.add_argument('-c', '--colored', action='store_true', help='Enable row coloring')
args = parser.parse_args()
keys = args.keys if args.keys else []
colored = args.colored


csv_file_path = 'C:\\Users\\Ivan\\Downloads\\vehicles.csv'  
data = []
with open(csv_file_path, 'r') as file:
    reader = csv.DictReader(file)
    data = list(reader)


url = 'https://api.baubuddy.de/dev/index.php/v1/vehicles/select/active'  
files = {'file': open(csv_file_path, 'rb')}
response = requests.post(url, files=files)


if response.status_code == 200:
    server_response = response.json()
else:
    print('Request failed with status code:', response.status_code)


df = pd.DataFrame(server_response)


df.sort_values(by='gruppe', inplace=True)  
df = df[['rnr'] + keys]  

if colored:
    def color_row(row):
        if row['hu'] <= 3:
            return ['background-color: #007500'] * len(row)
        elif row['hu'] <= 12:
            return ['background-color: #FFA500'] * len(row)
        else:
            return ['background-color: #b30000'] * len(row)

    df = df.style.apply(color_row, axis=1)


current_date_iso_formatted = datetime.now().strftime("%Y-%m-%d")
excel_file_path = f'vehicles_{current_date_iso_formatted}.xlsx'
df.to_excel(excel_file_path, index=False)

print('Excel file generated successfully.')