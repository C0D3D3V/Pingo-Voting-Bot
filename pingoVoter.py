#!/usr/bin/env python2
# -*- coding: utf-8 -*-

#  Copyright 2017 Daniel Vogt
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.



import cookielib
import urllib2
import urllib
import io
import os
import os.path
import hashlib
import sys
import stat
import md5
import re
import filecmp
import sys

from datetime import datetime
from ConfigParser import ConfigParser
from random import randint

try:
   from bs4 import BeautifulSoup
except Exception, e:
   print("Module BeautifulSoup4 is missing!")
   exit(1)

try:
   from colorama import init
except Exception, e:
   print("Module Colorama is missing!")
   exit(1)

try:
   from termcolor import colored
except Exception, e:
   print("Module Termcolor is missing!")
   exit(1)

# use Colorama to make Termcolor work on Windows too
init()


#utf8 shit
reload(sys)
sys.setdefaultencoding('utf-8')

filesBySize = {}

def walker(arg, dirname, fnames):
    d = os.getcwd()
    os.chdir(dirname)
    try:
        fnames.remove('Thumbs')
    except ValueError:
        pass
    for f in fnames:
        if not os.path.isfile(f):
            continue
        size = os.stat(f)[stat.ST_SIZE]
        if size < 100:
            continue
        if filesBySize.has_key(size):
            a = filesBySize[size]
        else:
            a = []
            filesBySize[size] = a
        a.append(os.path.join(dirname, f))
    os.chdir(d)

def checkQuotationMarks(settingString):
   if not settingString is None and settingString[0] == "\"" and settingString[-1] == "\"":
      settingString = settingString[1:-1]
   if settingString is None:
      settingString = ""
   return settingString
 

def addSlashIfNeeded(settingString):
   if not settingString is None and not settingString[-1] == "/":
      settingString = settingString + "/"
   return settingString


#Log levels:
# - Level 0: Minimal Information + small Errors
# - Level 1: More Information + Successes 
# - Level 2: Doing Statemants + Found information
# - Level 3: More Errors + More Infos
# - Level 4: More Doing Statements + Dowload Info + Scann Dublicates
# - Level 5: More Download Info + More Info about dublicates

 
def log(logString, level=0):
   if level <= int(loglevel):
      if level == 0:
         print(datetime.now().strftime('%H:%M:%S') + " " + logString)
      elif level == 1:
         print(colored(datetime.now().strftime('%H:%M:%S') + " " + logString, "green")) 
      elif level == 2:
         print(colored(datetime.now().strftime('%H:%M:%S') + " " + logString, "yellow"))
      elif level == 3:
         print(colored(datetime.now().strftime('%H:%M:%S') + " " + logString, "red"))
      elif level == 4:
         print(colored(datetime.now().strftime('%H:%M:%S') + " " + logString, "magenta"))
      elif level == 5:
         print(colored(datetime.now().strftime('%H:%M:%S') + " " + logString, "cyan"))




def donwloadFile(downloadFileResponse):
   log("Download has started.", 4)
       
   downloadFileContent = ""
   
   if downloadFileResponse is None:
      log("Faild to download file", 4)
      return ""

   try:
       total_size = downloadFileResponse.info().getheader('Content-Length').strip()
       header = True
   except Exception:
       log("No Content-Length available.", 5)
       header = False # a response doesn't always include the "Content-Length" header
          
   if header:
       total_size = int(total_size)
         
   bytes_so_far = 0
        
   while True:
       downloadFileContentBuffer = downloadFileResponse.read(8192)
       if not downloadFileContentBuffer: 
           break
           
       bytes_so_far += len(downloadFileContentBuffer) 
       downloadFileContent = downloadFileContent + downloadFileContentBuffer
              
       if not header: 
          log("Downloaded %d bytes" % (bytes_so_far), 5)
           
       else:
          percent = float(bytes_so_far) / total_size
          percent = round(percent*100, 2)
          log("Downloaded %d of %d bytes (%0.2f%%)\r" % (bytes_so_far, total_size, percent), 5)
            
          
   log("Download complete.", 4)
   return downloadFileContent

 
 

 

conf = ConfigParser()
project_dir = os.path.dirname(os.path.abspath(__file__))
conf.read(os.path.join(project_dir, 'config.ini'))


loglevel = checkQuotationMarks(conf.get("other", "loglevel"))
votingtimes = int(conf.get("voting", "times"))
  
authentication_url = addSlashIfNeeded(checkQuotationMarks(conf.get("auth", "url")))

  

cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
opener.addheaders = [('User-agent', 'HeyThanksForWatchingThisAgenet')]
urllib2.install_opener(opener)



log("Pingo Voter started working.")

# Connection established?
log("Try to get options...", 1)
 
#response = urllib2.urlopen(req)
try:
   responseLogin = urllib2.urlopen(authentication_url, timeout=10)
except Exception:
   log("Connection lost! It is not possible to connect to pingo!")
   exit(1)
LoginContents = donwloadFile(responseLogin)
  


LoginSoup = BeautifulSoup(LoginContents, "lxml") 

LoginStatusConntent = LoginSoup.find(id="survey-content")
if LoginStatusConntent is None : 
   log("Cannot connect to pingo or no survay has started. Crawler is not logged in. Check your login data.") 
   exit(1)


OptionList = LoginStatusConntent.find_all(class_="center-block well") #("input", {"name":"option"})

optionsValues = []

for option in OptionList:
   log("Voting Option: " + option.text)
   optionValue = option.find("input", {"name":"option"})
   optionsValues.append([option.text, optionValue.get("value")])

 

log("Got all options!", 2)
 
 

mainpageURL = responseLogin.geturl()
 



log("Start Vottong...", 1)
 
anzOptionen = len(optionsValues)
anzDurch = anzOptionen * votingtimes
anzVotet = 0

while anzVotet < anzDurch:
   anzVotet += 1

   cj = cookielib.CookieJar()
   opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
   opener.addheaders = [('User-agent', 'HeyThanksForWatchingThisAgenet' + str(randint(0,9999999)))]
   urllib2.install_opener(opener)
   
   try:
      responseLogin = urllib2.urlopen(authentication_url, timeout=10)
   except Exception:
      log("Connection lost! It is not possible to connect to pingo!")
      anzVotet += anzOptionen
      continue
   LoginContents = donwloadFile(responseLogin)
     
   
   LoginSoup = BeautifulSoup(LoginContents, "lxml") 
   
   if LoginSoup is None:
      log("Something faild! An empty file was returned.")
      anzVotet += anzOptionen
      continue

   option_vote = optionsValues[(anzVotet - 1) % anzOptionen][1]
   authenticity_tokenSoup = LoginSoup.find("input", {"name":"authenticity_token"})

   if authenticity_tokenSoup is None:
      log("Something faild! Authenticity_token was not found.")
      anzVotet += anzOptionen
      continue

   authenticity_token = authenticity_tokenSoup.get("value")

   id_voteSoup = LoginSoup.find("input", {"name":"id"})

   if id_voteSoup is None:
      log("Something faild! Id_vote was not found.")
      anzVotet += anzOptionen
      continue
      
   id_vote = id_voteSoup.get("value")
   
   payload = {
       'utf8': '/',
       'authenticity_token': authenticity_token,
       'option': option_vote,
       'id': id_vote,
   }
    
     
   data = urllib.urlencode(payload)
   
   req = urllib2.Request("http://pingo.upb.de/vote", data)
   #response = urllib2.urlopen(req)
   log("Try to vote.", 2)
   try:
      responseLogin = urllib2.urlopen(req, timeout=10)
   except Exception:
      log("Connection lost! It is not possible to connect to pingo!")
      anzVotet += anzOptionen
      continue
   log("Voted for: " + optionsValues[(anzVotet - 1) % anzOptionen][1])
  


log("Voting Complete")
