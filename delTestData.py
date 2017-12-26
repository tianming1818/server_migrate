#coding:utf-8
import requests,json,os
import datetime,sys,time
from config import *


url = sys.argv[1]
org = sys.argv[2]
app = sys.argv[3]
username = sys.argv[4]
password = sys.argv[5]
clientname = sys.argv[6]



def deleteUser(user):
    # delete a user
    try:
        r = requests.delete("%s/%s/%s/users/%s" % (url, org, app, user), headers=headers)
        if r.status_code == 200:
            data1 = r.json()
            get = requests.get("%s/%s/%s/users/%s" % (url, org, app, user), headers=headers)
            data2 = get.json()
            if get.status_code == 404:
                print "delete user %s success" % user
                #print json.dumps(data1, sort_keys=True, indent=2)
                return True
            else:
                print "delete user %s failed, get deleted user detail status code is not 404, is %s " % (user, get.status_code)
                print "delete user,get user detail: "
                print json.dumps(data2, sort_keys=True, indent=2)
                #exit(9)
        else:
            print "status code is %s, del user request error" % r.status_code
            print json.dumps(r.json(), sort_keys=True, indent=2)
            #exit(9)
    except requests.exceptions.ConnectionError, e:
        print "Your url is error: %s" % e
        #exit(9)


for user in userlist:
    deleteUser(user)

os.system("rm -f %s.txt" % clientname)


