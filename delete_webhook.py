import requests

TOKEN = "8051188469:AAGDVGdYbpt3A3nIn38gu052ykv5TUKvtMI"
url = f"https://api.telegram.org/bot{TOKEN}/deleteWebhook"

response = requests.get(url)
print(response.text)
