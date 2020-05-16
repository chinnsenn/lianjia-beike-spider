from lxml import etree
import requests
import urllib3

def test_http(ip_host):
    # 测试http代理是否有效
    # 调用ProxyHandler  代理IP的形式是字典
    # px = urllib.request.ProxyHandler({'http':ip_host})
    # 用build_opener()来构建一个opener对象
    # opener = urllib.request.build_opener(px)
    # 然后调用构建好的opener对象里面的open方法来发生请求。
    # 实际上urlopen也是类似这样使用内部定义好的opener.open()，这里就相当于我们自己重写。

    s = requests.session()
    s.verify = False
    s.proxies = {'http':ip_host}
    urllib3.disable_warnings()

    try:
        page = 'https://www.baidu.com'
        response = s.get(page, timeout=10000, verify=False)

        if response:
            print('HTTP @@代理有效(>_<): ', ip_host)
            with open('http.txt', 'w') as f:
                f.write(ip_host + '\n')
    except:
        print('HTTP @@代理无效(X_X!)：',ip_host)

def test_https(ip_host):
    s = requests.session()
    s.verify = False
    s.proxies = {'https':ip_host}
    urllib3.disable_warnings()

    try:
        page = 'https://www.baidu.com'
        response = s.get(page, timeout=10000, verify=False)

        if response:
            print('HTTPS__代理有效(>_<): ', ip_host)
            with open('https.txt', 'w') as f:
                f.write(ip_host + '\n')
    except:
        print('HTTPS__代理无效(X_X!)：', ip_host)

def get_ip(num):
    print('正在搜寻第 %s 的内容',num)
    url = 'http://www.xicidaili.com/nn/' + str(num)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
    }
    res = urllib.request.Request(url,headers=headers)
    response = urllib.request.urlopen(res)
    response = response.read()

    # s = requests.session()
    # s.verify = False
    # urllib3.disable_warnings()
    # response = s.get(url, timeout=10000, verify=False)

    html = etree.HTML(response)  # 转化这个位置 不用解码
    ip_lists = html.xpath('//div//tr')  # 节点
    proxies = list()
    for tem in ip_lists:
        ip = tem.xpath('./td[2]/text()')
        if not ip:                  # 如果列表是空的跳过本次循环 这个主要是针对最上面的标签问题
            continue
        ip = ip[0]  # xpath 提取数据以后返回的是列表
        host = tem.xpath('./td[3]/text()')[0]
        tcp_type = tem.xpath('./td[6]/text()')[0]  # 获得协议类型

        if tcp_type == 'HTTP':
            # 判断是否是http协议
            ip_host = ip + ':' + host   # 拼接将要使用的地址和端口
            test_http(ip_host)  # 测试代理的有效性
            proxy = {'http':ip_host}
            proxies.append(proxy)

        elif tcp_type == 'HTTPS':
            ip_host = ip + ':' + host   # 拼接将要使用的地址和端口
            test_https(ip_host)  # 测试代理的有效性
            proxy = {'https':ip_host}
            proxies.append(proxy)

        else:
            # 可能还会有其他类型的协议
            pass
    print(proxies)
if __name__ == '__main__':
    page = int(input('输入要爬取的页数:'))
    for num in range(1,page+1):
        get_ip(num)