import requests, time, re, pickle
session = requests.Session()

response = session.get(f'https://vk.com/')
remixstid, remixlhk = session.cookies.get_dict()['remixstid'], session.cookies.get_dict()['remixlhk'] 

ip_h =  re.findall(r'ip_h=(\S*)&lg', str(response.text))[0]
lg_h =  re.findall(r'lg_h=(\S*)&r', str(response.text))[0]
print(ip_h, lg_h)

login = 'your_login'
password = 'your_password'

response = session.post(f'https://login.vk.com/?act=login', data=f'act=login&role=al_frame&expire=&recaptcha=&captcha_sid=&captcha_key=&_origin=https%3A%2F%2Fvk.com&ip_h={ip_h}&lg_h={lg_h}&ul=&email={login}&pass={password}',
                        cookies={'remixlang': "0",
                        'remixstid': remixstid, 
                        'remixlhk': remixlhk,
                        "remixflash": "0.0.0 ",
                        "remixscreen_depth":"24",
                        "remixscreen_orient":"1",
                        "tmr_lvidTS":str(int(time.time())),
                        "tmr_reqNum":"1",
                        })


for i in session.cookies.get_dict():
    if 'remixq_' in i:
        parametr_q = i
        q_hash = i.split('remixq_')[1]
        break

response = session.get(f'https://vk.com/login.php?act=slogin&to=&s=1&__q_hash={q_hash}')
last_cookies = session.cookies.get_dict()

response = session.get(f'https://vk.com/login?act=authcheck',
                cookies={'remixlang': "0",
                        'remixstid': remixstid, 
                        'remixlhk': remixlhk,
                        "remixflash": "0.0.0 ",
                        "remixscreen_depth":"24",
                        "remixscreen_orient":"1",
                        "tmr_lvidTS":str(int(time.time())),
                        "tmr_reqNum":"1",
                        "remixauthcheck":last_cookies['remixauthcheck'],
                        parametr_q:last_cookies[parametr_q]})

hash_url =  re.findall(r"hash: '(\S*)'},", str(response.text))[0]
print(hash_url)

code = input('Enter verification code:  ')

response = session.post(f'https://vk.com/al_login.php', data=f'act=a_authcheck_code&al=1&code={code}&hash={hash_url}&remember=1',
                        cookies={'remixlang': "0",
                        'remixstid': remixstid, 
                        'remixlhk': remixlhk,
                        "remixflash": "0.0.0 ",
                        "remixscreen_depth":"24",
                        "remixscreen_orient":"1",
                        "tmr_lvidTS":str(int(time.time())),
                        "tmr_reqNum":"1",
                        "remixauthcheck":last_cookies['remixauthcheck'],
                        parametr_q:last_cookies[parametr_q]
                        })
                        
response = session.get(f'https://vk.com/login.php?act=slogin&to=&s=1&__q_hash={q_hash}&fast=1',
                        cookies={'remixlang': "0",
                        'remixstid': remixstid, 
                        'remixlhk': remixlhk,
                        "remixflash": "0.0.0 ",
                        "remixscreen_depth":"24",
                        "remixscreen_orient":"1",
                        "tmr_lvidTS":str(int(time.time())),
                        "tmr_reqNum":"1",
                        "remixauthcheck":last_cookies['remixauthcheck'],
                         parametr_q:last_cookies[parametr_q],
                        'remixttpid': session.cookies.get_dict()['remixttpid']})

cookies_auth = session.cookies.get_dict()
print(response, cookies_auth)
print(cookies_auth['remixusid'], cookies_auth['remixsid'])

response = session.get(f'https://vk.com/feed',
                cookies={'remixlang': "0",
                        'remixstid': remixstid, 
                        'remixlhk': remixlhk,
                        "remixflash": "0.0.0 ",
                        "remixscreen_depth":"24",
                        "remixscreen_orient":"1",
                        "tmr_lvidTS":str(int(time.time())),
                        "tmr_reqNum":"1",
                        'remixttpid': cookies_auth['remixttpid'],
                        'remixusid': cookies_auth['remixusid'],
                        'remixsid': cookies_auth['remixsid']})

cookies_final = {'remixlang': "0",
                        'remixstid': remixstid, 
                        'remixlhk': remixlhk,
                        "remixflash": "0.0.0 ",
                        "remixscreen_depth":"24",
                        "remixscreen_orient":"1",
                        "tmr_lvidTS":str(int(time.time())),
                        "tmr_reqNum":"1",
                        'remixttpid': cookies_auth['remixttpid'],
                        'remixusid': cookies_auth['remixusid'],
                        'remixsid': cookies_auth['remixsid']}

with open('cookies_vk_auth.pickle', 'wb') as handle:
    pickle.dump(cookies_final, handle, protocol=pickle.HIGHEST_PROTOCOL)
