import argparse
import datetime
import re
import requests
import time


parser = argparse.ArgumentParser()
parser.add_argument('--store_url', type=str, help='The Apple website page url of the primary store to watch. The 11 nearest stores to the primary store will also be watched.')
parser.add_argument('--models', type=str, help="A comma separated list of the models to watch. Valid values are space_gray, silver, green, sky_blue, pink.")
parser.add_argument('--sleep_time', type=float, default=300, help='The number of seconds to wait in between each check. Default: 5 minutes.')

args = parser.parse_args()

if args.store_url is None or args.models is None:
    exit('--store_url and --models are required')

model_name_to_id = {
    'space_gray': 'MGYH3AM/A',
    'silver': 'MGYJ3AM/A',
    'green': 'MGYN3AM/A',
    'sky_blue': 'MGYL3AM/A',
    'pink': 'MGYM3AM/A',
}

model_id_to_name = {v: k for k, v in model_name_to_id.items()}

r = requests.get(args.store_url)
if r.status_code != 200:
    exit('Got an unexpected response from the store page. Did you specify the correct URL?')
_, store_to_watch = re.search('<meta property=\"analytics-track\" content=\"Retail Store - (.+?):(.+?)\" \/>', r.text).groups()
models_to_watch = [model_name_to_id[model_id] for model_id in args.models.split(',')]
sleep_time = args.sleep_time

def log(msg):
    print(f'[{datetime.datetime.now()}] {msg}')

def check_store(store, product):
    return store['partsAvailability'][product]['pickupDisplay'] != 'unavailable'

def webhookRequest(store_name, model):
    url = "" # Put your Discord webhook url here

    data = {
        "content" : "", # Put your Discord id in the format of <@[discord ID]> to get mentioned when there's stock
        "username" : "AirPods Max Stock" # Put your Discord webhook name here
    }

    data["embeds"] = [
        {
            "description" : "AirPods Max are in stock for the " + model + " model!",
            "title" : "Stock Available at " + store_name
        }
    ]

    result = requests.post(url, json = data)

def check_model_near(model, store_id):
    try:
        r = requests.get(
            f'https://www.apple.com/shop/retail/pickup-message?pl=true&searchNearby=true&store={store_id}&parts.0={model}')
        if r.status_code == 200:
            resp = r.json()
            found = False
            for store in resp['body']['stores']:
                store_name = store['storeName']
                if check_store(store, model):
                    log(f'Found {model_id_to_name[model]} availability at {store_name}!')
                    webhookRequest(store_name, model_id_to_name[model])
                    found = True
            if not found:
                log(f'No availability found for {model_id_to_name[model]}.')
        else:
            log(f"Received unexpected status code ${r.status_code}")
    except:
        log(f"Error requesting store availability.")

while True:
    for model in models_to_watch:
        check_model_near(model, store_to_watch)

    time.sleep(sleep_time)
