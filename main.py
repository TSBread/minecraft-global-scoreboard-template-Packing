import os
import json
import base64
import warnings
import zipfile
import io
from urllib.request import urlopen
from urllib.request import Request

import requests

headers = {'User-Agent': 'Mozilla/5.0',
           'Authorization': 'token ' + os.environ.get('TOKEN'),
           'Accept': 'application/vnd.github.v3+json'}
print("template by TSBread")


def merge_file_data(repo_owner, repo_name, data):
    path = 'modify.mcfunction'
    url = 'https://api.github.com/repos/' + repo_owner + '/' + repo_name + '/contents/saves?ref=main'
    for i in json.loads(urlopen(Request(url, headers=headers)).read().decode()):
        print(i['name'])
        if i['name'] == path:
            url = 'https://api.github.com/repos/' + repo_owner + '/' + repo_name + '/git/blobs/' + i['sha']
            content = json.loads(urlopen(Request(url, headers=headers)).read().decode())
            get_data = list(bytes.decode(base64.b64decode(content['content'])))
            if get_data[-2] == "[":
                get_data.insert(-1, data)
            else:
                get_data.insert(-1, "," + data)
            data = "".join(get_data)
            mydata = {"message": "上传玩家提交数据", "sha": i['sha'],
                      "content": bytes.decode(base64.b64encode(data.encode('utf-8')))}
            url = 'https://api.github.com/repos/' + repo_owner + '/' + repo_name + '/contents/saves'
            warnings.filterwarnings('ignore')
            requests.put(url + "/"+path, data=json.dumps(mydata), headers=headers, verify=False)


def open_file(file):
    with open(file, 'rb') as f:
        return f.read()


def update_file_to_repo(repo_owner, repo_name, file):
    url = 'https://api.github.com/repos/' + repo_owner + '/' + repo_name + '/contents/'
    data = {"message": "地图档案打包", "content": base64.b64encode(open_file(file)).decode('utf-8')}
    warnings.filterwarnings('ignore')
    print(data['content'])
    print(url + file)
    test = requests.put(url + file, data=json.dumps(data), headers=headers, verify=False)
    print(test.text)


def get_repo_content(repo_owner, repo_name):
    url = 'https://api.github.com/repos/' + repo_owner + '/' + repo_name + '/contents'
    return json.loads(urlopen(Request(url, headers=headers)).read().decode())


def get_player_update_info(repo_owner, repo_name, repo):
    for i in repo:
        if i["name"] == "value.mgst":
            url = 'https://api.github.com/repos/' + repo_owner + '/' + repo_name + '/git/blobs/' + i['sha']
            content = json.loads(urlopen(Request(url, headers=headers)).read().decode())
            return bytes.decode(base64.b64decode(content['content']))


def delete_file_from_repo(repo_owner, repo_name, repo, file_name):
    url = 'https://api.github.com/repos/' + repo_owner + '/' + repo_name + '/contents/'
    for i in repo:
        if i['name'] == packing_name:
            warnings.filterwarnings('ignore')
            data = {"message": "删除旧版本", "sha": i['sha']}
            requests.delete(url + file_name, data=json.dumps(data), headers=headers, verify=False)


def zip_files_in_buffer(path):
    buffer = io.BytesIO()
    zfile = zipfile.ZipFile(buffer, 'w', zipfile.ZIP_DEFLATED)
    for root, dirs, files in os.walk(path):
        relative_root = '' if root == path else root.replace(path, '') + os.sep
        for filename in files:
            zfile.write(os.path.join(root, filename), relative_root + filename)
    print(zfile.filelist)
    zfile.close()
    buffer.seek(0)
    return buffer


if __name__ == '__main__':
    owner = 'TSBread'
    name = 'minecraft-global-scoreboard-template-Packing'
    packing_name = 'test.zip'
    repo_content = get_repo_content(owner, name)
    data = get_player_update_info(owner, name, repo_content)
    merge_file_data(owner, name, data)
    with open(packing_name, 'wb') as f:
        print(zip_files_in_buffer('saves').getbuffer())
    delete_file_from_repo(owner, name, repo_content, packing_name)
    update_file_to_repo(owner, name, packing_name)

