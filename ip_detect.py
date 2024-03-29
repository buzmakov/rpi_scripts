# python ip_detect.py > /dev/null 2>&1
'''
Finds your IP address
'''
import requests
import socket
import yaml
from collections import Counter
from plumbum.cmd import git


def get_external_ip():
    ips = {}
    sites = ['http://www.icanhazip.com/', 'http://ipaddr.me',
             'http://curlmyip.com/']
    for s in sites:
        try:
            r = requests.get(s)
            ip = r.text.strip()
            if ip.startswith('<pre>') and ip.endswith('</pre>'):
                ip = ip[5:-6]
            ips[s] = ip
        except:
            pass
    c = Counter([v for k, v in ips.items()])
    return c.most_common(1)[0][0].encode('utf-8')


def get_local_ip(target):
    ipaddr = ''
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((target, 8000))
        ipaddr = s.getsockname()[0]
        s.close()
    except:
        pass
    return ipaddr


def get_ips():
    res = {}
    try:
        res['local'] = get_local_ip('ya.ru')
    except:
        pass
    try:
        res['external'] = get_external_ip()
    except:
        pass
    return res


def save_file(data):
    name = 'rpi_ip.yaml'
    with open(name, 'w') as f:
        f.write(yaml.dump(data, default_flow_style=False))

if __name__ == "__main__":
    try:
        data = get_ips()
        save_file(data)
        git['commit', '-m', '"ip update"', 'rpi_ip.yaml']()
        git['push']()
    except:
        pass
