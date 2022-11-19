from flask import Flask, render_template,request,flash,redirect,url_for
import datetime
import ibm_db


con = ibm_db.connect("DATABASE=bludb;HOSTNAME=55fbc997-9266-4331-afd3-888b05e734c0.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;PORT=31929;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=qlk23202;PWD=VRhFlQo0AHQQwX6f",'','')

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('signinUp.html')
    

@app.route("/addData",methods=["POST","GET"])
def addData():
    if request.method=='POST':
        try:
            name=request.form['name']
            mail=request.form['mmail']
            country=request.form['country']
            password=request.form['password']

            insert_sql="INSERT INTO customers values(?,?,?,?)"
            prep_stmt=ibm_db.prepare(con,insert_sql)
            ibm_db.bind_param(prep_stmt,1,name)
            ibm_db.bind_param(prep_stmt,2,mail)
            ibm_db.bind_param(prep_stmt,3,country)
            ibm_db.bind_param(prep_stmt,4,password)
            ibm_db.execute(prep_stmt)
            return render_template("hello.html")
        except Exception as e:
             print("Exception : "+str(e))
        finally:
            return render_template("hello.html")

@app.route("/login",methods=["POST","GET"])
def login():  
    if request.method=='POST':
        try:
            password=request.form['password']
            mail=request.form['mmail']
            sql = "SELECT * FROM customers"
            stmt = ibm_db.exec_immediate(con, sql)
            tuple = ibm_db.fetch_tuple(stmt)
            while tuple != False:
                if mail==tuple[1]:
                    checkpassw=tuple[3]
                    break
                tuple = ibm_db.fetch_tuple(stmt)

            if password==checkpassw:
                return redirect(url_for("dash"))
            else:
                # print("Wrong pwd")
                return render_template("hello_copy.html")
        except Exception as e:
             print("Exception : "+str(e))


if __name__ == '__main__':
    app.run(debug=True)
