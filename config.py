#coding:utf-8
import requests,json
import sys,time

url = sys.argv[1]
org = sys.argv[2]
app = sys.argv[3]
username = sys.argv[4]
password = sys.argv[5]




user1 = "test001"
user2 = "test002"
user3 = "test003"
user4 = "test004"
user5 = "test005"
user6 = "test006"
user7 = "test007"
user8 = "test008"
user9 = "test009"


userlist = [user1,user2,user3,user4,user5,user6,user7,user8,user9]


## get Admin token
def acquire_token(url,username,password):
    tokenbody = {
        "grant_type":"password",
        "username":username,
        "password":password }
    try:
        req = requests.post("%s/management/token/superToken" %(url),data=json.dumps(tokenbody),headers={'Accept':'application/json','Content-Type': 'application/json'})
    except requests.exceptions.ConnectionError,e:
        return "Your url is error :", e.message
    try:
        if req.status_code == 200:
            contents = json.loads(req.content)
            tokens = contents["access_token"]
            expires_in = contents["expires_in"]
            return tokens,expires_in
        else:
            print "get token failed, status code: %s" % req.status_code
            print json.dumps(req.json(), sort_keys=True, indent=2)
            exit()
    except (ValueError,UnboundLocalError),e:
        print e

token,expires_in = acquire_token(url,username,password)

if token:
    print "token is: ", token
    print "expires_in is: %s" % expires_in
else:
    print "token get failed, exit"
    exit()

'''
#超级token
token = "YWMtmPpRmt5ZEeedV_961BhnFQAAAAAAAAAAAAAAAAAAAAFe2JYa1n8R45heowo6U5LUAQMAAAFgRQFecABPGgD7v50BoYYFAfDgr3XCGSgm9zdQGNyIseJjXBswqJQYSQ"

#灰度token
#token = "YWMtlIXhXM4YEeezpfcn9NztsAAAAAAAAAAAAAAAAAAAAAE0jHVaFpQR5oOh13fSZKt6AQMAAAFf2nu5qgBPGgCsETm-lBkrSIqrlQmESeEMS-WarDIpqx0VrTTSG6x9RQ"

'''

headers = {'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': "Bearer %s" % token}