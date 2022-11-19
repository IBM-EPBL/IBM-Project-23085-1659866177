from flask import Flask, render_template,request,flash,redirect,url_for
import datetime
import ibm_db

from newsapi import NewsApiClient
newsapi = NewsApiClient(api_key='73cedc4b8d504ef7a2a6bbbe4456dd1b')


con = ibm_db.connect("DATABASE=bludb;HOSTNAME=55fbc997-9266-4331-afd3-888b05e734c0.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;PORT=31929;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=qlk23202;PWD=VRhFlQo0AHQQwX6f",'','')

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('signinUp.html')
    

@app.route('/dash')
def dash():
    topheadlines=newsapi.get_top_headlines(sources='bbc-news,the-verge,google-news')
    # from_param="2022-11-08",to="2022-11-09",page=2,
    articles=topheadlines['articles']   
    desc=[]
    news=[]
    img=[]
    timing=[]
    more=[]
    auth=[]
    for i in range(len(articles)):
        myarticles=articles[i]

        news.append(myarticles['title'])
        desc.append(myarticles['description'])
        img.append(myarticles['urlToImage'])
        x=myarticles['publishedAt']
        timing.append(x[0:10]+" @ "+x[11:16])
        more.append(myarticles['url'])
        au=myarticles['author']
        if au==None or au[0:3]=="htt": 
            au="Media News"
        auth.append(au)

    myList=zip(desc,news,img,timing,more,auth)  


    topsources=newsapi.get_sources(language="en")
    articles=topsources['sources']
    desc=[]#category
    name=[]
    url=[]
    id=[]
    # timing=[]
    coun=[]
    for i in range(len(articles)):
        myarticles=articles[i]
        id.append(myarticles['id'])
        name.append(myarticles['name'][0:19])
        desc.append(myarticles['category'].capitalize())
        url.append(myarticles['url'])
        coun.append(myarticles['country'].upper())

    mySources=zip(id,name,desc,url,coun)  


    return render_template('dashboard.html',context=myList,channels=mySources)

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
