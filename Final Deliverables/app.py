from flask import Flask, render_template,request,flash,redirect,url_for
import datetime
import ibm_db

from newsapi import NewsApiClient
newsapi = NewsApiClient(api_key='73cedc4b8d504ef7a2a6bbbe4456dd1b')
con = ibm_db.connect("DATABASE=bludb;HOSTNAME=55fbc997-9266-4331-afd3-888b05e734c0.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;PORT=31929;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=qlk23202;PWD=VRhFlQo0AHQQwX6f",'','')
# print(con)
# print("connection successful...")

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('signinUp.html')

@app.route('/coun')
def coun():
    return render_template("country_list.html")
@app.route('/dat')
def dat():
    return render_template("date_list.html")
@app.route('/cat')
def cat():
    return render_template("cat_list.html")

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

@app.route('/channel/<string:ida>')
def channel(ida):
    topheadlines=newsapi.get_top_headlines(sources=ida)
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

    channel_name=ida
    topsources=newsapi.get_sources(language="en")
    articles=topsources['sources']
    desc=[]#category
    name=[]
    url=[]
    channel=[]
    # timing=[]
    coun=[]
    for i in range(len(articles)):
        myarticles=articles[i]
        x=myarticles['id']
        if ida==x:
            channel_name=myarticles['name']
        channel.append(x)
        name.append(myarticles['name'])
        desc.append(myarticles['category'].capitalize())
        url.append(myarticles['url'])
        coun.append(myarticles['country'].upper())

    mySources=zip(name,desc,url,coun,channel)  


    return render_template('dash_channel.html',context=myList,channels=mySources,id=channel_name)


@app.route('/country',methods=["POST","GET"])
def country():
      if request.method=='POST':
        try:            
            id=request.form['country']
            # id="in"
            # print("country: "+id)

    
            topheadlines=newsapi.get_top_headlines(country=id.lower(),page=2)
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

            topsources=newsapi.get_sources(country=id.lower())
            articles=topsources['sources']
            desc=[]#category
            name=[]
            url=[]
            chan=[]
            # timing=[]
            coun=[]
            for i in range(len(articles)):
                myarticles=articles[i]
                chan.append(myarticles['id'])
                name.append(myarticles['name'])
                desc.append(myarticles['category'].capitalize())
                url.append(myarticles['url'])
                coun.append(myarticles['country'].upper())

            mySources=zip(name,desc,url,coun,chan)  

            return render_template('dash_country.html',context=myList,channels=mySources,id=id.upper())
        except Exception as e:
             print("Exception : "+str(e))

@app.route('/category',methods=["POST","GET"])
def category():
      if request.method=='POST':
        try:            
            ida=request.form['category']
            idb=request.form['language']
            # id="in"
            # print("category: "+ida+"  "+ "language: "+idb)
    
            topheadlines=newsapi.get_top_headlines(category=ida,language=idb)
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

            topsources=newsapi.get_sources(category=ida.lower(),language=idb)
            articles=topsources['sources']
            desc=[]#category
            name=[]
            url=[]
            chan=[]
            # timing=[]
            coun=[]
            for i in range(len(articles)):
                myarticles=articles[i]
                chan.append(myarticles['id'])
                name.append(myarticles['name'])
                desc.append(myarticles['category'].capitalize())
                url.append(myarticles['url'])
                coun.append(myarticles['country'].upper())

            mySources=zip(name,desc,url,coun,chan)  

            return render_template('dash_category.html',context=myList,channels=mySources,ida=ida.upper(),idb=idb.upper())
        except Exception as e:
             print("Exception : "+str(e))



@app.route('/date',methods=["POST","GET"])
def date():
      if request.method=='POST':
        try:            
            from_dat=request.form['from']
            to=request.form['to']
            lan=request.form['language']

            # id="in"
            # print("Date: "+from_dat+" : "+to)

    
            topheadlines=newsapi.get_everything(from_param=from_dat,to=to,page=2,language=lan,sources='bbc-news,the-verge',)
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
            # print("Above source")

            topsources=newsapi.get_sources(language=lan)
            articles=topsources['sources']
            desc=[]#category
            name=[]
            url=[]
            chan=[]
            # timing=[]
            coun=[]
            for i in range(len(articles)):
                myarticles=articles[i]
                chan.append(myarticles['id'])
                name.append(myarticles['name'])
                desc.append(myarticles['category'].capitalize())
                url.append(myarticles['url'])
                coun.append(myarticles['country'].upper())

            mySources=zip(name,desc,url,coun,chan)  

            return render_template('dash_date.html',context=myList,channels=mySources,ida=from_dat,idb=to,lan=lan.upper())
        except Exception as e:
             print("Exception : "+str(e))




@app.route('/search',methods=["POST","GET"])
def search():
    
    if request.method=='POST':
        try:
            # time=datetime.datetime.now()
            # print("time: "+time)
            topheadlines=newsapi.get_top_headlines(sources='bbc-news,the-verge,google-news')
            articles=topheadlines['articles']
            desc=[]
            news=[]
            img=[]
            timing=[]
            more=[]
            auth=[]
            ser=request.form['search']
            # print(ser)
            for i in range(len(articles)):
                myarticles=articles[i]

                chck=myarticles['title']
                chck_b=myarticles['description']
                # print(ser+chck)
                if ser.lower() in chck.lower() or ser.lower() in chck_b.lower():
                    # print("check\n")
                    news.append(chck)
                    desc.append(chck_b)
                    # print(ser)
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
            # timing=[]
            coun=[]
            id=[]
            for i in range(len(articles)):
                myarticles=articles[i]
                id.append(myarticles['id'])
                name.append(myarticles['name'])
                desc.append(myarticles['category'].capitalize())
                url.append(myarticles['url'])
                coun.append(myarticles['country'].upper())

            mySources=zip(id,name,desc,url,coun)  

            return render_template('dashboard.html',context=myList,channels=mySources)

        except Exception as e:
             print("Exception : "+str(e))

    

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
