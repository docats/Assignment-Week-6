import mysql.connector #匯入資料庫模組
from distutils.log import debug
from os import name
from flask import Flask # 載入Flask 
from flask import request # 載入Request物件(要取得POST參數值)
from flask import redirect # 載入redirect函式
from flask import render_template # 使用樣板引擎
from flask import session # 使用session

#嘗試連接到資料庫
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root123",
    database="mydatabase"
)

print("資料庫訊息:",mydb)

# 建立 Application物件，可以設定靜態檔案的路徑處理
# 所有在 static 資料夾底下的檔案，都對應到網址路徑 /static/ 檔案名稱
app=Flask(
    __name__,
    static_folder="static", # 靜態檔案的資料夾名稱
    static_url_path="/static" #靜態檔案對應的網址路徑
    ) 


# 使用 Session密鑰
app.secret_key = "any string but secret" 


# 建立路徑 / 對應的處理函式
@app.route('/')
def index(): #用來回應路徑 / 的處理函式
    
    return render_template('index.html') # 回傳網站首頁內容

#建立路徑 /signin對應的處理函式
@app.route("/signin",methods=['POST'])
def signin():
    username = request.form['uname']
    password = request.form['psw']
    if username=="" or password=="":
        return redirect('/empty/?message=帳號或密碼不能為空')
    got=mydb.cursor().execute("SELECT username FROM member WHERE username=%s",(username,))
    result=mydb.cursor().fetchone()
    mydb.commit()
    if got == 0:
        return redirect("error/?message=帳號或密碼錯誤")
    elif got == 1:
        if password == result['password']:
            session['username']=[username,result['nickName']]
            return redirect("/member")
        else:
            return redirect("error/?message=帳號或密碼錯誤")
    else:
        return redirect("error/?message=全部都錯")
    

#建立路徑 /signup對應的處理函式，獲取註冊請求及處理
@app.route("/signup",methods=['POST'])
def signup():
    name = request.form['nickname'] #取得表格輸入的姓名
    username = request.form['new_ac'] #取得表格輸入的新帳號
    password = request.form['new_psw'] #取得表格輸入的新密碼
    cur = mydb.cursor()
    got=cur.execute("SELECT username FROM member where username=%s",(username,))
    mydb.commit()
    # result = cur.fetchall()
    if got!=0:
       return redirect("/error/?message=註冊失敗，該用戶已被註冊")    
    else:
            result = cur.execute("INSERT INTO member (name,username,password) VALUES (%s,%s,%s)",
                (name,username,password))
            mydb.commit()
            print("新增",result,"筆，恭喜記錄成功")
            return redirect("/")
   

# 建立路徑 /member對應的處理函式
@app.route("/member/",methods=['GET'])
def member():
    if session.get("username"):
        # username=request.args.get("username","大豆貓")
        # username=session["username"] #session把資料放到username，取得名字
        return  render_template('member.html',username=session['username'][1]+"恭喜您，成功登入系統")
    else:
        return redirect("/signout")


# 建立路徑 /error對應的處理函式
@app.route("/error/",methods=['GET'])
def error():
    message=request.args.get("message")
    return render_template('error.html',message=message)

# 建立路徑 /empty對應的處理函式
@app.route("/empty/",methods=['GET'])
def empty():
    message=request.args.get("message")
    return render_template('empty.html',message=message)

#建立路徑 /signout對應的處理函式
@app.route("/signout",methods=['GET'])
def signout():
     session.pop("username"," ") #登出使用pop()方法把session紀錄刪除
     return redirect("/")

# (啟動網站伺服器)host,port,debug等參數，要在這邊設定
app.run(port=3000,debug='true') 
