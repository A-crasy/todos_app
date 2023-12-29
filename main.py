from flask import Flask, request, render_template, session, flash
from flask_session import  Session
import helper
app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
from datetime import date, datetime


@app.route("/")
def home() :
     return  render_template("index.html")

@app.route("/a" , methods=["POST","GET"])
def allusers() :
     datas = helper.fetch_data_from_graphql_api(helper.graphql_query)
     result =   datas["data"]["allUsers"]["edges"]

     if request.method == "POST" :
          all = request.form
          username = all.get("username")
          password = all.get("password")
          result = helper.user_checker(username,password,result)
          if result == False :
               flash('You need to log-in to do any search!')
               return  render_template("index.html")

          if username == result["username"] and password == result["password"] :
               allposts = helper.fetch_data_from_graphql_api(helper.graphql_query2)
               results= allposts["data"]["allPosts"]["edges"]
               session["username"] = username
               session["list1"] = results
               session["id"] = result["ids"]
               return  render_template("main_page.html",list1=results,users = session["id"],username = username)
     else :
          return "yess"

@app.route("/edits/<n>",methods=["POST","GET"])
def edits(n) :
     return "edits page"



@app.route("/addtodo",methods=["POST","GET"])
def add_todo():
     return  render_template("todo_add.html")



@app.route("/addtodos",methods=["POST","GET"])
def adds() :

     files = request.form
     allposts = helper.fetch_data_from_graphql_api(helper.graphql_query2)
     results = allposts["data"]["allPosts"]["edges"]
     id = len(results)+5
     ids = id
     title = files.get("title")
     content = files.get("content")
     dates = date.today()
     now = datetime.now()
     times = now.strftime("%H:%M:%S")
     username = session["username"]
     helper.addtodo(id,ids,title,content,dates,str(times),"Not Done",str(session["id"]))
     allposts = helper.fetch_data_from_graphql_api(helper.graphql_query2)
     results = allposts["data"]["allPosts"]["edges"]
     return render_template("main_page.html",list1=results,users = session["id"],username = username)

app.run(host="0.0.0.0",debug=True)