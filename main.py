import os
import json
import warnings
from urllib.request import urlopen
from urllib.request import Request

import requests


def delete_commit_value():
    repo_owner = 'TSBread'
    repo_name = 'minecraft-global-scoreboard-template-Packing'
    
    url = 'https://api.github.com/repos/' + repo_owner + '/' + repo_name + '/contents'
    headers = {'User-Agent': 'Mozilla/5.0',
               'Authorization': 'token ' + os.environ.get('TOKEN'),
               'Accept': 'application/vnd.github.v3+json'}
    req = Request(url, headers=headers)
    response = urlopen(req).read()
    result = json.loads(response.decode())
    for i in result:
        if i["name"] == "value":
            print(i['sha'])
            data = {"message": "Merge Successful", "sha": i['sha']}
            warnings.filterwarnings('ignore')
            del_rep = requests.delete(url + '/value', data=json.dumps(data), headers=headers, verify=False)
            print(del_rep.text)


if __name__ == '__main__':
    delete_commit_value()
