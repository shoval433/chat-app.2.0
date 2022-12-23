from flask import Flask,render_template, request 
from datetime import datetime 
import mysql.connector
import socket
chatDB = mysql.connector.connect(
  host='my_data',
  user="root",
  password="root",
  database="chatDB",
  auth_plugin="mysql_native_password"
)
mycursor = chatDB.cursor()
mycursorBu = chatDB.cursor(buffered=True)

app = Flask(__name__)

#general chat
@app.route('/')
def get_no_room():
    return render_template("index.html")

@app.route('/<room>')
def get_room(room):
    return render_template("index.html")

@app.route("/chat/<room>")
def have_room(room):
    try:
        mycursorBu.execute("select * from log_%s;" %room)
        chatDB.commit()
    except:
         
        mycursor.execute('create table log_' + room + ' (id int NOT NULL AUTO_INCREMENT key, username VARCHAR(255), msg VARCHAR(255));')
        chatDB.commit()
    return render_template('index.html',host=socket.gethostname())


#The GET and POST of the chat 
@app.route("/api/chat/<room>",methods=['POST', 'GET'])
def chat(room):
    if request.method == 'GET':
        mycursor.execute("select msg from log_"+room+" ")
        chatDB.commit()
        # Format the output nicly
        chatContent = ""
        for line in mycursor.fetchall():
            chatContent += line[0]
        
        return chatContent

    elif request.method == 'POST':
        timeData=datetime.now().strftime("%H:%M:%S")
        user=request.form['username']
        usr_massge = "["+timeData +"] "+request.form['username']+':'+request.form['msg'] +'\n'
        sql = "INSERT INTO log_"+ room +" (username, msg) VALUES (%s, %s)"
        val = (user, usr_massge)
        mycursorBu.execute(sql,val)

        chatDB.commit()
        # f.write(usr_massge)
        return "200"

if __name__=="__main__":
    app.run(host="0.0.0.0",debug=True)