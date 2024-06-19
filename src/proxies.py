import random

proxies = []

def add_proxy(ip, port, proxy_type='HTTP'):
    proxies.append(f"{ip}:{port}:{proxy_type}")

def remove_proxy(proxy):
    if proxy in proxies:
        proxies.remove(proxy)

def list_proxies():
    return proxies

def get_random_proxy():
    return random.choice(proxies)
