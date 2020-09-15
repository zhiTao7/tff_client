# -*- coding: utf-8 -*-
import os
import sys


base_dir = os.path.dirname(os.path.abspath(__file__))


class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY") or "123456"
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BASE_DATASET_DIR = os.path.join(os.environ['HOME'], "federated_learning", "testdata")
    
    CPUT = 2      #计算CPU利用率的时间间隔
    NETT = 2      #计算网卡流量的时间间隔"""
    #LOOPT = 2     """#脚本循环时间间隔"""


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL',
                                             "mysql+pymysql://root:111@10.0.0.200:3306/flask_db?charset=UTF8MB4")


config = {
 'development': DevelopmentConfig,
 'default': DevelopmentConfig
}
