import requests
import re
import threading

# 全局请求头，可根据实际情况调整
headers = {

}


# 获取章节的HTML内容并提取文本，写入文件
def get_html(url, a, i):
    headers1 = {

    }
    html = requests.get(url, headers=headers1).text
    pattern = '<article id="article" class="content"><p>(.*?)</article>'
    data = re.findall(pattern, html)
    if data:
        text = data[0].replace('</p><p>', '\n')
        text = text.replace('<p>', '')
        text = text.replace('</p>', '')
        write(text, a, i)
    else:
        print(f"第{a + 1}章第{i}页 未获取到有效内容")

# 将提取的文本写入文件
def write(fond, a, i):
    file_path = "test.txt"
    with open(file_path, 'a', encoding='utf-8') as file:
        file.write(f"第{a + 1}章第{i}页" + '\n')
        file.write(fond + '\n')
    print(f"第{a + 1}章第{i}页完成")

# 获取单章的多页内容
def get_main(url, a):
    threads = []
    for i in range(1, 6):
        if i == 1:
            url_i = url
        else:
            url_i = url[:-1] + "_" + str(i) + url[-1:]
        t = threading.Thread(target=get_html, args=(url_i, a, i))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
if __name__ == "__main__":
    url = "https://www.ixiaoshu.com/b/4569/"
    response = requests.get(url, headers=headers).content.decode()
    pattern = r'<a href="(.*?)" title="大奉打更人 大奉打更人.*?">大奉打更人.*?</a>'
    url_html = re.findall(pattern, response, re.DOTALL)
    del url_html[0:12]
    a = 0
    threads_main = []
    for i in url_html:
        url_full = "https://www.ixiaoshu.com" + i
        t_main = threading.Thread(target=get_main, args=(url_full, a))
        threads_main.append(t_main)
        t_main.start()
        a = a + 1
    for t in threads_main:
        t.join()
    print("所有章节爬取完成")