from time import sleep
from json import dumps
from kafka import KafkaProducer
from kafka import KafkaConsumer
from pymongo import MongoClient
from json import loads
from flask import Flask, request, jsonify, make_response
from bson.objectid import ObjectId
import pymongo

consumer = KafkaConsumer(
    'test',
     bootstrap_servers=['localhost:9092'],
     auto_offset_reset='earliest',
     enable_auto_commit=True,
     group_id='my-group',
     value_deserializer=lambda x: loads(x.decode('utf-8')))

client = MongoClient("mongodb://127.0.0.1:27017")
db = client.mymongodb
todos = db.testconsumer



for message in consumer:
    count_view = todos.find_one({"_id": ObjectId("5fec3488d91f1160d9a452f8")})
    count_view_prop = count_view["views"]
    count_view_prop += 1
    todos.update_one({"_id": ObjectId("5fec3488d91f1160d9a452f8")}, {'$set': {"views": count_view_prop}})
    # message value and key are raw bytes -- decode if necessary!
    # e.g., for unicode: `message.value.decode('utf-8')`
    print ("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,
                                          message.offset, message.key,
                                          message.value))



