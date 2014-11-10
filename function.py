import urllib2, json

def findFoods(tag):
     url = "http://api.yummly.com/v1/api/recipes?_app_id=e8e8c50c&_app_key=4c0512521aa32bbd045b29900f91a176&q=%s"
    url = url%(tag)
    request = urllib2.urlopen(url)
    res_string = request.read()
    d = json.loads(res_string)
    matches = d['totalMatchCount']
    page = "Search for "+tag+": "+str(matches)+" matches.<br>"
    for r in d['matches']:
        #keys = flavors,rating,totalTimeInSeconds,ingredients,smallImageUrls,sourceDisplayName,recipeName,attributes,id,imageUrlsBySize
        page = page + "<br><br>" + "<a href='http://www.yummly.com/recipe/" + \
               r['id'] + "'>" + r['recipeName'] + "</a>" + "<br>Rating: " + \
               str(r['rating']) + "<br>Ingredients: "
        for i in r['ingredients']:
            page = page + i + ", "
        page = page + "<br>" + "<img height=200 src=%s>"%(r['smallImageUrls'][0])
    return page

def calcFoods(tag):
    url = "http://api.yummly.com/v1/api/recipes?_app_id=e8e8c50c&_app_key=4c0512521aa32bbd045b29900f91a176&q=%s"
    url = url%(tag)
    request = urllib2.urlopen(url)
    res_string = request.read()
    d=json.loads(res_string)
    x = "The calories for this food is"
    if d['nutritionEstimates'].get(0)[value] != Null:
        x+=d['nutritionEstimates'].get(0)[value]  
    else:
        x+= " not available"

    return x;
    
