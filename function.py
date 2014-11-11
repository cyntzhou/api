from flask import Flask,request,url_for,redirect,render_template
import urllib2, json

def findFoods(tag):
     url = "http://api.yummly.com/v1/api/recipes?_app_id=e8e8c50c&_app_key=4c0512521aa32bbd045b29900f91a176%s" #<--got rid of the &q= because the person might not necessarily enter a keyword
     url = url%(tag)
     request = urllib2.urlopen(url)
     res_string = request.read()
     d = json.loads(res_string)
     matches = d['totalMatchCount']
     return render_template("findfoods.html",
                            tag=tag,
                            matches=matches,
                            d=d)
     return page

#MICHAEL, WHEN WE USED THE GET URL IN CLASS YESTERDAY IT WAS ACTUALLY THE SEARCH URL; THAT'S WHY IT SHOWED MULTIPLE RESULTS.. BECAUSE NOW WHEN I TRY TO SEARCH FOR SOMETHING USING THE GET URL, THE PAGE IS TELLING ME TO USE THE EXACT RECIPE-ID
def calcFoods(id):
     url = "http://api.yummly.com/v1/api/recipe/recipe-id?_app_id=e8e8c50c&_app_key=4c0512521aa32bbd045b29900f91a176%s"
     url = url%(id)
     request = urllib2.urlopen(url)
     res_string = request.read()
     d=json.loads(res_string)
     x = "The calories for this food is"
     if d['nutritionEstimates'].get(0)[value] != Null:
          x+=d['nutritionEstimates'].get(0)[value]  
     else:
          x+= " not available"
     return x;
          
