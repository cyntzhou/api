from flask import Flask,request,url_for,redirect,render_template
from pymongo import MongoClient
import function
import urllib2, json

appid = "65fb5a0e"
appkey = "f8cbfed212e664b2f56f9e04a91c1bc9" 	

app=Flask(__name__)

mongo = MongoClient()
dbname = "cynmiclawyummly"
db = mongo[dbname]
recipedb = db['recipes']

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
    #url = "http://api.yummly.com/v1/api/recipe/recipe-id?_app_id=e8e8c50c&_app_key=4c0512521aa32bbd045b29900f91a176Healthy-Morning-Muffins-Martha-Stewart"
    url = "http://api.yummly.com/v1/api/recipes?_app_id="+appid+"&_app_key="+appkey+"&q=cookie"
    request = urllib2.urlopen(url)
    res_string = request.read()
    return res_string
    
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
            time = request.form["time"]
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
            if time:
                tag = tag + "&maxTotalTimeInSeconds=" + time            
            return function.findFoods(tag)
        else:
            return redirect("/")
        return None

if __name__=="__main__":
    app.debug=True
    app.run()
