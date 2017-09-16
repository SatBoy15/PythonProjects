'''---------------------'''
'WeSchool.com - Api2Python'
'Programmed  by  SatBoy15 '
'''---------------------'''
import urllib2

api = 'https://api.weschool.com/oauth/v2/token'

user = '_your_username_'
password = 'your_password'

if user != '_your_username_':
    if password == 'your_password':
        print 'Please set your Password'
        exit()
else:
    if password != 'your_password':
        print 'Please set your Username'
        exit()
    else:
       print 'Please Set your Username and Password'
       exit()

def json2list(json):
    lista = json.replace('{','').replace('}','').replace('"','').split(',')
    for i in lista:
        if i.find('\\')>-1:
            lista[lista.index(i)]=i.replace('\\','')
    return lista

def getClientInfo():
    client_infopage_req = urllib2.Request('http://app.weschool.com/js/classroom-lib.min.js')
    client_infopage_req.add_header('Referer','http://app.weschool.com/#login')
    client_infopage_req.add_header('User-Agent','Mozilla (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36')
    client_infopage = urllib2.urlopen(client_infopage_req).read()
    posclid = client_infopage.find('__CLIENT_ID__')
    posfine = client_infopage.find(',__GRANT_TYPE',posclid)
    clientinfo = client_infopage[posclid:posfine].replace('"','').split(",")
    clientinfo[0]= clientinfo[0].split('__CLIENT_ID__=')[1]
    clientinfo[1]= clientinfo[1].split('__CLIENT_SECRET__=')[1]
    return clientinfo

def getTokenv1(clientinfos):
    client_id, client_secret = clientinfos
    call1 = '?client_id=%s&client_secret=%s&grant_type=client_credentials&scope=client' % (client_id,client_secret)
    tokpage = urllib2.urlopen(api+call1).read()
    token = json2list(tokpage)[0].split('access_token:')[1]
    return token

def getTokenv2(clientinfos):
    client_id, client_secret = clientinfos
    call1 = '?client_id=%s&client_secret=%s&grant_type=password&password=%s&scope=user&username=%s' % (clientinfos[0],clientinfos[1],password,user)
    tokpage = urllib2.urlopen(api+call1).read()
    token1 = json2list(tokpage)[0].split('access_token:')[1]
    token2 = json2list(tokpage)[4].split('refresh_token:')[1]
    return [token1,token2]

def getMe(user,password,logintokens):
    token1 = logintokens[0]
    token2 = logintokens[1]
    import time
    meurl ='https://api.weschool.com/v1/users/me?_='+ str(time.time()).replace('.','')+'0'
    reqmepage = urllib2.Request(mewallurl)
    reqmepage.add_header('Referer','http://app.weschool.com/#login')
    reqmepage.add_header('User-Agent','Mozilla (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36')
    reqmepage.add_header('Authorization','Bearer %s' % token1)
    reqmepage.add_header('Cookie','_weschool_client_timezone=Europe/Berlin')
    me = json2list(urllib2.urlopen(reqmepage).read())
    return me

def getWall(user,password,logintokens):
    token1 = logintokens[0]
    token2 = logintokens[1]
    import time, json
    wallurl ='https://api.weschool.com/v1/notifications?_='+ str(time.time()).replace('.','')+'0'
    reqwallpage = urllib2.Request(wallurl)
    reqwallpage.add_header('Referer','http://app.weschool.com/#login')
    reqwallpage.add_header('User-Agent','Mozilla (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36')
    reqwallpage.add_header('Authorization','Bearer %s' % token1)
    reqwallpage.add_header('Cookie','_weschool_client_timezone=Europe/Berlin')
    walljson = urllib2.urlopen(reqwallpage).read()
    parsed_wall = json.loads(walljson)
    return parsed_wall
