from __future__ import print_function
import whois
import json
import os
import os.path
import time
import sys
import emailSender
import sms
from datetime import datetime
from consoleColors import consoleColors
from whois.parser import PywhoisError

#global constants
domainsPath = "../domains.txt"
savedData = "../saved_data/data.json"
expiredDomains = "../saved_data/expired.txt"
domainMap = {}
domains = []
recipient = None
with open("../config.json") as config:
    conf = json.load(config)
    recipient = conf['recipient']
    domains = [x.strip() for x in conf['domains']]
messenger = sms.SMS(recipient)

def stringToDateTime(string):
    return datetime.strptime(string, "%Y-%m-%d %H:%M:%S")

def hasDomainBeenRenewed(prevDate, newDate):
    if prevDate == "None" or newDate is None:
        return False
    if stringToDateTime(newDate) > stringToDateTime(prevDate):
        return True
    else:
        return False

def hasDomainExpired(domainDate):
    if domainDate == "None":
        return True
    tempDate = stringToDateTime(domainDate)
    if(datetime.now() > tempDate):
        return True
    else:
        return False

def isFileEmpty(fp):
    isEmpty = True
    try:
        if(os.path.getsize(fp) > 0):
            isEmpty = False
    except OSError:
        return isEmpty
    return isEmpty        

def updateFile(fp):
    fp.seek(0)
    fp.truncate()
    json.dump(domainMap, fp, indent=4)

def printSeparator():
    count = 40
    for x in range(0,count):
        print('-', end='')
        sys.stdout.flush()
        time.sleep(0.01)
    print('')

#map listed domains to their expiration dates
def updateDomainMap():
    for domain in domains:
            if domain == '':
                continue
            print("Grabbing details for " + consoleColors.OKBLUE + domain + consoleColors.ENDC)
            
            #handle exceptions if domain has been deleted from the nameservers
            try:
                result = whois.whois(domain)
                exp = result.expiration_date
            except PywhoisError as e:
                exp = None
            
            if isinstance(exp,list) or isinstance(exp, tuple):
                domainMap[domain] = exp[0].__str__()
            else:
                domainMap[domain] = exp.__str__()

#read saved data
savedDataJson = None
jsonExists = False
if(os.path.exists(savedData)):
    with open(savedData) as dataFile:
        savedDataJson = json.load(dataFile)
        jsonExists = True

updateDomainMap()

#handle to the save file we will constantly make operations on
filePointer = open(savedData, "a+")
expiredPointer = open(expiredDomains, "a+")

while(True):

    printSeparator()

    #if the save data doesnt exist, create one
    if not jsonExists and len(domainMap) >= 1:
        filePointer.seek(0)
        filePointer.truncate()
        json.dump(domainMap, filePointer, indent=4)
        filePointer.flush()
        jsonExists = True
        print("New save data, saved at " + savedData)
        continue

    #if it does exist check if the domain list has any new domains
    if jsonExists:
        filePointer.seek(0)
        tempJson = json.load(filePointer)
        domainList = []
        for domain in tempJson:
            if domain == '':
                continue
            domainList.append(domain)    

        for domain in domains:
            if domain == '':
                continue
            if domain not in domainList:
                updateFile(filePointer)
                print("New domain detected, overwriting save...")
                break        

    #keep checking the expiry date
    filePointer.seek(0)
    storedDomains = json.load(filePointer)
    
    for domain in storedDomains:
        if(domain in domainMap):
            hasRenewed = hasDomainBeenRenewed(storedDomains[domain], domainMap[domain])
            hasExpired = hasDomainExpired(domainMap[domain])
            if(hasRenewed):
                textBody = domain + " has been renewed"
                print(consoleColors.WARNING + textBody + consoleColors.ENDC)
                #ovewrite the file and update with new date
                updateFile(filePointer)
                print("Save data has been updated")

                #send a notification
                print(consoleColors.OKGREEN + "\nSending notification\n" + consoleColors.ENDC)
                messenger.sendSms(textBody)

            if(hasExpired):
                expiredPointer.seek(0)
                tempDomainList = [x.strip() for x in expiredPointer.readlines()]
                if(domain not in tempDomainList):
                    textBody = domain + " HAS EXPIRED"
                    printSeparator()
                    print(consoleColors.WARNING + domain + " HAS EXPIRED, GO GRAB IT OR BACKORDER IT" 
                    + consoleColors.ENDC)
                    printSeparator()
                    #now add domain to expired list
                    print("Writing " + domain + " to expired list at " + expiredDomains)
                    expiredPointer.write(domain + "\n")
                    expiredPointer.flush()

                    #send an sms notification
                    print(consoleColors.OKGREEN + "\nSending notification\n" + consoleColors.ENDC)
                    messenger.sendSms(textBody)
                    
            else:
                print(domain + consoleColors.OKBLUE + " no renewal present" + consoleColors.ENDC)

    updateDomainMap()        
    time.sleep(5)        

#finally close the handles
filePointer.close()
expiredDomains.close()
