
import numpy as np
import matplotlib.pyplot as plt
import time
import schedule
import sys
from pysnmp.hlapi import * 
from pysnmp.entity.rfc3413.oneliner import cmdgen
import csv
import smtplib 
import datetime 
from email.mime.text import MIMEText 
from email.mime.multipart import MIMEMultipart 
from email.mime.base import MIMEBase 
from email import encoders
import matplotlib.pyplot as plt;plt.rcdefaults() 
import os 

counter = 0 
logfile = 'log' 

def plotline():

    try: 
        os.remove('server1graph.png')
    except Notex : 
        print(Notex," server1graph.png does not exist ")

    Ram, cpu , Disk = np.loadtxt('server1output.csv'
                      , delimiter=','
                      , unpack=True
                      )


    with plt.style.context('ggplot'):
        x = np.arange(1,(int(np.size(cpu))+1))
        plt.plot(x,cpu, label='cpu usage')
        plt.plot(x,Ram, label='ram usage')
        plt.plot(x,Disk, label='Disk usage')
        plt.legend()
        plt.xlabel('Time (in min)')
        plt.ylabel('Percantage(out of 100)')
        plt.savefig("server1graph.png", bbox_inches='tight')
        plt.close()
        plt.clf()   
        
	


def listcsv(): 
    
    data = np.loadtxt('server1output.csv'
                        , delimiter=','
                        , unpack= False
                        )
    data = np.delete(data, (0), axis=0)
    np.savetxt('server1output.csv', data ,delimiter=',', fmt='%.1f')


def csvwriter(datarow, name1): 
    with open(name1+'.csv', 'a') as x:
        a = csv.writer(x)
        a.writerow(datarow)

def plot1 (Ram, cpu, Disk):

    objects = ('RAM','CPU','Disk')
    y_pos = np.arange(len(objects))
    t = [Ram, cpu, Disk]
    plt.clf()
    plt.bar(y_pos, t, align='center', alpha=0.5)
    plt.xticks(y_pos, objects)
    plt.ylabel('Usage')
    plt.savefig("server11graph.png")
    plt.show()


	
def ramcalc(ram1,ram2):
    x = int(ram1) / 100
    percentage = int(ram2)/x
    return percentage

def tempwrite(Ram,cpu, Disk):

    line = '{0:.2f}'.format(cpu), '{0:.2f}'.format(Ram), '{0:.2f}'.format(Disk)

    csvwriter(line, 'server1output')

def sendMail():
    plotline()
    mail('scheduled email ', 'this is a scheduled email')
    print("scheduled email sent.......")


def automail():
    plotline()
    mail('auto email', 'this is an auto email')
    print("auto email sent.........")
	
def mail(subject, body):
    
    email_user = 'alyasrdatabase@gmail.com'
    email_password = '36719071'
    email_send = '7mood.94@gmail.com'
    
    msg = MIMEMultipart()
    msg['From'] = email_user
    msg['To'] = email_send
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

   
    filename = 'server1graph.png'
    attachment = open(filename, 'rb')

    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= " + filename)

    
    filename2 = 'log.csv'
    attachment2 = open(filename2, 'rb')

    part2 = MIMEBase('application', 'octet-stream')
    part2.set_payload((attachment2).read())
    encoders.encode_base64(part2)
    part2.add_header('Content-Disposition', "attachment; filename= " + filename2)

    
    filename3 = 'server11graph.png'
    attachment3 = open(filename3, 'rb')

    part3 = MIMEBase('application', 'octet-stream')
    part3.set_payload((attachment3).read())
    encoders.encode_base64(part3)
    part3.add_header('Content-Disposition', "attachment; filename= " + filename3)

    
    msg.attach(part)
    msg.attach(part2)
    msg.attach(part3)
    text = msg.as_string()
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email_user, email_password)

    server.sendmail(email_user, email_send, text)
    server.quit()
	
def snmpscan():
    global counter 
    global logfile 
    errorIndication, errorStatus, errorIndex, varBinds = next(
        getCmd(SnmpEngine(),
               UsmUserData('privUser', 'AuthPassword', 'CryptoPassword'
),
               UdpTransportTarget(('172.16.1.80', 161)),
               ContextData(),
               
               ObjectType(ObjectIdentity('1.3.6.1.4.1.2021.4.5.0')),
               
               ObjectType(ObjectIdentity('1.3.6.1.4.1.2021.4.6.0')),
               
               ObjectType(ObjectIdentity('1.3.6.1.4.1.2021.11.9.0')),
               
               ObjectType(ObjectIdentity('1.3.6.1.4.1.2021.10.1.3.3')),
               
               ObjectType(ObjectIdentity('1.3.6.1.4.1.2021.9.1.9.1')),
               
               ObjectType(ObjectIdentity('1.3.6.1.2.1.25.4.2.1')),
               
               
               ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysDescr', 0)))
    )
    if errorIndication:
        print(errorIndication)
    else:
        if errorStatus:
            print('%s at %s' % (
                errorStatus.prettyPrint(),
                errorIndex and varBinds[int(errorIndex) - 1] or '?'
            )
				  )
        else:

            valueslist = []
            for name, val in varBinds:
                
                valueslist.append(str(val))

            Ram = ramcalc(valueslist[0],valueslist[1])
            cpu = int(valueslist[2])
            Disk = int(valueslist[4])
            csvwriter(valueslist, logfile)
            plot1(Ram, cpu, Disk)
            if int(counter) < 10:
                
                tempwrite(cpu, Ram, Disk)

                counter += 1 

            elif int(counter) >= 10:
                listcsv()
                tempwrite(cpu, Ram, Disk)

            if int(Ram) > 70 or int(cpu) > 70 or int(Disk) > 70:
    

                automail()
                
                    
            time.sleep(10) 
            
	
	
	
if __name__ == '__main__':

    try:
        os.remove('server1output.csv')

    except Exception :
        print(Exception,'error file not found')

    names = 'Total Ram', 'Ram', 'CPU', 'CPU 15 min', 'Disk space', 'Running Procces', 'System information' 
    csvwriter(names,logfile)
    schedule.every().day.at("22:00").do(sendMail)
    

    while True:
        print ("running......")
        schedule.run_pending()
        snmpscan()


