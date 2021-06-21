from datetime import datetime

from apscheduler.schedulers.blocking import BlockingScheduler
from crypto_emailer import messagemaker, select, start

import requests

url = 'https://api.chat-api.com/instance291064/message?token=token'

data = {
  "phone": "15555555555",
  "body": messagemaker(select(start))
}

def job_function():
	res = requests.post(url, json=data)
	print(res.text)

# Schedule job_function to be called every two hours
scheduler = BlockingScheduler()
scheduler.add_job(job_function, 'interval', hours=4)
scheduler.start()
