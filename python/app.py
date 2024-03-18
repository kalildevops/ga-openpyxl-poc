import requests
import json
import os
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import pandas as pd
import openpyxl
import datetime

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

today = datetime.datetime.now()
data_time = today.strftime("%d%m%Y_%H-%M-%S")

rows = []

#From GA workflow
environment = os.environ.get("ENV_CHOICE")
download_choice = os.environ.get("DOWNLOAD_CHOICE")
token = os.environ.get("API_TOKEN")

def open_file(file):
  with open("api_list/" + file, "r") as file:
    api_endpoints = [line.strip() for line in file]
  return api_endpoints

if environment == "Dev":
  api_endpoints = open_file("dev.txt")
elif environment == "Stage":
  api_endpoints = open_file("stage.txt")
elif environment == "Prod":
  api_endpoints = open_file("prod.txt")

n = 0
for endpoint in api_endpoints:
  n += 1
  print(f"{n} - {endpoint}")
  if environment == "Dev":
    base_url = "https://dev.com"
    xls_file = "results-dev-" + str(data_time) + ".xlsx"
  elif environment == "Stage":
    base_url = "https://stage.com"
    xls_file = "results-stage-" + str(data_time) + ".xlsx"
  elif environment == "Prod":
    base_url = "https://prod.com"
    xls_file = "results-prod-" + str(data_time) + ".xlsx"
  
  full_url = f"{base_url}/{endpoint}/heath_check"

  try:
    response = requests.head(
      full_url,
      headers={'Authorization': f'Basic {token}'},
      verify=False # Disable SSL verification
    )
    http_status = response.status_code
    openapi_data = requests.get(
      full_url,
      headers={'Authorization': f'Basic {token}'},
      verify=False # Disable SSL verification
    )
  
    openapi_json = openapi_data.json()
    version = openapi_json.get('info', {}).get('version')
    print(f"HTTP Status: {http_status} - Version {version}")
    print("")

    if download_choice == "Yes":
      rows.append([
        n,
        endpoint,
        http_status,
        version,
        full_url,
        data_time
      ])
      df1 = pd.DataFrame(rows,
      columns=[
        "#",
        "API",
        "HTTP Status",
        "Version",
        "URL",
        "Date"
      ])
      df1.to_excel(xls_file, sheet_name='Sheet1', index=False)
  except requests.exceptions.RequestException as e:
    print(e)
  



