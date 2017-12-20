# -*- coding: UTF-8 -*-
import os
import smtplib 
 
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText

from email.utils import COMMASPACE,formatdate
from email import encoders
 
     
#server['name'], server['user'], server['passwd']，server['port']
def send_mail(server, fro, to, subject, text, files=[]): 
    assert type(server) == dict 
    assert type(to) == list 
    assert type(files) == list 
 
    msg = MIMEMultipart() 
    msg['From'] = fro 
    msg['Subject'] = subject 
    msg['To'] = COMMASPACE.join(to) #COMMASPACE==', ' 
    msg['Date'] = formatdate(localtime=True) 
    msg.attach(MIMEText(text,"html" ,"utf-8"))  
 
    for file in files: 
        part = MIMEBase('application', 'octet-stream') #'octet-stream': binary data 
        part.set_payload(open(file, 'rb'.read())) 
        encoders.encode_base64(part) 
        part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(file)) 
        msg.attach(part) 
 

    smtp = smtplib.SMTP(server['name'], server.get("port",  25)) 
    smtp.login(server['user'], server['passwd']) 
    smtp.sendmail(fro, to, msg.as_string()) 
    smtp.close()
    
    
    
if __name__ == "__main__":
    
    server = {"name":"smtp.exmail.qq.com", "user": "cqz@safedragon.com.cn", "passwd":"chenqizheng"}
    to = "cqz@safedragon.com.cn"
    subject="Hello Test Mail"
    text = "Test..."
    send_mail(server, server["user"], to, subject, text)
    
    