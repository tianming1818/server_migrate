#coding:utf-8
import requests,json,os
import datetime,sys,time
from config import *

true = True
false = False

url = sys.argv[1]
org = sys.argv[2]
app = sys.argv[3]
username = sys.argv[4]
password = sys.argv[5]
clientname = sys.argv[6]


os.system("python config.py %s %s %s %s %s" %(url,org,app,username,password))

'''

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

headers = {'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': "Bearer %s" % token}

'''

def greateUser(userlist):
    for myuser in userlist:
        req = requests.get("%s/%s/%s/users/%s" % (url, org, app, myuser),headers=headers)
        if req.status_code == 404:
            CreateUserBody = {"username":myuser,"password":"1"}
            r = requests.post("%s/%s/%s/users" % (url, org, app),
                              data=json.dumps(CreateUserBody),
                              headers=headers)
            if r.status_code ==200:
                print "user %s create success" % myuser
            else:
                print "create user %s failed, status code is: %s" % (myuser,r.status_code)
                print json.dumps(r.json(), sort_keys=True, indent=2)
                exit()
        elif req.status_code == 200:
            print "user %s is exist" % myuser
        else:
            print "get user %s detail failed, status code is: %s" % (myuser,req.status_code)
            print json.dumps(req.json(), sort_keys=True, indent=2)
            exit()

def addFriends(user, friend):
    # add friend for user
    try:
        r = requests.post("%s/%s/%s/users/%s/contacts/users/%s" % (url, org, app, user, friend),headers=headers)
        if r.status_code == 200:
            data1 = r.json()
            get = requests.get("%s/%s/%s/users/%s/contacts/users" % (url, org, app, user), headers=headers)
            if get.status_code == 200:
                data2 = get.json()
                if friend in data2["data"]:
                    #print "user %s additional friend %s success" % (user, friend)
                    return True
                else:
                    print "user %s additional friend %s failed" % (user, friend)
                    print "get user friends list return data: "
                    print json.dumps(data2, sort_keys=True, indent=2)
                    return False
            else:
                print "status code is %s, get user %s friend list request error" % (get.status_code,user)
                print json.dumps(get.json(), sort_keys=True, indent=2)
                return False
        else:
            print "status code is %s, add friend api request error" % r.status_code
            print json.dumps(r.json(), sort_keys=True, indent=2)
            return False
    except requests.exceptions.ConnectionError, e:
        print "Your url is error: %s" % e
        return False

def addFriend(userlist):
    for user in userlist:
        for friend in userlist:
            if user == friend:
                continue
            else:
                result = addFriends(user, friend)
                if result == False:
                    exit()

    for user in userlist:
        get = requests.get("%s/%s/%s/users/%s/contacts/users" % (url, org, app, user), headers=headers)
        data2 = get.json()
        if get.status_code == 200:
            print "user %s friend list: %s" % (user,data2["data"])
        else:
            print "get user friend failed"
            print json.dumps(data2, sort_keys=True, indent=2)
            exit()


def sendMess(userlist,messages):
    sendbody = {"target_type": "users",
                "target": userlist,
                "msg": {
                    "type": "txt",
                    "msg": messages
                },
                "from": "rest"
                }
    r = requests.post("%s/%s/%s/messages" % (url, org, app), data=json.dumps(sendbody), headers=headers)
    if r.status_code == 200:
        print "send message %s success" % messages
    else:
        print "send message %s failed, status code is: %s" % (messages,r.status_code)
        print json.dumps(r.json(), sort_keys=True, indent=2)
        exit()


def uploadImage(imagefile):
    uploadHeader = {'restrict-access': 'true',
                    'Authorization': "Bearer %s" % token}

    file = {'file': (imagefile, open(imagefile, 'rb'))}
    try:
        r = requests.post("%s/%s/%s/chatfiles/" %(url,org,app), files=file, headers=uploadHeader)
        if r.status_code == 200:
            data = r.json()
            imageurl = data['uri'] + '/' + data['entities'][0]['uuid']
            return imageurl
        else:
            print "upload images failed",r.status_code,r.content
    except requests.exceptions.ConnectionError,e:
        print "Your url is error: %s" %e

def sendImage(imageurl,userlist):
    sendImagebody = {"target_type": "users",
                     "target": userlist,
                     "msg": {
                         "type": "img",
                         "url": imageurl,
                         "filename": "lorex.jpg",
                         "secret": "yK5a2qWnEeaRcJUaVNstNOVVTjuqBVyib-rF7Vw1xSVn28X4",
                         "size": {
                             "width": 780,
                             "height": 1480
                         }
                     },
                     "from": "rest"
                     }
    r = requests.post("%s/%s/%s/messages" % (url, org, app), data=json.dumps(sendImagebody), headers=headers)
    if r.status_code == 200:
        print "send image message to userlist success"
    else:
        print "send image message failed, error status code is: %s" % r.status_code
        print json.dumps(r.json(), sort_keys=True, indent=2)

def sendFiled(imageurl,userlist):
    sendFilebody = {"target_type": "users",
                     "target": userlist,
                     "msg": {
                         "type": "file",
                         "url": imageurl,
                         "filename": "lorex.jpg",
                         "secret": "yK5a2qWnEeaRcJUaVNstNOVVTjuqBVyib-rF7Vw1xSVn28X4"
                     },
                     "from": "rest"
                     }
    r = requests.post("%s/%s/%s/messages" % (url, org, app), data=json.dumps(sendFilebody), headers=headers)
    if r.status_code == 200:
        print "send files message to userlist success"
    else:
        print "send files message failed, error status code is: %s" % r.status_code
        print json.dumps(r.json(), sort_keys=True, indent=2)


def addtoBlack(user,blackuser):
    blackBody = {"usernames":[blackuser]}
    r = requests.post("%s/%s/%s/users/%s/blocks/users" % (url, org, app,user), data=json.dumps(blackBody), headers=headers)
    if r.status_code != 200:
        print "add blackuser %s to user %s black list failed, error status code is: %s" % (blackuser, user, r.status_code)
        print json.dumps(r.json(), sort_keys=True, indent=2)

def getBlackList(user):
    r = requests.get("%s/%s/%s/users/%s/blocks/users" % (url, org, app, user),headers=headers)
    if r.status_code == 200:
        data = r.json()
        print "user %s blacklist is: %s" %(user,data["data"])
    else:
        print "get user black list failed,error status code is: %s" % r.status_code
        print json.dumps(r.json(), sort_keys=True, indent=2)




PubGrpBody = {
        "groupname": "public_group1",
        "desc": "RST created group",
        "public": true,
        "maxusers": 800,
        "approval": false,
        "owner": user1,
        "members": userlist
    }

PubGrpVerify = {
    "groupname":"public_group2",
    "desc":"RST created group",
    "public":true,
    "allowinvites":false,
    "maxusers":800,
    "approval":true,
    "owner":user1,
    "members":userlist
}

PrivateGrp = {
    "groupname":"private_group1",
    "desc":"RST created group",
    "public":false,
    "allowinvites":false,
    "maxusers":800,
    "approval":true,
    "owner":user1,
    "members":userlist
}

privateGrpAllow = {
    "groupname":"private_group2",
    "desc":"RST created group",
    "public":false,
    "allowinvites":true,
    "maxusers":800,
    "approval":true,
    "owner":user1,
    "members":userlist
}

def greatePublic1(createBody):
    r = requests.post("%s/%s/%s/chatgroups" % (url, org, app), data=json.dumps(createBody), headers=headers)
    if r.status_code == 200:
        data1 = r.json()
        groupid = data1['data']['groupid']
        print "create  group %s success" % (createBody["groupname"])
        return groupid
    else:
        print "create  group % failed" % createBody["groupname"]
        print json.dumps(r.json(), sort_keys=True, indent=2)
        return None

def getMemberlist(groupid):
    get = requests.get("%s/%s/%s/chatgroups/%s/users" % (url, org, app, groupid), headers=headers)
    if get.status_code == 200:
        data2 = get.json()
        newmembers = []
        for a in data2['data']:
            for x, y in a.items():
                newmembers.append(y)
        print "group %s members list is: %s" %(groupid,newmembers)
    else:
        print "get group members list failed"
        print json.dumps(get.json(), sort_keys=True, indent=2)
        #exit()

# send group message
def sendGroupMess(grouplist,messages):
    sendmessBody = { "target_type":"chatgroups",
             "target":grouplist,
             "msg":{
             "type":"txt",
             "msg":messages
            },
            "from":"rest"
    }
    r = requests.post("%s/%s/%s/messages" %(url, org, app),data=json.dumps(sendmessBody),headers=headers)
    if r.status_code == 200:
        print "send message %s to group success" % messages
    else:
        print "send message failed, status code is: %s" % r.status_code
        print json.dumps(r.json(), sort_keys=True, indent=2)
        exit()

def getOfflineMess(user):
    get = requests.get("%s/%s/%s/users/%s/offline_msg_count" % (url, org, app, user), headers=headers)
    if get.status_code == 200:
        data = get.json()
        print data["data"]
    else:
        print "get offline message failed, status code is: %s" % get.status_code
        print json.dumps(get.json(), sort_keys=True, indent=2)
        #exit()

def CreateRoom():
    CteroomBody={
    "name":"rest_chatroom",
    "description":"Rest create chatroom",
    "maxusers":5000,
    "owner":user1
    }
    r = requests.post("%s/%s/%s/chatrooms" % (url, org, app), data=json.dumps(CteroomBody), headers=headers)
    if r.status_code == 200:
        data = r.json()
        if data['data']['id']:
            RoomID = data['data']['id']
            print "create chat room success roomid is: %s" % RoomID
            return RoomID
        else:
            print "create chat room failed"
            return None
    else:
        print "create chat room failed, status code is: %s" % r.status_code
        print json.dumps(r.json(), sort_keys=True, indent=2)
        return None

def addRoomMember(roomid,userlist):
    MultiMemBody = {"usernames": userlist}
    r = requests.post("%s/%s/%s/chatrooms/%s/users" % (url, org, app, roomid), data=json.dumps(MultiMemBody),headers=headers)
    if r.status_code != 200:
        print "add multi user to chatroom failed, error status code is: %s" % r.status_code
        print json.dumps(r.json(), sort_keys=True, indent=2)
        exit()
    get = requests.get("%s/%s/%s/chatrooms/%s" % (url, org, app, roomid),headers=headers)
    if get.status_code == 200:
        data1 = get.json()
        roomuser = []
        for a in data1["data"][0]['affiliations']:
            for x, y in a.items():
                roomuser.append(y)
        print "chat roomid is %s member list is: %s" % (roomid,roomuser)
    else:
        print "get chat room detail failed, error status code is: %s" % get.status_code
        exit()

def addRoomAdmin(roomid,roomadmin):
    AddAdminBody = {"newadmin": roomadmin}
    r = requests.post("%s/%s/%s/chatrooms/%s/admin" % (url, org, app, roomid), data=json.dumps(AddAdminBody),headers=headers)
    if r.status_code != 200:
        print "add chatroom admin failed, error status code is: %s" % r.status_code
        print json.dumps(r.json(), sort_keys=True, indent=2)

def getroomAdminlist(roomid):
    get = requests.get("%s/%s/%s/chatrooms/%s/admin" % (url, org, app, roomid), headers=headers)
    if get.status_code == 200:
        data2 = get.json()
        print "chatroom %s admin list is: %s" % (roomid,data2["data"])
    else:
        print "get chatroom admin list failed, error status code is: %s" % get.status_code
        print json.dumps(get.json(), sort_keys=True, indent=2)

if __name__ == "__main__":
    #great user
    greateUser(userlist)

    #add friend
    addFriend(userlist)

    #add black user
    addtoBlack(user1, user8)
    addtoBlack(user1, user9)
    addtoBlack(user2, user8)
    addtoBlack(user2, user9)
    addtoBlack(user3, user8)
    addtoBlack(user3, user9)
    getBlackList(user1)
    getBlackList(user2)
    getBlackList(user3)

    #send message to all test user
    for mess in range(101,116):
        time.sleep(0.5)
        sendMess(userlist,mess)

    imageurl = uploadImage('scenery.png')
    sendImage(imageurl, userlist)
    sendImage(imageurl, userlist)
    sendFiled(imageurl, userlist)
    sendFiled(imageurl, userlist)

    time.sleep(2)
    for user in userlist:
        getOfflineMess(user)

    #create group
    grouplist = []
    groupid1 = greatePublic1(PubGrpBody)
    getMemberlist(groupid1)
    groupid2 = greatePublic1(PubGrpVerify)
    getMemberlist(groupid2)
    groupid3 = greatePublic1(PrivateGrp)
    getMemberlist(groupid3)
    groupid4 = greatePublic1(privateGrpAllow)
    getMemberlist(groupid4)
    grouplist.append(groupid1)
    grouplist.append(groupid2)
    grouplist.append(groupid3)
    grouplist.append(groupid4)

    #print "group list is: %s" % grouplist

    #send group message
    for messages in range(101,116):
        time.sleep(0.5)
        sendGroupMess(grouplist,messages)

    #chatroom
    roomlist = []
    roomid = CreateRoom()
    addRoomMember(roomid,userlist)
    addRoomAdmin(roomid,user8)
    addRoomAdmin(roomid,user9)
    getroomAdminlist(roomid)
    roomlist.append(roomid)

    roomid2 = CreateRoom()
    addRoomMember(roomid2, userlist)
    addRoomAdmin(roomid2,user8)
    addRoomAdmin(roomid2,user9)
    getroomAdminlist(roomid2)
    roomlist.append(roomid2)

    roomid3 = CreateRoom()
    addRoomMember(roomid3, userlist)
    addRoomAdmin(roomid3,user8)
    addRoomAdmin(roomid3,user9)
    getroomAdminlist(roomid3)
    roomlist.append(roomid3)

    file = open("%s.txt" % clientname, "wb")
    mydic = {}
    mydic["groupid"] = grouplist
    mydic["roomid"] = roomlist
    json.dump(mydic,file)
    file.close()

    time.sleep(2)
    print "offline message number is: "
    for user in userlist:
        getOfflineMess(user)

