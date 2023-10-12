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
print("template by TSBread")


def merge_file_data(repo_owner, repo_name, data):
    path = '/modify.mcfunction'
    url = 'https://api.github.com/repos/' + repo_owner + '/' + repo_name + '/contents/saves?ref=main'
    for i in json.loads(urlopen(Request(url, headers=headers)).read().decode()):
        if i['name'] == path:
            url = 'https://api.github.com/repos/' + repo_owner + '/' + repo_name + '/git/blobs/' + i['sha']
            content = json.loads(urlopen(Request(url, headers=headers)).read().decode())
            get_data = list(bytes.decode(base64.b64decode(content['content'])))
            if get_data[-2] == "[":
                get_data.insert(-1, data)
            else:
                get_data.insert(-1, "," + data)
            data = "".join(get_data)
            data = {"message": "上传玩家提交数据", "sha": i['sha'],
                    "content": bytes.decode(base64.b64encode(data.encode('utf-8')))}
            url = 'https://api.github.com/repos/' + repo_owner + '/' + repo_name + '/contents/saves'
            warnings.filterwarnings('ignore')
            requests.put(url + path, data=json.dumps(data), headers=headers, verify=False)


def get_repo_content(repo_owner, repo_name):
    url = 'https://api.github.com/repos/' + repo_owner + '/' + repo_name + '/contents'
    return json.loads(urlopen(Request(url, headers=headers)).read().decode())


def get_player_update_info(repo_owner, repo_name, repo):
    for i in repo:
        if i["name"] == "value.mgst":
            url = 'https://api.github.com/repos/' + repo_owner + '/' + repo_name + '/git/blobs/' + i['sha']
            content = json.loads(urlopen(Request(url, headers=headers)).read().decode())
            return bytes.decode(base64.b64decode(content['content']))


def delete_player_update_info(repo_owner, repo_name, repo):
    url = 'https://api.github.com/repos/' + repo_owner + '/' + repo_name + '/contents'
    for i in repo:
        warnings.filterwarnings('ignore')
        data = {"message": "合并成功", "sha": i['sha']}
        requests.delete(url + '/value.mgst', data=json.dumps(data), headers=headers, verify=False)


def check_mgst(repo):
    for i in repo:
        if i["name"] == "value.mgst":
            return 1


if __name__ == '__main__':
    owner = 'TSBread'
    name = 'minecraft-global-scoreboard-template-Packing'
    repo_content = get_repo_content(owner, name)
    if check_mgst(repo_content):
        data = get_player_update_info(owner, name, repo_content)
        merge_file_data(owner, name, data)
        delete_player_update_info(owner, name, repo_content)
