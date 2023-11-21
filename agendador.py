import schedule
import time
import requests

def agendador():
    requests.get("http://127.0.0.1:5000/get_aniversarios/")

schedule.every().day.at("17:40").do(agendador)

while True:
    schedule.run_pending()
    time.sleep(30)