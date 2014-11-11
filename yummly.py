from flask import Flask,request,url_for,redirect,render_template
import urllib2, json
import function

app=Flask(__name__)
@app.route("/")
def index():
    return "Yummly"

@app.route("/t")
@app.route("/t/<tag>")
def t(tag="Cookies"):
    return function.findFoods(tag)

@app.route("/get")
def get():
    url = "http://api.yummly.com/v1/api/recipe/recipe-id?_app_id=e8e8c50c&_app_key=4c0512521aa32bbd045b29900f91a176Healthy-Morning-Muffins-Martha-Stewart"
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
                    tag = tag + "&allowedIngredient[]=" + i
            if exclude:
                for i in exclude:
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
