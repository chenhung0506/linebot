import log as logpy
import sys
import traceback
import service
import const
import os
import smtplib, ssl
import pymysql
import dao
import utils
import json
from threading import Timer,Thread,Event
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.combining import OrTrigger
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.header import Header

log = logpy.logging.getLogger(__name__)

def insertTest():
    try:
        conn = pymysql.Connect(host='us-cdbr-east-02.cleardb.com',user='bdef9ef0984947',passwd='0b65d70f',db='heroku_d38736f240fb4e6',charset='utf8')
        dao.Database(conn).insertConversation( 'test2', '["test1","test2","test3","test4"]' )
    except Exception as e:
        log.info("insertConversation occured some error: "+utils.except_raise(e))
    finally:
        conn.close()

def queryTest():
    data=[]
    try:
        conn = pymysql.Connect(host='us-cdbr-east-02.cleardb.com',user='bdef9ef0984947',passwd='0b65d70f',db='heroku_d38736f240fb4e6',charset='utf8')
        data = dao.Database(conn).queryConversation( 'test2' )
        log.info(len(data))
        log.info(json.loads(data[0][1])[0])
            # print "%s, %s" % (row["USER_ID"], row["CONVERSATION"])
            # log.info (row["USER_ID"] + row["CONVERSATION"])
    except Exception as e:
        log.info("queryConversation occured some error: "+utils.except_raise(e))
    finally:
        conn.close()
    log.info(len(data))