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

def timel(response_body):
    return (re.findall(r'(?<=<p>)It took you .*?(?=</p>)',response_body)[0])

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
took_time = 0
while not finished:
    magic = get_magic(req.text)
    answer,value = find_bitcoin(magic)

    print("Round {}, magic code: {}\n{} {}.{}".format(roundd,magic,answer,value // 100,value % 100))
    
    headers = {"Content-Type":"application/x-www-form-urlencoded"}

    req = requests.post(url=dom,data={"answer":answer,"submit":"Submit!"},cookies=cookies,headers=headers)

    try:
        resp = isright(req.text)
    except:
        err("Wrong Answer")

    print(resp)

    finished = is_finished(req.text)
    if not finished:
        req = requests.post(url=dom,data={"again":"Continue!","continue":"continue"},cookies=cookies,headers=headers)
    else:
        try:
            took_time = timel(req.text)
            print(took_time)
        except:
            pass
    
    roundd+=1