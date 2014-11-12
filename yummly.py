from flask import Flask,request,url_for,redirect,render_template
from pymongo import MongoClient
import time
import urllib2, json
import function

appid = "65fb5a0e"
appkey = "f8cbfed212e664b2f56f9e04a91c1bc9" 	

app=Flask(__name__)

mongo = MongoClient()
dbname = "cynmiclawyummly"
db = mongo[dbname]
recipedb = db['recipes']
searchdb = db['searches']

@app.route("/")
def index():
    return "Yummly"

@app.route("/t")
@app.route("/t/<tag>")
def t(tag="Cookies"):
    return function.findFoods(tag)

@app.route("/test")
def test():
    jsonname = "cookietest.json"
    jsonf = open(jsonname)
    content = jsonf.read()
    jsonf.close()
    load = json.loads(content)
    toprint = json.dumps(load, sort_keys=True, 
                         indent=4, separators=(',',':'))
    #load = json.loads(json.dumps(load["matches"][1]))
    toprint = json.dumps(load, sort_keys=True, 
                         indent=4, separators=(',',':'))
    #return str(load)
    return "<pre>"+toprint+"</pre>"
    
@app.route("/get")
def get():
    return function.calcFoods("Healthy-Morning-Muffins-Martha-Stewart")
    
@app.route("/search", methods=["GET","POST"])
def search():
    if request.method=="GET":
        return render_template("search.html")
    else:
        button = request.form["button"]
        if button=="search":
            keyword = request.form["keyword"].replace(" ","+")
            include = request.form["include"].replace(" ","+").split(",") #list of ingredients with spaces replaced by +, e.g. "large eggs" --> "large+eggs"
            exclude = request.form["exclude"].replace(" ","+").split(",") 
            maketime = request.form["time"]
            tag = ""
            #return render_template("results.html")
            if keyword:
                tag = tag + "&q=" + keyword
            if include:
                for i in include:
                    if len(i)>0:
                        tag = tag + "&allowedIngredient[]=" + i
            if exclude:
                for i in exclude:
                    if len(i)>0:
                        tag = tag + "&excludedIngredient[]=" + i
            if maketime:
                tag = tag + "&maxTotalTimeInSeconds=" + maketime            
            #checks if the same search has been made in last 24hrs
            #if so, returns a saved copy of the search results
            #otherwise, make api request and save new search results
            #saves us a bunch of api calls so we don't go over limit
            srch = searchdb.find_one({"tag":tag})
            curtime = int(time.time())
            if srch:
                if curtime-srch["time"] > 60*60*24:
                    srch["time"] = curtime
                    srch["json"] = function.findFoods(tag)
                    searchdb.save(srch)
            else:
                srch = {"tag":tag,
                        "time":curtime,
                        "json":function.findFoods(tag)}
                searchdb.insert(srch)
            res_string = srch["json"]
            
            d = json.loads(res_string)
            matches = d['totalMatchCount']
            return render_template("findfoods.html",
                                   tag=tag,
                                   matches=matches,
                                   d=d)
        else:
            return redirect("/")

if __name__=="__main__":
    app.debug=True
    app.run()
