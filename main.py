import pymongo
from bson.objectid import ObjectId
from flask import Flask, render_template, redirect, url_for, jsonify, abort
from flask import Flask, request, jsonify, make_response
from flask import Flask
from pymongo import MongoClient
from flask_pymongo import PyMongo
import json
from multiprocessing import Value


from json import dumps
from kafka import KafkaProducer
from kafka import KafkaConsumer
from json import loads

counter = Value('i', 0)

producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                             value_serializer=lambda x:
                             dumps(x).encode('utf-8'))

app = Flask(__name__)

app.config['SECRET_KEY']='LongAndRandomSecretKey'
client = MongoClient("mongodb://127.0.0.1:27017")
db = client.mymongodb
todos = db.todo

@app.route('/')
def home():
    page = request.args.get('page', 1 ,int)
    posts = [1,2,3,4,5,6,7,8]
    sorts_list = ['desc', 'asc']
    item_list = todos.find().sort("_id",pymongo.DESCENDING).limit(4)

    with counter.get_lock():
        counter.value += 1
        out = counter.value

    producer.send('test', 'callme')

    return render_template("base.html", item_list = item_list,
                           posts = posts, sorts_list = sorts_list, out = out)

@app.route("/add", methods = ['POST'])
def add():
    item_name = request.values.get("itemName")
    item_desc = request.values.get("itemDescribe")
    todos.insert({"item_name": item_name, "item_desc": item_desc})
    return redirect('/')

@app.route("/delete")
def delete():
    key = request.values.get("_id")
    todos.remove({"_id": ObjectId(key)})
    return redirect(url_for("home"))

@app.route("/update")
def updateRoute():
    id = request.values.get("_id")
    item_list = todos.find({"_id": ObjectId(id)})
    return render_template('update.html', item_list=item_list)


@app.route("/action_update",methods=['post'])
def update():
    item_name = request.values.get("item_name")
    item_desc = request.values.get("item_desc")
    id = request.values.get("_id")
    todos.update({"_id": ObjectId(id)}, {'$set': {"item_name": item_name, "item_desc": item_desc}})
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
