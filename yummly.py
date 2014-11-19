from flask import Flask,request,url_for,redirect,render_template,session
from pymongo import MongoClient
import time
import urllib2, json
import function
import re

appid = "65fb5a0e"
appkey = "f8cbfed212e664b2f56f9e04a91c1bc9" 	

app=Flask(__name__)

mongo = MongoClient()
dbname = "cynmiclawyummly"
db = mongo[dbname]
searchdb = db['searches']
mealdb = db['meals']

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
@app.route("/get/<id>", methods=["GET","POST"])
def get(id=""):
    if id:
        n = function.nutritionInfo(id) #returns a dict of nutritionalInfo or False
        d = function.moreInfo(id)
        if n and d:
            if request.method=="GET":
                return render_template("get.html",d=d,n=n)
            else:
                button = request.form["button"]
                if button=="Add to Meal Plan":
                    n['id'] = id
                    n['name'] = d['name']
                    mealdb.insert(n)
                    return redirect("/mealplan")
                return render_template("get.html",d=d,n=n)
    return "Invalid"

@app.route("/mealplan", methods=["GET","POST"])
def mealplan():
    if request.method=="POST":
        button = request.form["button"]
        if button == "Clear All Recipes":
            mealdb.remove({})
        else: #the user must want to remove an individual recipe
            mealdb.remove({'id':button})
    d = {'recipes':{}}
    r = re.compile("[0-9]+")
    for recipe in mealdb.find():
        for nutrition in recipe:
            d['recipes'][recipe['id']] = recipe['name']
            if not nutrition=='id' and not nutrition=='name':
                nutrition = nutrition.encode('ascii')
                value = str(recipe[nutrition])
                f = r.findall(value)
                number = f[0] #an int
                if nutrition in d.keys():
                    d[nutrition] = int(number)+int(d[nutrition])
                else:
                    d[nutrition] = number
    return render_template("mealplan.html",d=d)

@app.route("/", methods=["GET","POST"])
def search():
    if request.method=="GET":
        return render_template("search.html")
    else:
        button = request.form["button"]
        if button=="search":
            keyword = request.form["keyword"].strip().replace(" ","+")
            include = request.form["include"].lower().split(",") #list of ingredients with spaces replaced by +, e.g. "large eggs" --> "large+eggs"
            exclude = request.form["exclude"].lower().split(",") 
            for i in include:
                include[include.index(i)] = i.strip().replace(" ","+") 
            for i in exclude:
                exclude[exclude.index(i)] = i.strip().replace(" ","+")
            maketime = request.form["time"] #seconds
            if maketime:
                try:
                    maketime = str(int(request.form["time"])*60) #seconds
                except:
                    return "Invalid"
            course = request.form.getlist("course")
            cuisine = request.form.getlist("cuisine")
            tag = ""
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
            if cuisine:
                for i in cuisine:
                    tag = tag + "&allowedCuisine[]=cuisine^cuisine-" + i.lower()
            if course:
                for i in course:
                    tag = tag + "&allowedCourse[]=course^course-" + i
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

            d = function.findFoods(tag)
            return render_template("findfoods.html",
                                   tag=tag,
                                   d=d)
            #                       calc = cal)
        else:
            return redirect("/")

if __name__=="__main__":
    app.debug=True
    app.run()
