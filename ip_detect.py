'''
Finds your external IP address
'''
import requests
import socket
import yaml
from collections import Counter


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
    res['local'] = get_local_ip('ya.ru')
    res['external'] = get_external_ip()
    return res


def save_file(data):
    name = 'rpi_ip.yaml'
    with open(name, 'w') as f:
        f.write(yaml.dump(data, default_flow_style=False))

if __name__ == "__main__":
    data = get_ips()
    save_file(data)
