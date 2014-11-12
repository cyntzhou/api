from flask import Flask,request,url_for,redirect,render_template
import urllib2, json

appid = "65fb5a0e"
appkey = "f8cbfed212e664b2f56f9e04a91c1bc9" 	

def findFoods(tag):
     url = "http://api.yummly.com/v1/api/recipes?_app_id="+appid+"&_app_key="+appkey+"%s" #<--got rid of the &q= because the person might not necessarily enter a keyword
     url = url%(tag)
     request = urllib2.urlopen(url)
     res_string = request.read()
     #print "made an api request"
     return res_string

#MICHAEL, WHEN WE USED THE GET URL IN CLASS YESTERDAY IT WAS ACTUALLY THE SEARCH URL; THAT'S WHY IT SHOWED MULTIPLE RESULTS.. BECAUSE NOW WHEN I TRY TO SEARCH FOR SOMETHING USING THE GET URL, THE PAGE IS TELLING ME TO USE THE EXACT RECIPE-ID
def calcFoods(id):
     url = "http://api.yummly.com/v1/api/recipe/"+id+"?_app_id="+appid+"&_app_key="+appkey
     request = urllib2.urlopen(url)
     res_string = request.read()
     d = json.loads(res_string)
     x = "The calories for this food is "
     #keys:totalTime,ingredientLines,attribution,name,rating,numberOfServings,yield,nutritionEstimates,source,flavors,images,attributes,id,totalTimeInSeconds
     x+=str(d['nutritionEstimates'][0].get("value"))
     return x;
          
