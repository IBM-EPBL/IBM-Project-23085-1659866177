from flask import Flask, render_template,request,flash,redirect,url_for
import sqlite3 as sql

app = Flask(__name__)
app.secret_key="123"

con=sql.connect("database.db")
con.execute("CREATE TABLE IF NOT EXISTS data(pid INTEGER PRIMARY KEY ,name TEXT,address TEXT,contact INTEGER,mail TEXT)")
con.close()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/add_record')
def add_record():
    return render_template('add_record.html')

@app.route("/addData",methods=["POST","GET"])
def addData():
    if request.method=='POST':
        try:
            name=request.form['name']
            address=request.form['address']
            contact=request.form['contact']
            mail=request.form['mail']
            con=sql.connect("database.db")
            cur=con.cursor()
            cur.execute("INSERT INTO data(name,address,contact,mail)values(?,?,?,?)",(name,address,contact,mail))
            con.commit()
            flash("Record Added Successfully","success")
        except:
            flash("Error in Insert Operation","danger")
        finally:
            return redirect(url_for("home"))
            con.close()

@app.route('/view_record')
def view_record():
    con=sql.connect("database.db")
    con.row_factory=sql.Row
    cur=con.cursor()
    cur.execute("SELECT * FROM data")
    data=cur.fetchall()
    con.close()
    return render_template("view_record.html",data=data)

@app.route('/update_record/<string:id>',methods=["POST","GET"])
def update_record(id):
    con=sql.connect("database.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM data where pid=?",(id))
    data = cur.fetchone()
    con.close()

    if request.method=='POST':
        try:
            name=request.form['name']
            address=request.form['address']
            contact=request.form['contact']
            mail=request.form['mail']
            con = sql.connect("database.db")
            cur = con.cursor()
            cur.execute("UPDATE data SET name=?,address=?,contact=?,mail=? where pid=?",(name,address,contact,mail,id))
            con.commit()
            flash("Update Successfully","success")
        except:
            flash("Error in Update Operation","danger")
        finally:
            return redirect(url_for("home"))
            con.close()
    return render_template('update_record.html',data=data)

@app.route('/delete_record/<string:id>')
def delete_record(id):
    try:
        con = sql.connect("database.db")
        cur = con.cursor()
        cur.execute("DELETE FROM data where pid=?",(id))
        con.commit()    
        flash("Record Deleted Successfully","success")
    except:
        flash("Record Delete Failed","danger")
    finally:
        return redirect(url_for("home"))
        con.close()

if __name__ == '__main__':
    app.run(debug=True)
