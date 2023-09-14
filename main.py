import os
import requests
import bs4
import markdown
import requests
import json
import re
import urllib.parse
import jsonpath
import socket
import time
import random
import gzip
from bs4 import BeautifulSoup

savePath1 = "problems"
savePath2 = "solutions"

Cookie = {
    '__client_id' : '27cedeb169fd8383e4e189a6f8a79f566ec95977',
    'login_referer' : 'https%3A%2F%2Fwww.luogu.com.cn%2F',
    '_uid' : '15886',
    'C3VK':'e17ff1'
}

headers = {
    "authority": "www.luogu.com.cn",
    "method": "GET",
    "path": "/problem/list?difficulty=2&page=1&_contentOnly=1",
    "scheme": "https",
    "accept": "application/json, text/plain, */*",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
    "cookie": "__client_id=27cedeb169fd8383e4e189a6f8a79f566ec95977; _uid=15886; C3VK=31ec12",
    "referer": "https://www.luogu.com.cn/problem/list",
    "sec-ch-ua": "\"Chromium\";v=\"116\", \"Not)A;Brand\";v=\"24\", \"Google Chrome\";v=\"116\"",
    "sec-ch-ua-mobile": "?1",
    "sec-ch-ua-platform": "\"Android\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36",
    "x-csrf-token": "1694742469:1p4SNM9FURZNEOEG5fRLhgEP0/LEaUQ3OeXJvVp+r6k=",
    "x-requested-with": "XMLHttpRequest"
}

# 定义要爬取的难度和关键词
default_difficulties = ["暂无评定","入门", "普及-", "普及/提高−", "普及+/提高", "提高+/省选−", "省选/NOI−", "NOI/NOI+/CTSC"]
default_keywords = ["算法", "来源", "标题", "题目编号"]

# 获取题目难度和关键词的映射
difficulty_mapping = {
    "1": "暂无评定",
    "2": "入门",
    "3": "普及−",
    "4": "普及/提高−",
    "5": "普及+/提高",
    "6": "提高+/省选−",
    "7": "省选/NOI−",
    "8": "NOI/NOI+/CTSC",
}

# 洛谷题目的URL
base_url = "https://www.luogu.org/problemnew/show/"

# 定义函数来创建目录
def create_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)

# 定义函数来保存Markdown文件
def save_markdown_file(filename, content):
    with open(filename, "w", encoding="utf-8") as file:
        file.write(content)

# 定义函数来获取标签数据，添加异常处理
def get_tags():
    try:
        tag_url = 'https://www.luogu.com.cn/_lfe/tags'
        tag_data = requests.get(url=tag_url, headers=headers).json()
        tags_dicts = []
        for tag in jsonpath.jsonpath(tag_data, '$.tags')[0]:
            tag_type = jsonpath.jsonpath(tag, '$.type')[0]
            tags_dicts.append({'id': jsonpath.jsonpath(tag, '$.id')[0], 'name': jsonpath.jsonpath(tag, '$.name')[0]})
        return tags_dicts
    except Exception as e:
        print(f"获取标签数据时发生错误: {str(e)}")
        return []

# 定义函数来获取题目数据，添加异常处理
def get_problems(anum, bnum, tags_dicts, INdifficulty, INkeywords):
    ts = []
    try:
        a = (anum - 1000) // 50 + 1
        b = (bnum - 1000) // 50 + 1

        for page in range(a, b + 1):
            url = f'https://www.luogu.com.cn/problem/list?page={page}'
            html = requests.get(url=url, headers=headers).text
            urlParse = re.findall('decodeURIComponent\((.*?)\)\)', html)[0]
            htmlParse = json.loads(urllib.parse.unquote(urlParse)[1:-1])
            result = list(jsonpath.jsonpath(htmlParse, '$.currentData.problems.result')[0])

            for res in result:
                pid = jsonpath.jsonpath(res, '$.pid')[0]
                ppid = int(pid[1:])
                if ppid < anum:
                    continue
                if ppid > bnum:
                    break
                title = jsonpath.jsonpath(res, '$.title')[0]
                difficulty = difficulty_mapping.get(str(jsonpath.jsonpath(res, '$.difficulty')[0]), "未知")
                tags_s = list(jsonpath.jsonpath(res, '$.tags')[0])
                tags = []
                for ta in tags_s:
                    for tags_dict in tags_dicts:
                        if tags_dict.get('id') == ta:
                            tags.append(tags_dict.get('name'))
                
                # 添加条件检查
                if INdifficulty!='' and INkeywords!='':
                    if difficulty == INdifficulty and any(keyword in tags for keyword in INkeywords):
                        wen = {
                            "题号": pid,
                            "题目": title,
                            "标签": tags,
                            "难度": difficulty,
                        }
                        ts.append(wen)
                        getPage(pid,title)
                        get_solutions(pid,title)
                        continue
                if INdifficulty!='' and INkeywords == ['']:
                    if difficulty == INdifficulty:
                        wen = {
                            "题号": pid,
                            "题目": title,
                            "标签": tags,
                            "难度": difficulty,
                        }
                        ts.append(wen)
                        getPage(pid,title)
                        get_solutions(pid,title)
                        continue
                if INkeywords!=''  and INdifficulty == ['']:
                    if any(keyword in tags for keyword in INkeywords):
                        wen = {
                            "题号": pid,
                            "题目": title,
                            "标签": tags,
                            "难度": difficulty,
                        }
                        ts.append(wen)
                        getPage(pid,title)
                        get_solutions(pid,title)
                        continue
                wen = {
                    "题号": pid,
                    "题目": title,
                    "标签": tags,
                    "难度": difficulty,
                }
                ts.append(wen)
                getPage(pid,title)
                get_solutions(pid,title)

            print(f'第{page}页已经保存\n已将页面中符合查询条件的题目保存为md，请打开文件夹查看')
    except Exception as e:
        print(f"获取题目数据时发生错误: {str(e)}")
    return ts

def web():

    # 创建服务器套接字
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 绑定服务器地址和端口
    server_address = ('localhost', 12345)  # 使用localhost和端口12345
    server_socket.bind(server_address)

    # 启动服务器监听
    server_socket.listen(1)
    print("等待客户端连接...")

    # 接受客户端连接
    client_socket, client_address = server_socket.accept()
    print(f"连接来自 {client_address}")

    # 接收来自客户端的数据
    data = client_socket.recv(1024)  # 接收最多1024字节的数据
    received_data = data.decode('utf-8')
    print(f"接收到的数据: {received_data}")

    # 从接收的数据中提取难度和关键词
    received_data_dict = eval(received_data)  # 将接收的字符串转换为字典
    difficulty = received_data_dict.get("难度", "")
    keywords = received_data_dict.get("关键词", "")
    anum = received_data_dict.get("起始题号", "")
    bnum = received_data_dict.get("结束题号", "")
    anum = int(anum)
    bnum = int(bnum)
    if bnum-anum>100:
        bnum=anum+100
    
    keywords = [kw.strip() for kw in keywords.split(',')]

    try:
        # 获取标签数据
        tags_dicts = get_tags()

        # 获取题目数据
        problems_data = get_problems(anum, bnum, tags_dicts, difficulty, keywords)

        # 将数据写入JSON文件
        with open('info.json', 'w', encoding='utf-8') as f:
            json.dump(problems_data, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"发生未处理的异常: {str(e)}")

    # 关闭套接字
    client_socket.close()
    server_socket.close()

def getMD(html):
    bs = bs4.BeautifulSoup(html, "html.parser")
    core = bs.select("article")[0]
    md = str(core)
    md = re.sub("<h1>", "# ", md)
    md = re.sub("<h2>", "## ", md)
    md = re.sub("<h3>", "#### ", md)
    md = re.sub("</?[a-zA-Z]+[^<>]*>", "", md)
    return md

workPath = os.getcwd()
def saveData(data, save, filename):
    if not os.path.exists(save):
        os.makedirs(save)
    cfilename = os.path.join(workPath, save, filename)
    if os.path.exists(cfilename):
        print(f"'{cfilename}'已存在，不再重复存储.")
        return
    file = open(cfilename, "w", encoding="utf-8")
    for d in data:
        file.writelines(d)
    file.close()

def getHTML(url):
    Pageheaders = {
        "user-agent": "Mozilla / 5.0(Windows NT 10.0;Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 85.0.4183.121 Safari / 537.36"
    }
    request = urllib.request.Request(url = url,headers = Pageheaders)
    response = urllib.request.urlopen(request)
    html = response.read().decode('utf-8')
    if str(html).find("Exception") == -1:        #洛谷中没找到该题目或无权查看的提示网页中会有该字样
        return html
    else:
        return "error"

def getPage(pid,title):
    baseUrl = "https://www.luogu.com.cn/problem/"
    print("正在爬取{}...".format(pid),end="\n")
    html = getHTML(baseUrl + str(pid))
    if html == "error":
        print("爬取失败，可能是不存在该题或无权查看")
    else:
        problemMD = getMD(html)
        print("爬取成功！正在保存...\n",end="")
        saveData(problemMD,savePath1,str(pid)+"-"+str(title)+".md")
        print("保存成功!")

#获取题解

def Get_TJ_MD(html):
    soup = BeautifulSoup(html, "html.parser")
    encoded_content_element = soup.find('script')
    encoded_content = encoded_content_element.text
    start = encoded_content.find('"')
    end = encoded_content.find('"', start + 1)
    encoded_content = encoded_content[start + 1:end]
    # 对encoded_content进行decodeURIComponent解码为html源码
    decoded_content = urllib.parse.unquote(encoded_content)
    decoded_content = decoded_content.encode('utf-8').decode('unicode_escape')
    start = decoded_content.find('"content":"')
    end = decoded_content.find('","type":"题解"')
    # 截取出题解的内容
    decoded_content = decoded_content[start + 11:end]
    return decoded_content

def get_solutions(pid,title):
    solution_url = "https://www.luogu.com.cn/problem/solution/"+str(pid)
    try:
        # 发送HTTP GET请求获取页面内容
        response = requests.get(url=solution_url, headers=headers, cookies=Cookie)
        html = response.text
        if html == 'error':
            print("题解爬取失败！")
        else:
            print("已获取题解网页源码！")

            # 调用函数，传入html，获取题解MD文件
            solutionMD = Get_TJ_MD(html)
            print("获取题解MD文件成功！")

            # 将题目编号-题目标题-题解作为文件名
            filename = str(pid) + '-' + str(title) + '-题解.md'
            
            saveData(solutionMD, savePath2, filename)

            # 打印提示信息
            print('题解爬取成功！')
    except requests.RequestException as e:
        print(f"请求题解页面时发生错误: {e}")
    except Exception as e:
        print(f"获取题解时发生未知错误: {e}")

if __name__ == '__main__':
    while(1):
        web()