# coding=UTF-8
import requests
import json
import time
import re
import ast
import logging
import os
import math
import time
import ctypes 
import threading
import dao
import const
import log as logpy
import pymysql
import service
import utils
import service_line
from datetime import datetime, timedelta
from flask import Flask, Response, render_template, request, redirect, jsonify, abort
from threading import Timer,Thread,Event
from flask_restful import Resource
from datetime import datetime
from linebot import  LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

log = logpy.logging.getLogger(__name__)

def setup_route(api):
    api.add_resource(Default, '/')
    api.add_resource(HealthCheck, '/healthCheck')
    api.add_resource(BatchStart, '/batchStart')
    api.add_resource(BatchStop, '/batchStop')
    api.add_resource(Transmit, '/transmit')
    api.add_resource(Weather, '/weather')
    api.add_resource(Forecast, '/forecast')
    api.add_resource(SendMail, '/sendmail')

#localhost:8331/sendmail?receiver=chenhung0506@gmail.com&subject=這是標題&msg=這是內容

class SendMail(Resource):
    def post(self):
        args = request.get_json()
        return self.process(args)
    def get(self):
        args = request.args
        return self.process(args)
    def process(self,args):
        log.info(args)
        status, result, message = utils.sendEmail(args.get('receiver'),args.get('subject'),args.get('msg'))
        return {
            'status': status,
            'result': result,
            'message': message
        }, status

class Default(Resource):
    def get(self):
        return {
            'status': 200,
            'message': 'health',
            'result': {}
        }, 200

class Weather(Resource):
    def get(self):
        log.info('GetWeather api start')
        lineService = service_line.lineService()
        return {
            'status': 200,
            'message': 'success',
            'result': lineService.getWeather('65')
        }, 200

class Forecast(Resource):
    def get(self):
        log.info('GetWeather api start')
        lineService = service_line.lineService()
        return {
            'status': 200,
            'message': 'success',
            'result': lineService.getForecast('65')
        }, 200


class HealthCheck(Resource):
    log.debug('check health')
    def get(self):
        return {
            'status': 0,
            'message': 'success',
            'method': request.method,
            'username': request.form.get('username'),
            'PHONE_NUMBER': const.PHONE_NUMBER
        }, 200

class BatchStop(Resource):
    def get(self):
        log.info('BatchStop api start')
        return {
            'status': 200,
            'message': utils.stop_batch()
        }, 200

class BatchStart(Resource):
    def get(self):        
        log.info('stop batch:' + utils.stop_batch())
        log.info('BatchStart api start')
        time.sleep(int(5))
        utils.prepare_batch_blocking(transmitProcess,None)
        # utils.prepare_batch_blocking(batchTest,'*/1 * * * *',None)
        
        # sched = BlockingScheduler()
        # sched.add_job(cronTest, CronTrigger.from_crontab(const.TRANSMIT_CRON))
        # sched.start()
        return {
            'message': 'success'
        }, 200

def batchTest():
    log.info(datetime.today().strftime('%Y-%m-%d'))



class Transmit(Resource):
    def get(self):
        return {
            'status': 200,
            'message': transmitProcess(request)
        }, 200

def transmitProcess(request):
    try:
        callApi=service.CallApi()
        dataForRakutens = callApi.getTag(request)
        dataForRakutens = callApi.sortData(dataForRakutens)
        # return dataForRakutens
        log.info("dataForRakuten quantity:" + str(len(dataForRakutens['data'])))
        report=[]
        errorEmail=""
        for val in dataForRakutens['data']:
            dataForRakuten={}
            dataForRakuten['data']=[]
            dataForRakuten['data'].append(val)
            dataForRakuten['total_size']=1
            # return dataForRakuten
            callArmsResponse=callApi.transmitToArms(dataForRakuten)
            if callArmsResponse.status_code == 204 :
                log.info('Transmit success')
                report.append({"session_id":val["session_id"], "message":"success", "status": 200})
            else:
                log.info('Transmit fail, status: ' + str(callArmsResponse.status_code) + ', message: ' + callArmsResponse.text)
                resendUrl='http://' + const.SERVER_IP + ':' + const.PORT + '/transmit?call_direction=outbound&session_id=' + val["session_id"]
                errorEmail = errorEmail + 'transmit error, session id: ' + val["session_id"] + '&nbsp;&nbsp;&nbsp;&nbsp;<a href="' + resendUrl + '"> click here to resend </a><br>'
                report.append({"session_id":val["session_id"], "message":"fail", "status": 204 , "error_data" : dataForRakuten})
        
        
        if errorEmail != "":
            log.info('send error email')
            subject = datetime.strftime(datetime.now() - timedelta(1), '%Y-%m-%d') + "AICC transmit to Arms Alert Mail"
            utils.sendEmail(["chenhung0506@gmail.com", "chenhunglin@emotibot.com"], subject, errorEmail)

        log.info('process complete')

        return report

    except Exception as e:
        log.error("transmitProcess error: "+utils.except_raise(e))
        return utils.except_raise(e)

def transmitProcessTest(request):
    try:
        callApi=service.CallApi()
        callArmsResponse=callApi.transmitToArmsTest()
        if callArmsResponse.status_code == 204 :
            log.info('Transmit success')
            return 'success'
        else:
            log.info('Response status: ' + str(callArmsResponse.status_code) + ', message: ' + callArmsResponse.text)
            return 'fail'
        log.info('process complete')

    except Exception as e:
        log.error("transmitProcess error: "+utils.except_raise(e))

def testGetChatRecords():
    try:
        callApi=service.CallApi()
        # s_reponse=callApi.getChatRecords(request).text.encode('utf8')
        # log.info(s_reponse)
        return callApi.getChatRecords("1eb7c32c-9333-11ea-bbff-119443b68c06")
        
    except Exception as e:
        log.error("transmitProcess error: "+utils.except_raise(e))