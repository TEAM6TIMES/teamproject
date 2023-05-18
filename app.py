from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
import certifi

ca = certifi.where()
client = MongoClient(
    'mongodb+srv://sparta:test@cluster0.0qxqx9k.mongodb.net/?retryWrites=true&w=majority', tlsCAFile=ca)
db = client.dbsparta

@app.route('/')
def home():
   return render_template('index.html')

@app.route("/guestbook", methods=["POST"])
def guestbook_post():
    name_receive = request.form['name_give']
    comment_receive = request.form['comment_give']
    currentDate_receive = request.form['currentDate_give']
    currentTime_receive = request.form['currentTime_give']
    password_receive = request.form['password_give']

    doc = {
        'name': name_receive,
        'comment': comment_receive,
        'currentDate': currentDate_receive,
        'currentTime': currentTime_receive,
        'password': password_receive
    }

    db.project.insert_one(doc)
    
    return jsonify({'msg': '기록 완료!'})

@app.route("/guestbook", methods=["GET"])
def guestbook_get():
    all_comments = list(db.project.find({},{'_id':False}))
    return jsonify({'result': all_comments})

@app.route('/guestbook', methods=['DELETE'])
def guestbook_delete():
    comment_receive = request.form['comment_give']
    db.project.delete_one({'comment': comment_receive})
    return jsonify({'msg': '삭제 완료!'})



if __name__ == '__main__':
   app.run('0.0.0.0', port=5000, debug=True)