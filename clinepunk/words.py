import bisect
import json
import logging
import pathlib
import pprint
import random
import sys
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

import requests

cache_path = pathlib.Path("/tmp/clinepunk.json")

def refresh_cache():
    r = requests.get(url)

    if r.status_code == 200:
        dct = r.json()
        js = json.dumps(dct, indent=2).encode("utf-8")
        return js
    return ""


def find_filter(words, min_length=3, max_length=7):
    return filter(lambda s: s.length > min_length and s.length <= max_length, words)


@dataclass(order=True)
class Word:
    word: str = field(compare=False)
    length: int


url = "https://raw.githubusercontent.com/first20hours/google-10000-english/master/google-10000-english-no-swears.txt"
if not cache_path.exists():
    response = requests.get(url)
    logging.debug(f"{response.url=}")
    if response.status_code != 200:
        logging.warning(f"couldn't fetch {url}")

    text = response.text

    words = []
    for word in text.splitlines():
        bisect.insort(words, Word(length=len(word), word=word))

    js = json.dumps(words, indent=2, default=str)
    cache_path.write_text(js)

words = json.loads(cache_path.read_text())
print(words)
sys.exit(-1)
subset = list(find_filter(words, min_length=3, max_length=7))

count = 2
sample = random.sample(words, count)
print(f"{sample[0].word}{sample[1].word}")


def main():
    logging.basicConfig(
        level=logging.DEBUG,
        format="{%(filename)s:%(lineno)d} %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(f"{pathlib.Path(__file__).stem}.log"),
            logging.StreamHandler(sys.stdout),
        ],
    )


if __name__ == "__main__":
    main()
