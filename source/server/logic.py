from question import get_question_html #owned,magic
from answer_wrong import get_answer_wrong_html # owed
from answer_right_finish import get_answer_right_finish_html # owed,worth,seconds
from answer_right_no_finish import get_answer_right_no_finish_html # owed,worth
from threading import Lock
import secrets
import string
import time
import hashlib

sess_dict = {}
sess_locks = {}
sess_full_lock = Lock()
id_len = 10
class player_info:
    def __init__(self):
        self.starting = 200000 #cents
        self.debt = self.starting
        self.start_time = time.time()
        self.magic_num = ""

def to_euros(value):
    return "{0:0{1}}.{2:0{3}}".format(value//100,1,value%100,2)

def random_magic_num():
    return ''.join(secrets.choice(["0","1","2","3","4","5","6","7","8","9","a","b","c","d","e","f"]) for _ in range(4))

def random_id(length):
    return ''.join(secrets.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(length))

def assert_id(old_id):
    
    if old_id is not None:
        with sess_full_lock:
            if old_id in sess_dict:
                return old_id
    
    # sess_id does not exist, we create new
    success = False
    new_id = random_id(id_len)
    while not success:
        with sess_full_lock:
            if new_id not in sess_dict:
                sess_dict[new_id] = player_info()
                sess_dict[new_id].magic_num = random_magic_num()
                sess_locks[new_id] = Lock()
                success = True
            else:
                new_id = random_id(id_len)
    return new_id

def ishex(hexnum):
    try:
        testy = int(hexnum,16)
        return True
    except:
        return False

def check_bitcoin(answer,magic_num):
    if len(answer)!=64 or not ishex(answer):
        return (False,0)
    n = int(answer,16)
    ba = n.to_bytes(32,"big")
    hashed = hashlib.sha256(ba).digest()
    hashed = hashlib.sha256(hashed).hexdigest()
    if hashed[:4] == magic_num:
        value = int(hashed[4:8],16)
        return (True,value)
    else:
        return (False,0)

# returns (body,cookie)
def handle_play(req_type,cookie,form_dict):
    cookie = assert_id(cookie)
    if req_type == "GET":
        with sess_locks[cookie]:
            return (get_question_html(to_euros(sess_dict[cookie].debt),sess_dict[cookie].magic_num),cookie)
    elif req_type == "POST":
        if "answer" in form_dict:
            valid,value = check_bitcoin(form_dict["answer"],sess_dict[cookie].magic_num)
            with sess_locks[cookie]:
                sess_dict[cookie].magic_num = random_magic_num()
            if valid:
                with sess_locks[cookie]:
                    olddebt = sess_dict[cookie].debt
                    sess_dict[cookie].debt -=value
                    if sess_dict[cookie].debt <= 0:
                        return (get_answer_right_finish_html(to_euros(olddebt),to_euros(value),time.time()-sess_dict[cookie].start_time),cookie)
                    else:
                        return (get_answer_right_no_finish_html(to_euros(olddebt),to_euros(value)),cookie)
            else:
                with sess_locks[cookie]:
                    return (get_answer_wrong_html(to_euros(sess_dict[cookie].debt)),cookie)
        elif "continue" in form_dict:
            with sess_locks[cookie]:
                return (get_question_html(to_euros(sess_dict[cookie].debt),sess_dict[cookie].magic_num),cookie)
        elif "again" or "reset" in form_dict:
            with sess_locks[cookie]:
                sess_dict[cookie].debt = sess_dict[cookie].starting
                sess_dict[cookie].start_time = time.time()
                sess_dict[cookie].magic_num = random_magic_num()
                return (get_question_html(to_euros(sess_dict[cookie].debt),sess_dict[cookie].magic_num),cookie)