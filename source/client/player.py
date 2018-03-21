from miner import find_bitcoin
import requests
import sys
import re
import copy

# the url on which we will play!
dom = sys.argv[1]

def err(msg="Error"):
    print(msg)
    sys.exit(1)

def isright(response_body):
    # return '<p class="right">' in response_body
    return (re.findall(r'(?<=<p class="right">).*?(?=</p>)',response_body)[0])

def get_magic(response_body):
    return (re.findall(r'(?<=<span class="question">).*?(?=</span>)',response_body)[0]).split(" ")[-1]

def is_finished(response_body):
    return 'value="Play again!"' in response_body

req = ""
try:
    req = requests.get(dom)
except:
    err("Could not reach server")

if req.status_code != 200:
    err()

finished = False
cookies = copy.deepcopy(req.cookies)
roundd=1
while not finished:
    magic = get_magic(req.text)
    answer,value = find_bitcoin(magic)
    print("Round {}, magic code: {}\n{} {}.{}".format(roundd,magic,answer,value // 100,value % 100))
    headers = {"Content-Type":"application/x-www-form-urlencoded"}
    # cookies = copy.deepcopy(req.cookies)
    # print(cookies)
    req = requests.post(url=dom,data={"answer":answer,"submit":"Submit!"},cookies=cookies,headers=headers)
    # req = requests.post(url=dom,json="answer={}&submit=Submit!".format(answer),cookies=cookies,headers=headers)
    try:
        resp = isright(req.text)
    except:
        err("Wrong Answer")
    print(resp)
    # cookies = req.cookies
    finished = is_finished(req.text)
    if not finished:
        req = requests.post(url=dom,data={"again":"Continue!","continue":"continue"},cookies=cookies,headers=headers)
    # cookies = req.cookies
    # print(cookies)
    
    roundd+=1
    # print(req.text)
    # x =input("")


# print(req.text)


# print(first.text)

# print(find_bitcoin("1111"))