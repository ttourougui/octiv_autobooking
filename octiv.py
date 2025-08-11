import requests
import os

# Your Bearer token here
secret = os.getenv("OCTIV_TOKEN")
user_id = os.getenv("USER_ID") # 
class_name = os.getenv("CLASS_NAME") # 6:30, 7:30 ...
from datetime import datetime, timedelta

# Calculate the date for today + 2 days
target_date = (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d")

# Build the filter[between] parameter
filter_between = f"&filter[between]={target_date},{target_date}"

print(target_date)

url = (
    "https://api.octivfitness.com/api/class-dates"
    "?filter[tenantId]=102326" # Keep these hardcoded Crossfit Ruller
    "&filter[locationId]=1981" # Keep these hardcoded Crossfit Ruller Kahler
    f"{filter_between}"
    "&filter[isSession]=0"
    "&perPage=-1"
)
headers = {
    "Accept": "application/json, text/plain, */*",
    "Authorization": f"Bearer {secret}",
    "Sec-Fetch-Site": "same-site",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Sec-Fetch-Mode": "cors",
    "Origin": "https://app.octivfitness.com",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.3 Safari/605.1.15",
    "Referer": "https://app.octivfitness.com/",
    "Sec-Fetch-Dest": "empty",
    "bypass-tunnel-reminder": "*",
    "Priority": "u=3, i",
    "X-CamelCase": "true"
}

response = requests.get(url, headers=headers)

# Print the JSON response, pretty-printed
# try:
#     print(str(response.json()))
# except Exception:
#     print(response.text)


# Assume 'data' is your JSON response (already loaded as a Python dict)
# If you have it as a string, use: data = json.loads(json_string)

def extract_class_id(data):
    class_dates = data.get('data', [])
    if not class_dates:
        print("No class dates found.")
        return

    # For demonstration, extract for the first class date
    class_date = class_dates[0]

    print(f"Class: {class_date.get('id'), class_date.get('name')} on {class_date.get('date')}")
    if str(class_date.get('name')).__contains__(class_name): 
        return class_date.get('id')
    else:
        print('Not a 06:30 class! Exiting...')
        exit()


# Example usage:
# import json
data = response.json()
class_id = extract_class_id(data)

payload = {
    "classDateId": class_id,
    "userId": user_id
}
url = "https://api.octivfitness.com/api/class-bookings"
response = requests.post(url, headers=headers, json=payload)

print("Status code:", response.status_code)
try:
    print("Response:", response.json())
except Exception:
    print("Response text:", response.text)