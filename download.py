import random
import requests
import time
import os

base_dir = os.path.dirname(os.path.realpath('__file__'))


def download(start_page=1, end_page=65):
    url_format = "http://www.sidneyluo.net/a/a04/{page}.htm"
    headers = {
        'user-agent': ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) '
                       'AppleWebKit/537.36 (KHTML, like Gecko) '
                       'Chrome/61.0.3163.100 Safari/537.36')
    }

    for _page in range(start_page, end_page + 1):
        page = "{:0>3}".format(_page)
        url = url_format.format(page=page)
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        r.encoding = "utf-8"

        path = os.path.join(base_dir, 'contents/{}.htm'.format(page))
        with open(path, 'w') as f:
            f.write(r.text)

        time.sleep(random.randint(2, 4))


if __name__ == '__main__':
    download()
