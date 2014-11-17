from flask import Flask,request,url_for,redirect,render_template,session
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
@app.route("/get/<id>")
def get(id=""):
    if id:
        d = function.moreInfo(id) #returns a dictionary or False
        if d:
            n = {}
            for r in d['nutritionEstimates']:
                print r['attribute']
                print r['description']
                n[r['attribute']] = str(r['value'])+r['unit']['abbreviation']
            return render_template("get.html",d=d,n=n)
    return "Invalid"
    
@app.route("/", methods=["GET","POST"])
def search():
    if request.method=="GET":
        return render_template("search.html")
    else:
        button = request.form["button"]
        if button=="search":
            keyword = request.form["keyword"].replace(" ","+")
            include = request.form["include"].replace(" ","+").split(",") #list of ingredients with spaces replaced by +, e.g. "large eggs" --> "large+eggs"
            exclude = request.form["exclude"].replace(" ","+").split(",") 
            maketime = request.form["time"] #seconds
            if maketime:
                maketime = str(int(request.form["time"])*60) #seconds
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
            res_string = srch["json"]
            d = json.loads(res_string)
            #This fixes an error where it would crash if no images were found,replace this with a better one if you want
            for x in d['matches']:
                if 'smallImageUrls' not in x.keys():
                    x['smallImageUrls']= "http://www.education.umd.edu/Academics/Faculty/Bios/images/generic_sm.jpg"

            
        
            return render_template("findfoods.html",
                                   tag=tag,
                                   d=d)
            #                       calc = cal)
        else:
            return redirect("/")

if __name__=="__main__":
    app.debug=True
    app.run()
