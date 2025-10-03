#!/usr/bin/env python3

import os
from pathlib import Path

import requests
from bs4 import BeautifulSoup

def main():
    base_url = 'https://pld.ttu.ee/~maksim/benchmarks/iscas85/bench/'
    target_dir = 'data.nogit'

    r = requests.get(base_url)
    assert r.status_code == 200
    soup = BeautifulSoup(r.text, features="html5lib")

    os.makedirs(target_dir, exist_ok=True)
    for file in [t['href'] for t in soup.find_all('a')]:
        if '.bench' not in file: continue
        print(f'Downloading {file}')
        with open(Path(target_dir, file), 'w') as f:
            rr = requests.get(base_url + file)
            assert rr.status_code == 200
            f.write(rr.text)

if __name__ == '__main__':
    main()