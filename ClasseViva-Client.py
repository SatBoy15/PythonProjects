
'''''''''''''''''''''
'                   '
' ClasseViva2Python '
'                   '
'   coded by Albi   '
'                   '
'''''''''''''''''''''

import urllib, urllib2, json, base64

baseurl = 'https://web.spaggiari.eu/'

try:
    loginfile = file('classeviva_python-login.json','r')
    file1 = json.loads(loginfile.read())
    print 'Bentornato, il programma e\' in caricamento...\n'
    user = file1['username']
    passw = base64.b64decode(file1['password'])
    loginfile.close()
except:
    print 'Benvenuto/a, mi sembra che non hai ancora inserito i tuoi dati...\n'
    user = raw_input('Inserisci l\' Utente:\n---->')
    passw = raw_input('Inserisci la Password:\n---->')
    loginfile = file('classeviva_python-login.json','w')
    jsonfile = {
        'username':user,
        'password':base64.b64encode(passw),
        }
    json.dump(jsonfile, loginfile)
    loginfile.close()

def Login(user,passw):
    post_args = {
        'cid':'',
        'pin':'',
        'target':'',
        'uid':user,
        'pwd':passw,
        }
    loginurl = baseurl+'auth/app/default/AuthApi4.php?a=aLoginPwd'
    rapicall1 = urllib2.Request(loginurl,urllib.urlencode(post_args))
    rapicall1.add_header('Cookie','weblogin='+user)
    rapicall1.add_header('Referer',baseurl)
    apicall1 = urllib2.urlopen(rapicall1)
    return [json.loads(apicall1.read()),apicall1.info().getheader('Set-Cookie').split(';')[0].split('=')[1]]
#Login(user,passw)[0]['data']['auth']['accountInfo']

def getUsername(phpsessid,user):
    link = 'https://web.spaggiari.eu/tools/app/default/get_username.php'
    rpage = urllib2.Request(link)
    rpage.add_header('Cookie','PHPSESSID='+phpsessid+'; weblogin='+user)
    rpage.add_header('Referer','https://web.spaggiari.eu/home/app/default/menu_webinfoschool_studenti.php')
    rpage.add_header('X-Requested-With','XMLHttpRequest')
    page = urllib2.urlopen(rpage)
    return page.read()

def getHome(user,passw):
    post_args={
        'custcode':'',
        'login':user,
        'password':passw,
        'pin':'',
        }
    logininfo = Login(user,passw)
    infos = getUsername(logininfo[1],user)
    rpage = urllib2.Request(baseurl+'home/app/default/login_ok_redirect.php', urllib.urlencode(post_args))
    rpage.add_header('Cookie','PHPSESSID='+logininfo[1]+'; weblogin='+user+'; LAST_REQUESTED_TARGET=cvv')
    rpage.add_header('Referer','https://web.spaggiari.eu/home/app/default/login.php?target=&mode=')
    rpage.add_header('Content-Type','application/x-www-form-urlencoded')
    rpage.add_header('User-Agent','Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:37.0) Gecko/20100101 Firefox/37.0')
    rpage.add_header('Upgrade-Insecure-Requests','1')
    rpage.add_header('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    rpage.add_header('Accept-Language','it-IT,it;q=0.8,en-US;q=0.5,en;q=0.3')
    rpage.add_header('Host','web.spaggiari.eu')
    rpage.add_header('DNT','1')
    rpage.add_header('Content-Length','74')
    page = urllib2.urlopen(rpage)
    headers = page.info()
    page = page.read()
    azioni = []
    posazione = page.find('<a href=')
    while posazione > -1:
        azioni.append(page[posazione+8:page.find('>',posazione+1)])
        posazione = page.find('<a href=',posazione+1)
    for i in azioni:
        ind = azioni.index(i)
        i = i.replace('\t','').replace('\n','').replace(':link_attribs:','')
        if i.find('title=')>-1:
            i = i.replace('title=','@')
        i = i.replace('php ','php')
        if i.find('#')>-1:
            i = i.split('#')[0]
        azioni[ind] = i
    azioni2 = []
    for i in azioni:
        i = i[1:i.find('"',2)].replace('"','')
        #+i[i.find('@'):]
        i = i.replace('php ','php').replace('../../../',baseurl)
        if i.find('xasapi')>-1:
            i = (baseurl+i).replace('&amp;','&')
        if i.find('/acc/')>-1:
            i = baseurl[:-1]+i
        i = i.replace('consultasingolo.ph','consultasingolo.php')
        azioni2.append(i.replace('php ','php').replace('../../../',baseurl))
    azioni_final = list(set(azioni2))
    for i in azioni_final:
        index = azioni_final.index(i)
        if i.find('@')>-1:
            azioni_final[index] = i.split('@')[0]
    return [azioni_final,json.loads(infos),logininfo[1]]

def getLezioni(user,cookie):
    url = baseurl+'fml/app/default/regclasse_lezioni_xstudenti.php'
    import urllib2
    rpage = urllib2.Request(url)
    rpage.add_header('Cookie','PHPSESSID='+cookie+'; weblogin='+user+'; LAST_REQUESTED_TARGET=cvv')
    rpage.add_header('User-Agent','Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:37.0) Gecko/20100101 Firefox/37.0')
    rpage.add_header('Accept','text/html,*/*')
    page = urllib2.urlopen(rpage).read()
    postitle = page.find('<div  title="')
    materie = []
    while postitle>-1:
        posid = page.find('materia_id',postitle+1)
        posautori = page.find('autori_id',postitle+1)
        autori = page[posautori+11:page.find('"',posautori+12)]
        materia = page[posid+12:page.find('"',posid+13)]
        titolo = page[postitle+13:page.find('"',postitle+14)]
        materie.append(titolo+'@'+materia+'@'+autori)
        postitle = page.find('<div  title="', postitle+1)
    cont = 1
    for i in materie:
        print str(cont)+ ' - '+i.split('@')[0]
        cont += 1
    while True:
        print '\nScrivi il numero della materia corrispondente:'
        scelta = input('---->')
        if scelta>cont-1:
            print '\nIl numero inserito non va bene, riprova...'
        if scelta<0:
            print '\nIl numero inserito non va bene, riprova...'
        if 0<scelta<=cont-1:
            break
    materia = materie[scelta-1].split('@')[0]
    idmateria = materie[scelta-1].split('@')[1]
    profs = materie[scelta-1].split('@')[2]
    url2 = baseurl+'fml/app/default/regclasse_lezioni_xstudenti.php?action=loadLezioni&materia=%s&autori_id=%s' % (idmateria,profs)
    rpagemateria = urllib2.Request(url2)
    rpagemateria.add_header('User-Agent','Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:37.0) Gecko/20100101 Firefox/37.0')
    rpagemateria.add_header('Accept','text/html,*/*')
    rpagemateria.add_header('Cookie','PHPSESSID='+cookie+'; weblogin='+user+'; LAST_REQUESTED_TARGET=cvv')
    rpagemateria.add_header('Referer',url)
    pagemateria = urllib2.urlopen(rpagemateria).read()
    postr = pagemateria.find('<tr')
    lezioniparse = []
    while postr>-1:
        pos1 = pagemateria.find(':studente_id:',postr+1)+16
        nameprof = pagemateria[pos1:pagemateria.find('</td',pos1+1)]
        posspan = pagemateria.find('<span class',pos1+1)
        data = pagemateria[posspan+15:pagemateria.find('</span',posspan+1)]
        posarg = pagemateria.find('align="',posspan+1)
        arg = pagemateria[posarg+13:pagemateria.find('</td',posarg+1)]
        lezioniparse.append(nameprof+'@'+data+'@'+arg)
        postr = pagemateria.find('<tr',postr+1)
    for i in lezioniparse:
        i = i.replace('\n','')
        print i.split('@')[0]+' - '+i.split('@')[1]+' - '+i.split('@')[2]
    #return pagemateria

def getAgenda(user,cookie):
    import urllib2,urllib,time
    ref = baseurl+'fml/app/default/agenda_studenti.php'
    url = ref+'?ope=get_events'
    timenow = int(time.time()/100000)*100000
    args = {
        'classe_id':'',
        'end':timenow+1296000,
        'gruppo_id':'',
        'start':timenow-1296000,
        }
    rpage = urllib2.Request(url, urllib.urlencode(args))
    rpage.add_header('User-Agent','Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:37.0) Gecko/20100101 Firefox/37.0')
    rpage.add_header('Cookie','PHPSESSID='+cookie+'; weblogin='+user+'; LAST_REQUESTED_TARGET=cvv')
    rpage.add_header('Referer',ref)
    page = urllib2.urlopen(rpage).read()
    lista = json.loads(page)
    for i in lista:
        print i['autore_desc']+' - '+i['start'].split(' ')[0]+' - '+i['nota_2']

def getVoti(user,cookie):
    import urllib2
    url = baseurl+'cvv/app/default/genitori_voti.php'
    rpage = urllib2.Request(url)
    rpage.add_header('User-Agent','Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:37.0) Gecko/20100101 Firefox/37.0')
    rpage.add_header('Cookie','PHPSESSID='+cookie+'; weblogin='+user+'; LAST_REQUESTED_TARGET=cvv')
    rpage.add_header('Referer','https://web.spaggiari.eu/home/app/default/menu_webinfoschool_studenti.php?custcode=')
    page = urllib2.urlopen(rpage).read()
    materie = []
    posmateria = page.find('<td width="350')
    while posmateria>-1:
        materia = page[page.find('>',posmateria+1)+1:page.find('&nbsp',posmateria+1)]
        while True:
            if materia[-1] == '	':
                materia = materia.replace('	','')
            else:
                break
            
        materie.append(materia+'@'+str(page.find('>',posmateria+1)+1))
        posmateria = page.find('<td width="350',posmateria+1)
    posclass = page.find('<span  class="')
    voti = []
    while posclass>-1:
        posvototype = page.find('cella_div',posclass+1)
        posvoto1 = page.find('p align=',posvototype+1)
        datavoto = page[page.find('data">',posclass+1)+6:page.find('</span',posclass+1)]
        voto = page[page.find('">',posvoto1+1)+2:page.find('</p',posvoto1+1)]
        vototype = page[page.find('f_reg_',posvototype+1)+6:page.find('"',posvototype+1)].split('_')[1]
        for i in materie:
            if posvoto1>int(i.split('@')[1]):
                materia = i.split('@')[0]
        if datavoto.find('/')>-1:
            voti.append(str(materia)+'@'+datavoto+'@'+voto+'@'+vototype)
        posclass = page.find('<span  class="',posclass+1)
    
    for i in voti:
        tempvoto = i.split('@')
        print tempvoto[0]+' - '+tempvoto[1]+' - '+tempvoto[2]+' - '+tempvoto[3]
        

def getCircolari(user,cookie,codstud):
    import urllib2
    url = baseurl+'sif/app/default/bacheca_utente.php'
    rpage = urllib2.Request(url)
    rpage.add_header('User-Agent','Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:37.0) Gecko/20100101 Firefox/37.0')
    rpage.add_header('Cookie','PHPSESSID='+cookie+'; weblogin='+user+'; LAST_REQUESTED_TARGET=cvv')
    rpage.add_header('Referer','https://web.spaggiari.eu/home/app/default/menu_webinfoschool_studenti.php?custcode=')
    page = urllib2.urlopen(rpage).read()
    poscirc1 = page.find('<td colspan="32" align="left" style="padding-left:10px;" class="bb_grey">')
    cont = 1
    circolari = []
    while poscirc1>-1:
        title = page[page.find('_14',poscirc1+1)+5:page.find('</div',poscirc1+1)].replace('\n','')
        postype = page.find('_10',poscirc1+1)+6
        posdata = page.find('12">',poscirc1+1)+4
        poscomid = page.find('comunicazione_id',poscirc1+1)
        tipo = page[postype:page.find('</div',postype+1)].replace('\n','').replace('n_pubbl hidden">','')
        data = page[posdata:page.find('</div',posdata+1)].replace('\n','')
        comunicazione = page[poscomid+18:page.find('"',poscomid+18)].replace('\n','')
        circolari.append(title+'@'+data+'@'+tipo+'@'+comunicazione)
        poscirc1 = page.find('<td colspan="32" align="left" style="padding-left:10px;" class="bb_grey">',poscirc1+1)
    for i in circolari:
        mini = i.split('@')
        print str(cont)+' - '+mini[0]+' - '+mini[2]+'\n'
        cont += 1
    while True:
        print '\nScrivi il numero della circolare corrispondente:'
        scelta = input('---->')
        if scelta>cont-1:
            print '\nIl numero inserito non va bene, riprova...'
        if scelta<0:
            print '\nIl numero inserito non va bene, riprova...'
        if 0<scelta<=cont-1:
            break
    idcircolare = circolari[scelta-1].split('@')[-1]
    nomecirc = circolari[scelta-1].split('@')[0].replace('\n','')
    import urllib
    print 'Sto Caricando il link ...\n'
    urldownload=url+'?action=file_download&com_id=%s' % idcircolare
    rpdf = urllib2.Request(urldownload)
    rpdf.add_header('User-Agent','Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:37.0) Gecko/20100101 Firefox/37.0')
    rpdf.add_header('Cookie','PHPSESSID='+cookie+'; weblogin='+user+'; LAST_REQUESTED_TARGET=cvv')
    rpdf.add_header('Referer',url)
    pdfread = urllib2.urlopen(rpdf)
    print 'Scrivo su File...\n'
    pdffile = file('circolare_'+codstud+'_'+str(scelta)+'.pdf','wb')
    pdffile.write(pdfread.read())
    pdfread.close()
    pdffile.close()
    print 'File Scritto.'
    

def getAssenze(user,cookie):
    print 'Aspetto di fare un\' assenza per implementare questo modulo. hahaha...\n'

def Registro(user,home):
    while True:
        print "1 - Visualizza le lezioni\n\n2 - Guarda l'Agenda\n\n3 - Guarda i Voti\n\n4 - Guarda le Circolari\n\n5 - Guarda le Assenze\n"
        azione = input('\nScegli il numero dell\' azione da fare:\n\n---->')
        if azione == 1:
            getLezioni(user,home[2])
        elif azione == 2:
            getAgenda(user,home[2])
        elif azione == 3:
            getVoti(user,home[2])
        elif azione == 4:
            getCircolari(user,home[2],home[1]['username'])
        elif azione == 5:
            getAssenze(user,home[2])
        else:
            print '\nNon hai scelto nessuna azione, Arrivederci!'
            break
        voglia = input('\nVuoi ancora usare il programma? (1:Si,0:No)\n\n---->')
        if voglia == 0:
            print 'Arrivederci!'
            break
        elif voglia == 1:
            print '\nOK, scegli di nuovo un\' azione:'
        else:
            print '\nNon hai scelto ne\' si ne\' no, quindi Arrivederci!'
            break
    
a = getHome(user,passw)

print 'Benvenuto/a '+a[1]['nome']+', '+a[1]['username']+'\n\nEcco le azioni che puoi fare:\n\n'

Registro(user,a)
