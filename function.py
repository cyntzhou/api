from flask import Flask,request,url_for,redirect,render_template
import urllib2, json

appid = "65fb5a0e"
appkey = "f8cbfed212e664b2f56f9e04a91c1bc9" 	

def findFoods(tag):
     url = "http://api.yummly.com/v1/api/recipes?_app_id="+appid+"&_app_key="+appkey+"%s"
     url = url%(tag)
     request = urllib2.urlopen(url)
     res_string = request.read()
     d = json.loads(res_string)
     #This fixes an error where it would crash if no images were found,replace this with a better one if you want
     for x in d['matches']:
          if 'smallImageUrls' not in x.keys():
               x['smallImageUrls']= "http://www.woodus.com/den/gallery/graphics/dqm4ds/monster/nopic.png"
     return d

#MICHAEL, WHEN WE USED THE GET URL IN CLASS YESTERDAY IT WAS ACTUALLY THE SEARCH URL; THAT'S WHY IT SHOWED MULTIPLE RESULTS.. BECAUSE NOW WHEN I TRY TO SEARCH FOR SOMETHING USING THE GET URL, THE PAGE IS TELLING ME TO USE THE EXACT RECIPE-ID
def moreInfo(id): #might get an error if invalid recipe-id
     try:
          url = "http://api.yummly.com/v1/api/recipe/"+id+"?_app_id="+appid+"&_app_key="+appkey
          request = urllib2.urlopen(url)
          res_string = request.read()
          d = json.loads(res_string)
          #keys:totalTime,ingredientLines,attribution,name,rating,numberOfServings,yield,nutritionEstimates,source,flavors,images,attributes,id,totalTimeInSeconds
          return d;
     except:
          return False

def nutritionInfo(id):
     d = moreInfo(id) #returns a dictionary or False
     if d:
          n = {} #stores the nutritional info
          for r in d['nutritionEstimates']:
               n[r['attribute']] = str(int(r['value']))+" "+r['unit']['abbreviation']
          return n
     else:
          return False

def calcFoods(id):
     if moreInfo(id):
          return moreInfo(id)['nutritionEstimates'][0].get("value")
     else:
          return False
