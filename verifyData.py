#coding:utf-8
import requests,json
import sys,time
from config import *
from CreateData import *


true = True
false = False

url = sys.argv[1]
org = sys.argv[2]
app = sys.argv[3]
username = sys.argv[4]
password = sys.argv[5]
clientname = sys.argv[6]

os.system("python config.py %s %s %s %s %s" %(url,org,app,username,password))

def getUserlist(userlist):
    for myuser in userlist:
        req = requests.get("%s/%s/%s/users/%s" % (url, org, app, myuser),headers=headers)
        if req.status_code == 200:
            print "user %s is exist" % myuser
        elif req.status_code == 404:
            print "verify user %s failed" % myuser
        else:
            print "get user %s detail failed, error status code is: %s" % (myuser,req.status_code)
            print json.dumps(req.json(), sort_keys=True, indent=2)

def getUserFriend(userlist):
    for user in userlist:
        get = requests.get("%s/%s/%s/users/%s/contacts/users" % (url, org, app, user), headers=headers)
        data2 = get.json()
        if get.status_code == 200:
            print "user %s friend list: %s" % (user,data2["data"])
        else:
            print "get user friend failed"
            print json.dumps(data2, sort_keys=True, indent=2)


if __name__ == "__main__":
    getUserlist(userlist)
    getUserFriend(userlist)
    getBlackList(user1)
    getBlackList(user2)
    getBlackList(user3)
    if os.path.exists('%s.txt' % clientname):
        test = open('%s.txt' % clientname, 'r').read()
        if test:
            f = open('%s.txt' % clientname, 'r')
            grouproom = json.load(f)
            for groupid in grouproom["groupid"]:
                getMemberlist(groupid)
            for roomid in grouproom["roomid"]:
                getroomAdminlist(roomid)
    print "offline message number is: "
    for user in userlist:
        getOfflineMess(user)