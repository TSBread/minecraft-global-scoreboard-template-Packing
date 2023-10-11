import os
import json
import base64
import warnings
from urllib.request import urlopen
from urllib.request import Request

import requests

headers = {'User-Agent': 'Mozilla/5.0',
           'Authorization': 'token ' + os.environ.get('TOKEN'),
           'Accept': 'application/vnd.github.v3+json'}


def delete_commit_value(repo_owner, repo_name):
    url = 'https://api.github.com/repos/' + repo_owner + '/' + repo_name + '/contents'
    result = json.loads(urlopen(Request(url, headers=headers)).read().decode())
    for i in result:
        if i["name"] == "value":
            data = {"message": "合并成功", "sha": i['sha']}
            warnings.filterwarnings('ignore')
            requests.delete(url + '/value', data=json.dumps(data), headers=headers, verify=False)
            c_url = 'https://api.github.com/repos/' + repo_owner + '/' + repo_name + '/git/blobs/' + i['sha']
            content = json.loads(urlopen(Request(c_url, headers=headers)).read().decode())
            return bytes.decode(base64.b64decode(content['content']))


if __name__ == '__main__':
    owner = 'TSBread'
    name = 'minecraft-global-scoreboard-template-Packing'
    delete_commit_value(owner, name)
