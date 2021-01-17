# myBot
import requests, json # Gemini API
import smtplib # sms
import time # scheduler

# Gemini/Crypto -------------------------------------------
base_url = "https://api.gemini.com/v1"

# SMS -----------------------------------------------------

botProperties = open("bot.properties", "r+")

botProperties.seek(0)
first_char = botProperties.read(1)

botProperties.seek(0)
email = botProperties.readline().split('=')[1].strip()
password = botProperties.readline().split('=')[1].strip()
sms_gateway = botProperties.readline().split('=')[1].strip()
smtp = botProperties.readline().split('=')[1].strip()
port = botProperties.readline().split('=')[1].strip()

server = smtplib.SMTP(smtp, port)
server.starttls()
server.login(email, password)

# APP --------------------------------------------------
print("Hello! This is your crypto notifier.")

symbol = input("Enter crypto symbol: ").upper()

print("Notify me when...")

low_price = float(input("Price is lower than:  "))
high_price = float(input("Price is higher than: "))

def check(symbol, low_price, high_price):
    response = requests.get(f"{base_url}/pubticker/{symbol}usd")
    crypto_data = response.json()
    live_price = float(crypto_data["last"])

    text = "The last price of " + symbol + f" is ${live_price}.\n"

    if live_price < low_price:
        text += "ALERT! LOW PRICE"
    elif live_price > high_price:
        text += "ALERT! HIGH PRICE"
    else:
        text += "Nothing interesting happening now. Relax!"

    server.sendmail(email, sms_gateway, text)
    print(text)
    time.sleep(60)

while True:
    check(symbol, low_price, high_price)
