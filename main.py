import os
import json
import warnings
from urllib.request import urlopen
from urllib.request import Request

import requests


def delete_commit_value():
    url = 'https://api.github.com/repos/TSBread/minecraft-global-scoreboard-template-Packing/contents'
    headers = {'User-Agent': 'Mozilla/5.0',
               'Authorization': 'token ' + os.environ.get('TOKEN'),
               'Accept': 'application/vnd.github.v3+json'}
    req = Request(url, headers=headers)
    response = urlopen(req).read()
    result = json.loads(response.decode())
    # print(result)
    for i in result:
        if i["name"] == "value":
            print(i['sha'])
            data = {"message": "delete a file", "sha": i['sha']}
            warnings.filterwarnings('ignore')
            del_rep = requests.delete(url + '/value', data=json.dumps(data), headers=headers, verify=False)
            print(del_rep.text)


if __name__ == '__main__':
    delete_commit_value()
