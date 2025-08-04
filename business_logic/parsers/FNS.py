import requests, json, os, datetime, traceback; from time import sleep
s = requests.Session()


def suggest_fsn(inn):
    r = s.get("https://egrul.nalog.ru/index.html",
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0",
            "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
            }
        )

    req = requests.Request(
        'POST',
        'https://egrul.nalog.ru/',
        data=b'vyp3CaptchaToken=&page=&query='+bytes(inn)+b'&region=&PreventChromeAutocomplete=', # хабр почему то заменяет rеg в слове rеgion (буква е заменена на русскую) на знак ®, магия
        headers = {
        "Host": "egrul.nalog.ru",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": "https://egrul.nalog.ru/index.html",
        "Content-Type": "application/x-www-form-urlencoded",
        "X-Requested-With": "XMLHttpRequest"
        }
        )

    r = s.prepare_request(req)
    r = s.send(r)
    #print(r.text)
    t = json.loads(r.text)['t']

    sleep(0.5)

    r = s.get("https://egrul.nalog.ru/search-result/"+str(t),
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0",
            "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
            "Referer": "https://egrul.nalog.ru/index.html"
            }
        )

    #print(r.text)
    jsn = json.loads(r.text)

    try:
        while True:
            if jsn['status'] != 'wait': break
            sleep(0.2)
    except Exception:
        pass

    try:
        item = (jsn["rows"])[0]
        if str(item['tot']) != '0':
            if len(item['n']) < 50: name = str(item['n'])
            else: name = str(item['i'])

            name = name.replace('"',"'").replace('\\','⧵').replace('/','⁄').replace('|','¦').replace(':',';').replace('*','✱').replace('?','').replace('<','«').replace('>','»')

            try:
                os.mkdir(name)
            except Exception:
                pass
                name = name + ' '+str(datetime.datetime.strftime(datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=3))),'%x %X %Z')).replace('/','.').replace(':','-')
                os.mkdir(name)

            f = open(name+'\\'+name+'.txt','w+',encoding='utf-8')
            f.write('по состоянию на ' + str(datetime.datetime.strftime(datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=3))),'%x %X %Z')).replace('/','.')+'\n'+str(item))
            f.close()

            t = item['t']

            r = s.get("https://egrul.nalog.ru/vyp-request/"+str(t),
                headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0",
                    "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
                    "Referer": "https://egrul.nalog.ru/index.html"
                    }
                )
            sleep(0.5)
            while True:
                r = s.get("https://egrul.nalog.ru/vyp-status/"+str(t),
                    headers={
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0",
                        "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
                        "Referer": "https://egrul.nalog.ru/index.html"
                        }
                    )
                st = json.loads(r.text)['status']
                if st == 'ready': break
                sleep(0.5)

            r = s.get("https://egrul.nalog.ru/vyp-download/"+str(t),
                    headers={
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0",
                        "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
                        "Referer": "https://egrul.nalog.ru/index.html"
                        }
                    )

            #print(r.text)

            f = open(name+'\\'+name+' выписка.pdf','wb+')
            f.write(r.content)
            f.close()

    except Exception as e:
        print(e)
        traceback.print_exc()
        pass