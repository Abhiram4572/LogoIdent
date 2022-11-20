from email import header
from email.quoprimime import header_decode
import json, requests
import shutil
import multiprocessing as mp
from tqdm import tqdm
import sys
import time
from fake_useragent import UserAgent
import os
ua = UserAgent()

def save_img_from_url(line):

    qid, source_url = line.split('\t')
    extension = source_url.split('.')[-1].strip()
    filename = 'logos/' + str(qid) + '.' + extension
    # print(os.path.exists(filename))
    if not os.path.exists(filename):
        
        headers = {'User-Agent': 'Logo_verification (email@domain.com)'}
        res = requests.get(url=source_url.strip(), stream=True, headers=headers)
        print(res.status_code)
        if res.status_code == 200:
            # print(res.raw)
            with open(filename, 'wb') as fp:
                shutil.copyfileobj(res.raw, fp)

        time.sleep(4)
        return res.status_code
    else:
        return 0

path2urlfile = sys.argv[1]
with open(path2urlfile, 'r') as fp:
    data = fp.readlines()

fp.close()

p = mp.Pool(300)

p.map(save_img_from_url, data)