from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient

db = client.dbsparta

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/bucket", methods=["POST"])
def bucket_post():
    bucket_receive = request.form["bucket_give"]

    # count = db.bucket.find({}, {'_id': False}).count()
    # num = count + 1
    count = list(db.bucket.find({}, {'_id': False}))
    num = len(count) + 1

    doc = {
        'num': num,
        'bucket': bucket_receive,
        'done': 0
    }

    db.bucket.insert_one(doc)
    return jsonify({'msg': '등록 완료!'})


@app.route("/bucket/done", methods=["POST"])
def bucket_done():
    num_receive = request.form["num_give"]
    done_receive = request.form["done_give"]
    db.bucket.update_one({'num': int(num_receive)}, {'$set': {'done': done_receive}})
    return jsonify({'msg': '수정 완료!'})

@app.route("/bucket", methods=["GET"])
def bucket_get():
    buckets_list = list(db.bucket.find({}, {'_id': False}))
    return jsonify({'buckets': buckets_list})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)