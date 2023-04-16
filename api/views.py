




from django.shortcuts import render
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status

 
from PIL import Image
import math

from api.decorators   import auth_required
#from PyPDF2 import PdfFileReader, PdfFileWriter

import json
from bson import ObjectId

 
from django.core.serializers.json import DjangoJSONEncoder
import random

from django.http import HttpResponseRedirect , HttpResponse

from django.contrib.auth.decorators import login_required, permission_required

 
from rest_framework.decorators import api_view

import pymongo
from pymongo import MongoClient

from datetime import date
import datetime
import json
from bson.objectid import ObjectId

from pymongo import MongoClient
import os ,time
import os.path
from django.core.files.storage import FileSystemStorage

from rest_framework import exceptions
 
from django.conf import settings

import jwt

import boto3
from botocore.exceptions import ClientError
import io
import logging

 
 
 



import sys
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import numpy  




from io import BytesIO
import base64
from base64 import b64encode
from json import dumps


from django.contrib.auth.hashers import make_password


sidimedDBclient = MongoClient('mongodb://sidimedsDBuser:sidimedsDBpassword@ec2-52-209-2-160.eu-west-1.compute.amazonaws.com:27017/sidimedsDB')
sidimedsDB = sidimedDBclient['sidimedsDB']
statistics = sidimedsDB['statistics']




client = MongoClient('localhost', 27017)

ads_db = client['ads_db']
ads_advertisement = ads_db['ads_advertisement']

s3_client = boto3.client('s3', region_name='eu-west-1', aws_access_key_id="AKIAIBQCNDBH2TWENTCA",
                               aws_secret_access_key="/59vNE5Ab+OSJnqhXpU8vVCGU1vBlLqv28qnsWnf")


# Create your views here.

@api_view(['GET', 'POST', 'DELETE'])
def tutorial_list(request):
    # GET list of tutorials, POST a new tutorial, DELETE all tutorials
    return JsonResponse({'message': 'Tutorial was deleted successfully!'}, status=status.HTTP_200_OK)


@api_view(['POST'])
def create_ad(request):



    photos = [] 
    for filename, file in request.FILES.items():
         
        photos.append(handle_uploaded_file(file))  # upload files locally
        
        #photos.append(upload_my_file("sidimedsbucket", "django_media_files",  "eu-west-1" ,file)) # upload files to s3


    ad_model = {




        "title": request.POST['title'],
        "publisher": {
            "name": request.POST['publisherName'],
            "phoneNumber": request.POST['publisherPhoneNumber'],
            "password": make_password(request.POST['password']) # make a password gives different results for the same password, see that later
        },

        "publishingDate": datetime.datetime.now(),

        "geometry": {
            "type": "Point",
            "coordinates": [float(request.POST['longitude']), float(request.POST['latitude'])]
        },
        "photos": photos
    }

    ads_advertisement.insert_one(ad_model)
 
    retour = json.dumps(ad_model, default=str)
    retour_parsed = json.loads(retour)
    
    return JsonResponse(retour_parsed, status=status.HTTP_201_CREATED)




@api_view(['GET'])
def getsAds(request):

    cursor = ads_advertisement.find({})
    json_ads = []
    for doc in cursor:
        retour = json.dumps(doc, default=str)
        json_ads.append(json.loads(retour))

    return JsonResponse(json_ads, safe=False)


@api_view(['GET'])
def getAdDetails(request):

    input = JSONParser().parse(request)
    ad = ads_advertisement.find_one({"_id": ObjectId(input["_id"])})
    print(input["_id"])
    print(ad)

    if ad:
        retour = json.dumps(ad, default=str)
        retour_parsed = json.loads(retour)
    else:
        retour_parsed = {}

    print(retour_parsed)

    return JsonResponse(retour_parsed, safe=False)
    
@api_view(['GET'])
def getAdsNearMe(request):

    input = JSONParser().parse(request)
    

    cursor = ads_advertisement.aggregate([

        {
            '$geoNear': {
                'near': {'type': 'Point', 'coordinates': [float(input['longitude']), float(input['latitude'])]},
                'query': {},
                'distanceField': "dist.calculated",
                'includeLocs': "dist.location",

                'minDistance': 1,
                'maxDistance': 10000000,
                'spherical': True

            },


        },
        {'$limit': 30}

    ])
    json_ads = []
    for doc in cursor:
        retour = json.dumps(doc, default=str)
        json_ads.append(json.loads(retour))

    return JsonResponse(json_ads, safe=False)


@api_view(['PUT'])
def updateAd(request): 
     

    input = JSONParser().parse(request)
    obj = {}

    if input['title']:
        print(input['title'])
        obj['title'] = input['title']
 

    print(obj)
    _id = input["_id"]
    del input["_id"]

    print(input)
    
    ad = ads_advertisement.update_one({'_id': ObjectId(_id)},{"$set":  obj} ,upsert=True)
    print(ad)
    return JsonResponse({"status": "updated"}, status=status.HTTP_201_CREATED)

@api_view(['DELETE'])
def deleteAd(request): 
      

    input = JSONParser().parse(request)
 
    _id = input["_id"]
    print(_id)
    ad = ads_advertisement.delete_one({ "_id": _id })
    #print(ad)


    return JsonResponse({"status": "deleted"}, safe=False)




@api_view(['POST'])
@auth_required
def getSomething(request):

 
    return JsonResponse({"token": "ca marche"}, safe=False)



@api_view(['GET'])
def login(request):

    key = settings.JWT_KEY
    now = datetime.datetime.utcnow()
    payload ={

        'id':  random.randint(1, 100),
        'exp': now +datetime.timedelta(days=1000),
        'iat': now
    }
    encoded = jwt.encode(payload, key, algorithm="HS256")

    
    return JsonResponse({"token": encoded}, safe=False)

def upload_my_file(bucket, folder, region , file):
        


        split_tup = os.path.splitext(file.name)
        key = folder+'/'+str(round(time.time() * 1000)) + split_tup[len(split_tup)-1]
        print('key = '+key)
        try:

            response = s3_client.upload_fileobj(file, bucket, key , ExtraArgs={ 'ContentType': 'image/jpeg','ACL': 'public-read'})
                    
        except ClientError as e:
            print(e)
            return False
        print( 'https://'+bucket+'.s3.'+region+'.'+'amazonaws.com/'+key)
       
        return 'https://'+bucket+'.s3.'+region+'.'+'amazonaws.com/'+key

def handle_uploaded_file(f):  

    print(f)

    split_tup = os.path.splitext(f.name)
    name = 'uploads/'+str(round(time.time() * 1000)) + split_tup[len(split_tup)-1]
     
    fs = FileSystemStorage()
    filename = fs.save(name,f)
    uploaded_file_url = fs.url(filename)
    return uploaded_file_url







@api_view(['GET'])
def getUniqueVisitorsCount(request):



    
    today = date.today()
    tonightAtmidnight = datetime.datetime.combine(today, datetime.datetime.min.time())
   
    cursor = statistics.distinct("id" , {"page": "map" , "visitDate": { "$lt": datetime.datetime.now(), "$gte":  tonightAtmidnight}}   ) 
    
    
    counter = len(list(cursor))

    return JsonResponse({"uniqueVisitors": counter}, safe=False)

@api_view(['GET'])
def getUniqueVisitorsLast24Hours(request):



    last24Hours = datetime.datetime.now() - datetime.timedelta(days=1)    
   
   
    cursor = statistics.distinct("id" , {"page": "map" , "visitDate": {  "$gte":  last24Hours}}   )
    
    
    counter = len(list(cursor))

    return JsonResponse({"uniqueVisitors": counter}, safe=False)

@api_view(['GET'])
def getUniqueVisitorsLast30Days(request):


    last30days = datetime.datetime.now() - datetime.timedelta(days=30)    
    cursor = statistics.distinct("id" , {"page": "map" , "visitDate": {  "$gte":  last30days}}   ) 
    counter = len(list(cursor))

    return JsonResponse({"uniqueVisitors": counter}, safe=False)


@api_view(['GET'])
def getVisistsCountLast24Hours(request):

    last24Hours = datetime.datetime.now() - datetime.timedelta(days=1)       
    cursor = statistics.find({"page": "map" , "visitDate": {  "$gte":  last24Hours}}   )
    counter = len(list(cursor))
    return JsonResponse({"uniqueVisitors": counter}, safe=False)


@api_view(['GET'])
def getVisitsCountLast365Hours(request):

    print("inside getVisitsCountLast365Hours")

    last365Hours = datetime.datetime.now() - datetime.timedelta(days=365)       
    cursor = statistics.find({"page": "map" , "visitDate": {  "$gte":  last365Hours}}   )
    counter = len(list(cursor))
    return JsonResponse({"visitsCount": counter}, safe=False)



@api_view(['GET'])
def getUniqueVisitorsOfLast365Days(request):


    lastyear = datetime.datetime.now() - datetime.timedelta(days=365)    
 
    cursor = statistics.distinct("id" , {"page": "map"  ,  "visitDate" : { "$gt":  lastyear }}   )

    counter = len(list(cursor))
 
    return JsonResponse({"uniqueVisitors": counter}, safe=False)


@api_view(['GET'])
def getUniqueVisitorsOfAllTime(request):
    cursor = statistics.distinct("id" , {"page": "map" }   )
    counter = len(list(cursor))
 
    return JsonResponse({"uniqueVisitors": counter}, safe=False)

@api_view(['GET'])
def getUniqueVisitorsThatVisitedForTheFirstTimeEverInTheLast24Hours(request):


    cursor1 = statistics.distinct("id" , {"page": "map" }   ) # all time

    counterAllTime = len(list(cursor1))


    last24Hours = datetime.datetime.now() - datetime.timedelta(days=1)    

    cursor2 = statistics.distinct("id" , {"page": "map"  ,  "visitDate" : { "$lt":  last24Hours } }   ) # all time minus 24 hours

    counterAllTimeMinus24Hours = len(list(cursor2))

    resu = counterAllTime - counterAllTimeMinus24Hours

    return JsonResponse({"uniqueVisitors": resu}, safe=False)

@api_view(['GET'])
def getUniqueVisitorsThatVisitedForTheFirstTimeEverInTheLast30Days(request):

    last30Days = datetime.datetime.now() - datetime.timedelta(days=30)  
    now = datetime.datetime.now()

    cursor1 = statistics.distinct("id" , {"page": "map"  }   ) # all time
    counterAllTime = len(list(cursor1))


    cursor2 = statistics.distinct("id" , {"page": "map"  ,  "visitDate" : { "$lt":  last30Days } }   ) # all time minus 30 hours

    counterAllTimeMinus30Days = len(list(cursor2))

    resu = counterAllTime - counterAllTimeMinus30Days

    return JsonResponse({"uniqueVisitors": resu}, safe=False)


    

@api_view(['GET'])
def getRegionsOfCountry(request):

    input = JSONParser().parse(request)
    cursor = statistics.distinct("region" , {"page": "map" , "country": str(input['country']) }   )

    regions = []

    for doc in cursor:
        retour = json.dumps(doc, default=str)
        regions.append(json.loads(retour))

    counter = len(list(cursor))
    return JsonResponse({"regions": regions}, safe=False)


@api_view(['GET'])
def getCitiesOfRegion(request):

    input = JSONParser().parse(request)
    cursor = statistics.distinct("city" , {"page": "map" , "country": str(input['country']) , "region": str(input['region'] ) }   )

    cities = []

    for doc in cursor:
        retour = json.dumps(doc, default=str)
        cities.append(json.loads(retour))

    counter = len(list(cursor))
    return JsonResponse({"cities": cities}, safe=False)


@api_view(['GET'])
def getCountriesForLast24Hours(request):


    last24Hours = datetime.datetime.now() - datetime.timedelta(days=1)    
    cursor = statistics.distinct("country" , {"page": "map"  ,  "visitDate" : { "$gte":  last24Hours }  }   ) 
    json_ads = []

    for doc in cursor:
        if doc != "404" and doc != "Côte d'Ivoire":
            retour = json.dumps(doc, default=str)
            json_ads.append(json.loads(retour))

    
    return JsonResponse({"countries": json_ads}, safe=False)

@api_view(['GET'])
def getAllCountries(request):

    cursor = statistics.distinct("country" , {"page": "map" }   ) 
    json_ads = []

    for doc in cursor:
        if doc != "404" and doc != "Côte d'Ivoire":
            retour = json.dumps(doc, default=str)
            json_ads.append(json.loads(retour))

    
    return JsonResponse({"countries": json_ads}, safe=False)


@api_view(['GET'])
def getAllCountriesThatvisitedForFirstTimeInLastMonth(request):

    dateOfStart = datetime.datetime.now() - datetime.timedelta(days=30)

    cursor1 = statistics.distinct("country" , {"page": "map"  , "visitDate": {"$lte": dateOfStart} }  ) 
    countries_list_except_last_month = []

    for doc in cursor1:
        if doc != "404" and doc != "Côte d'Ivoire":
            retour = json.dumps(doc, default=str)
            countries_list_except_last_month.append(json.loads(retour))


    
    cursor2 = statistics.distinct("country" , {"page": "map" }   ) 
    countries_list_Alltime = []

    for doc in cursor2:
        if doc != "404" and doc != "Côte d'Ivoire":
            retour = json.dumps(doc, default=str)
            countries_list_Alltime.append(json.loads(retour))

    
    difference = set(countries_list_Alltime) - set(countries_list_except_last_month)
    list_difference = list(difference)

    
    return JsonResponse({"countriesThatvisitedForFirstTimeInLastMonth": list_difference}, safe=False)


@api_view(['GET'])
def getUniqueVisitorsFromAndFromOutsideMauritania(request): # get unique visitors from and from outside Mauritania

    cursorMauritania = statistics.distinct("id" , {"page": "map" , "country": "Mauritania" }   )
    cursorTotal = statistics.distinct("id" , {"page": "map" }   )

    counterMauritania = len(list(cursorMauritania))
    counterTotal = len(list(cursorTotal))
    counterRestOfWorld = counterTotal - counterMauritania

    x = ["Total" , "Mauritania", "Rest Of the World"]
    y = [counterTotal , counterMauritania, counterRestOfWorld]

    uniqueId = str(round(time.time() * 1000)) + "_"+str(random.randint(1, 10000))
    file = uniqueId+".png"

    plt.bar( x , y ,  color = "purple")

    plt.ylabel("Visiteurs Uniques")

    
    
    
    for i in range(len(x)): 
        plt.text( i , y[i] ,  str(y[i]) +" (" +  str( float("{0:.1f}".format((y[i]/counterTotal) * 100)) )  + "%)" , ha="center" , va="bottom" )

    plt.savefig(file)

    with open(file, 'rb') as open_file:
        byte_content = open_file.read()

        # second: base64 encode read data
        # result: bytes (again)
    base64_bytes = b64encode(byte_content)

        # third: decode these bytes to text
        # result: string (in utf-8)
    base64_string = base64_bytes.decode('utf-8')
    if os.path.exists(file):
        print("The file does exist")
        os.remove(file)

        if not(os.path.exists(file)):
            print("The file does not exist anymore")
        else:
            print("The file does not exist")

    return JsonResponse({"resu": base64_string}, safe=False)


@api_view(['GET'])
def getMachineLearning(request):
 
        x = numpy.random.normal(5.0, 1.0, 1000)
        y = numpy.random.normal(10.0, 2.0, 1000)
        uniqueId = str(round(time.time() * 1000)) + "_" + str(random.randint(1, 10000))
        file = uniqueId+".png"

        

        plt.scatter(x, y)
        plt.savefig(file)
        

        with open(file, 'rb') as open_file:
            byte_content = open_file.read()

        # second: base64 encode read data
        # result: bytes (again)
        base64_bytes = b64encode(byte_content)

        # third: decode these bytes to text
        # result: string (in utf-8)
        base64_string = base64_bytes.decode('utf-8')

        if os.path.exists(file):
            print("The file does exist")
            os.remove(file)

            if not(os.path.exists(file)):
                print("The file does not exist anymore")
        else:
            print("The file does not exist")
 

        return JsonResponse({"resu": base64_string}, safe=False)


# make about operating system
# make one about countries and cities, if click on a country you get the regions if you click the region you get the city

""" @api_view(['GET'])
def extractTextFromPdf(request):
    

    
    BASE = os.path.dirname(os.path.abspath(__file__))
    print(BASE)

    #data = open(os.path.join(BASE, 'Lecture.pdf'))

    file_path = '/Users/mac/elwagiha_com/elwagiha_com/api/file.pdf'
    pdf = PdfFileReader(file_path)
    
    with open('Lecture Note.txt', 'w') as f:
        for page_num in range(pdf.numPages):
            # print('Page: {0}'.format(page_num))
            pageObj = pdf.getPage(page_num)

            try: 
                txt = pageObj.extractText()
                print(txt)
                print(''.center(100, '-'))
            except:
                pass
            else:
                f.write('Page {0}\n'.format(page_num+1))
                f.write(''.center(100, '-'))
                f.write(txt)
                print(txt)
        f.close()

    return JsonResponse({"status": 200}, safe=False) """

 

def sort_months(json):
    try:
        # Also convert to int since update_time will be string.  When comparing
        # strings, "10" is smaller than "2".
        return int(json['month'])
    except KeyError:
        return 0

@api_view(['POST'])
def getUniqueVisitorsPerMonth(request):

    print("-------------->")
    input = JSONParser().parse(request)
    rotate = input['isMobile']
 
    dateOfStart = datetime.datetime(2022,1,1)
    cursor = statistics.aggregate([

    {
        "$match": {  "page" : "map"  , "visitDate" : {"$gte": dateOfStart}}
    },
    {
        "$group": { "_id": { "year": { "$year": "$visitDate" } , "month": { "$month": "$visitDate" } }, "id": { "$addToSet": "$id"} }
    }, 
    {
        "$unwind":"$id"
    },
    {
        "$group": { "_id": "$_id", "idCount": { "$sum":1} }
    }
    ])

 
    list_months_counts = {}
    for doc in cursor:
        retour = json.dumps(doc, default=str)
        item = json.loads(retour)
        if item['_id']['month'] > 9:
            my_month = str(item['_id']['year']) +'-'+str(item['_id']['month'])
        else:
            my_month = str(item['_id']['year']) +'-'+'0'+str(item['_id']['month'])
        my_count = item['idCount']
        list_months_counts[my_month] = my_count
        #list_months_counts.append({"month": my_month, "uniqueVisitors": my_count})
    

    #list_months_counts_sorted = sorted(list_months_counts, key=lambda k: k['month'], reverse=False)
    list_months_counts_sorted = dict(sorted(list_months_counts.items(), key=lambda item: item[0] ,  reverse=False))
    base64_list_months_counts_sorted = generate_base64_image(list_months_counts_sorted , "Visiteurs Uniques par Mois" , rotate)
    return JsonResponse([base64_list_months_counts_sorted], safe=False)


@api_view(['POST'])
def getUniqueVisitorsPerOs(request):

    input = JSONParser().parse(request)
    rotate = input['isMobile']

    dateOfStart = datetime.datetime.now() - datetime.timedelta(days=365) 

    #dateOfStart = datetime.datetime(2022,1,1)
    cursor = statistics.aggregate([

    {
        "$match": {  "page" : "map"  , "visitDate" : {"$gte": dateOfStart}}
    },
    {
        "$group": { "_id": {"os": "$os" }, "id": { "$addToSet": "$id"} }
    }, 
    {
        "$unwind":"$id"
    },
    {
        "$group": { "_id": "$_id", "idCount": { "$sum":1} }
    }
    ])
 
    list_os_counts = {}
    for doc in cursor:
        retour = json.dumps(doc, default=str)
        item = json.loads(retour)
        
        os = item['_id']['os']
        my_count = item['idCount']
        list_os_counts[os] = my_count
        #list_months_counts.append({"month": my_month, "uniqueVisitors": my_count})
    

    #list_months_counts_sorted = sorted(list_months_counts, key=lambda k: k['month'], reverse=False)
    list_os_counts_sorted = dict(sorted(list_os_counts.items(), key=lambda item: item[1] ,  reverse=True))
    base64_list_os_counts_sorted = generate_base64_image(list_os_counts_sorted , "Visiteurs Uniques par Systèmes d'Exploitation durant les derniers 365 jours", rotate)
    return JsonResponse([base64_list_os_counts_sorted], safe=False)


@api_view(['POST'])
def getUniqueVisitorsPerDevice(request):

    input = JSONParser().parse(request)
    rotate = input['isMobile']

    #dateOfStart = datetime.datetime(2022,1,1)

    dateOfStart = datetime.datetime.now() - datetime.timedelta(days=365) 
    cursor = statistics.aggregate([

    {
        "$match": {  "page" : "map"  , "visitDate" : {"$gte": dateOfStart}}
    },
    {
        "$group": { "_id": {"device": "$device" }, "id": { "$addToSet": "$id"} }
    }, 
    {
        "$unwind":"$id"
    },
    {
        "$group": { "_id": "$_id", "idCount": { "$sum":1} }
    }
    ])
 
    list_device_counts = {}
    for doc in cursor:
        retour = json.dumps(doc, default=str)
        item = json.loads(retour)
        
        device = item['_id']['device']
        my_count = item['idCount']
        list_device_counts[device] = my_count
        #list_months_counts.append({"month": my_month, "uniqueVisitors": my_count})
    

    #list_months_counts_sorted = sorted(list_months_counts, key=lambda k: k['month'], reverse=False)
    list_device_counts_sorted = dict(sorted(list_device_counts.items(), key=lambda item: item[1] ,  reverse=True))
    base64_list_device_counts_sorted = generate_base64_image(list_device_counts_sorted , "Visiteurs Uniques Par Appareil durant les derniers 365 jours" , rotate)
    return JsonResponse([base64_list_device_counts_sorted], safe=False)


@api_view(['POST'])
def getUniqueVisitorsPerCity(request):

    input = JSONParser().parse(request)

    dateOfStart = datetime.datetime(2022,1,1)

    #dateOfStart = datetime.datetime.now() - datetime.timedelta(days=1)   


    cursor = statistics.aggregate([
 
        {
            "$match": {  "page" : "map" , "country": input['country'] , "region": input['region']  , "visitDate" : {"$gte": dateOfStart}}
        },
        {
            "$group": { "_id" : {"city" : "$city" }, "id": { "$addToSet": "$id"} }
        }, 
        {
            "$unwind":"$id"
        },
        {
            "$group": { "_id": "$_id", "idCount": { "$sum":1} }
        }

    ])

    list_cities_counts = {}
 

    for doc in cursor:
        retour = json.dumps(doc, default=str)
        item = json.loads(retour)
        
        city = item['_id']['city']
        my_count = item['idCount']

        list_cities_counts[city] = my_count


    list_cities_counts_sorted = dict(sorted(list_cities_counts.items(), key=lambda item: item[1] ,  reverse=True))

    return JsonResponse(list_cities_counts_sorted, safe=False)
 


@api_view(['POST'])
def getUniqueVisitorsPerCityForLast24Hours(request):

    input = JSONParser().parse(request)

    #dateOfStart = datetime.datetime(2022,1,1)

    dateOfStart = datetime.datetime.now() - datetime.timedelta(days=1)   


    cursor = statistics.aggregate([
 
        {
            "$match": {  "page" : "map" , "country": input['country'] , "region": input['region']  , "visitDate" : {"$gte": dateOfStart}}
        },
        {
            "$group": { "_id" : {"city" : "$city" }, "id": { "$addToSet": "$id"} }
        }, 
        {
            "$unwind":"$id"
        },
        {
            "$group": { "_id": "$_id", "idCount": { "$sum":1} }
        }

    ])

    list_cities_counts = {}
 

    for doc in cursor:
        retour = json.dumps(doc, default=str)
        item = json.loads(retour)
        
        city = item['_id']['city']
        my_count = item['idCount']

        list_cities_counts[city] = my_count


    list_cities_counts_sorted = dict(sorted(list_cities_counts.items(), key=lambda item: item[1] ,  reverse=True))

    return JsonResponse(list_cities_counts_sorted, safe=False)


@api_view(['POST'])
def getUniqueVisitorsPerRegion(request):

    input = JSONParser().parse(request)

    dateOfStart = datetime.datetime(2022,1,1)

    print(dateOfStart)

    cursor = statistics.aggregate([
 
        {
            "$match": {  "page" : "map" , "country": input['country']  , "visitDate" : {"$gte": dateOfStart}}
        },
        {
            "$group": { "_id" : {"region" : "$region" }, "id": { "$addToSet": "$id"} }
        }, 
        {
            "$unwind":"$id"
        },
        {
            "$group": { "_id": "$_id", "idCount": { "$sum":1} }
        }

    ])

    list_regions_counts = {}
 

    for doc in cursor:
        retour = json.dumps(doc, default=str)
        item = json.loads(retour)
        
        region = item['_id']['region']
        my_count = item['idCount']

        list_regions_counts[region] = my_count


    list_regions_counts_sorted = dict(sorted(list_regions_counts.items(), key=lambda item: item[1] ,  reverse=True))

    return JsonResponse(list_regions_counts_sorted, safe=False)



@api_view(['POST'])
def getUniqueVisitorsPerRegionForLast24Hours(request):

    print('inside etUniqueVisitorsPerRegionForLast24Hours')
    input = JSONParser().parse(request)

    #dateOfStart = datetime.datetime(2022,1,1) 

    dateOfStart = datetime.datetime.now() - datetime.timedelta(days=1)   

    cursor = statistics.aggregate([
 
        {
            "$match": {  "page" : "map" , "country": input['country']  , "visitDate" : {"$gte": dateOfStart}}
        },
        {
            "$group": { "_id" : {"region" : "$region" }, "id": { "$addToSet": "$id"} }
        }, 
        {
            "$unwind":"$id"
        },
        {
            "$group": { "_id": "$_id", "idCount": { "$sum":1} }
        }

    ])

    list_regions_counts = {}
 

    for doc in cursor:
        retour = json.dumps(doc, default=str)
        item = json.loads(retour)
        
        region = item['_id']['region']
        my_count = item['idCount']

        list_regions_counts[region] = my_count


    list_regions_counts_sorted = dict(sorted(list_regions_counts.items(), key=lambda item: item[1] ,  reverse=True))

    return JsonResponse(list_regions_counts_sorted, safe=False)



@api_view(['POST'])
def getUniqueVisitorsPerCountry(request):

    input = JSONParser().parse(request)
    rotate = input['isMobile']

    dateOfStart = datetime.datetime(2022,1,1)

    #dateOfStart = datetime.datetime.now() - datetime.timedelta(days=365) 

    print(dateOfStart)

    cursor = statistics.aggregate([

        {
            "$match": {  "page" : "map"  , "visitDate" : {"$gte": dateOfStart}}
        },
        {
            "$group": { "_id" : {"country" : "$country" }, "id": { "$addToSet": "$id"} }
        }, 
        {
            "$unwind":"$id"
        },
        {
            "$group": { "_id": "$_id", "idCount": { "$sum":1} }
        }

    ])
 
    list_foreign_country_counts = {}
    list_mauritania_abroad_counts = {}

    mauritania_count = 0
    the_404_count = 0
    abroad_count = 0

    for doc in cursor:
        retour = json.dumps(doc, default=str)
        item = json.loads(retour)
        
        country = item['_id']['country']
        my_count = item['idCount']

        if country == "Mauritania":
            mauritania_count = my_count
        
        elif country == "404":
            the_404_count = my_count
        else:
            abroad_count =  abroad_count + my_count
            list_foreign_country_counts[country] = my_count
        #list_months_counts.append({"month": my_month, "uniqueVisitors": my_count})
    
    list_mauritania_abroad_counts["Mauritania"] = mauritania_count
    list_mauritania_abroad_counts["Abroad"] = abroad_count
    list_mauritania_abroad_counts["404"] = the_404_count

    
    base64_list_mauritania_abroad_counts = generate_base64_image(list_mauritania_abroad_counts, "Visiteurs Uniques Provenant de la Mauritanie et de l'Etranger ", rotate)
    

    #list_foreign_country_counts_sorted = dict(sorted(list_foreign_country_counts.items(), key=lambda item: item[1] ,  reverse=True))
    
    list_foreign_country_counts["Mauritania"] = mauritania_count
    sorted_list_foreign_country_counts = sort_countries(list_foreign_country_counts)  


    sorted_and_trimed_countries = sort_and_trim_countries(list_foreign_country_counts)

    

    base64_list_foreign_country_counts_sorted = generate_base64_image(sorted_and_trimed_countries, "Visiteurs Uniques Provenant de l'Etranger ", rotate)

    return JsonResponse([ sorted_list_foreign_country_counts , base64_list_foreign_country_counts_sorted , base64_list_mauritania_abroad_counts ], safe=False)



@api_view(['GET'])
def getUniqueVisitorsPerCountryDuringLast24Hours(request):

    #dateOfStart = datetime.datetime(2022,1,1)

    dateOfStart = datetime.datetime.now() - datetime.timedelta(days=1)   
    

    print(dateOfStart)

    cursor = statistics.aggregate([

        {
            "$match": {  "page" : "map"  , "visitDate" : {"$gte": dateOfStart}}
        },
        {
            "$group": { "_id" : {"country" : "$country" }, "id": { "$addToSet": "$id"} }
        }, 
        {
            "$unwind":"$id"
        },
        {
            "$group": { "_id": "$_id", "idCount": { "$sum":1} }
        }

    ])

    countries = {}

    for doc in cursor:
        retour = json.dumps(doc, default=str)
        item = json.loads(retour)
        
        country = item['_id']['country']
        my_count = item['idCount']

        countries[country] = my_count
    
    sorted_countries= dict(sorted(countries.items(), key=lambda item: item[1] ,  reverse=True)) 
 
    return JsonResponse([ sorted_countries ], safe=False)


@api_view(['GET'])
def getGraphs(request):

    input = JSONParser().parse(request)
    print("------------------------------>isMobile"+ input['isMobile'])
    cursor = statistics.aggregate([
        {
            "$group": {
                "_id": "$id",
                "country" : { "$addToSet": '$country' },
                "region" : { "$addToSet": '$region' },
                "city" : { "$addToSet": '$city' },

                "os" : { "$addToSet": '$os' },
                "device" : { "$addToSet": '$device' },
                "visitDate" : { "$addToSet": '$visitDate' },   
            }
        }
    ])

    #counter = len(list(cursor))

    devices = {}
    opearting_systems = {}
    countries = {}
    dates = {}
    mauritania_other_404 = {}

    json_ads = []

 
    for doc in cursor:

        retour = json.dumps(doc, default=str)
        item = json.loads(retour)
        #json_ads.append(item)

        device = item["device"][0]
        populate_devices(devices , device)
        

        os = item["os"][0]
        populate_opearting_systems(opearting_systems , os)


        country = item["country"][0]
        populate_mauritania_other_404(country ,mauritania_other_404)


        country = item["country"][0]
        populate_countries(country , countries)


        visitDate = item["visitDate"][0]
        populate_dates( visitDate, dates )
   


 
    sorted_mauritania_other_404 = dict(sorted(mauritania_other_404.items(), key=lambda item: item[1] ,  reverse=True)) 
    base64_string_mauritania_other_404 = generate_base64_image(sorted_mauritania_other_404 , "Visiteurs Uniques provenant de la Mauritanie et de l'étranger", False )

    sorted_and_trimed_countries = sort_and_trim_countries(countries )
    base64_string_countries = generate_base64_image(sorted_and_trimed_countries , "Visiteurs uniques par pays étranger", False)

    sorted_dates = sort_dates_keys(dates)
    base64_string_dates = generate_base64_image(sorted_dates , "Visiteurs uniques par mois ayant visité l'application pour la première fois", False)


    sorted_devices = dict(sorted(devices.items(), key=lambda item: item[1] ,  reverse=True)) 
    base64_string_devices = generate_base64_image(sorted_devices , "Visiteurs uniques par appareil", False)


    sorted_opearting_systems = dict(sorted(opearting_systems.items(), key=lambda item: item[1] ,  reverse=True))
    base64_string_opearting_systems = generate_base64_image(sorted_opearting_systems , "Visiteurs uniques par systèmes d'exploitation", False)

    
    #print(devices)   
    return JsonResponse({"mauritania_other_404": base64_string_mauritania_other_404 , "countries": base64_string_countries, "dates": base64_string_dates, "devices": base64_string_devices , "operating_systems": base64_string_opearting_systems}, safe=False)
    #return JsonResponse(devices, safe=False)

    #return JsonResponse({"uniqueVisitors": counter}, safe=False)
    #return JsonResponse(json_ads, safe=False)

def sort_and_trim_countries(countries: dict):

    del countries["Mauritania"]
    counter = 0
    for key in list(countries.keys()):

        if countries[key] < 50:
            counter = counter + countries[key]
            del countries[key]

    countries["Others"] = counter

    new_key = "UAE"
    old_key = "United Arab Emirates"
    countries[new_key] = countries.pop(old_key)


    new_key = "Hollande"
    old_key = "Netherlands"
    countries[new_key] = countries.pop(old_key)

    

    new_key = "UK"
    old_key = "United Kingdom"
    countries[new_key] = countries.pop(old_key)



    new_key = "RDC"
    old_key = "Republic of the Congo"
    countries[new_key] = countries.pop(old_key)

    new_key = "USA"
    old_key = "United States"
    countries[new_key] = countries.pop(old_key)

    new_key = "Saudi"
    old_key = "Saudi Arabia"
    countries[new_key] = countries.pop(old_key)

    sorted_countries= dict(sorted(countries.items(), key=lambda item: item[1] ,  reverse=True)) 

    return sorted_countries
    #return countries
    

def sort_countries(countries: dict):


    sorted_countries= dict(sorted(countries.items(), key=lambda item: item[1] ,  reverse=True)) 

    return sorted_countries

def populate_countries(country , countries):
        if country != "Mauritania":
            if  country in countries:
                countries[country] = countries[country] + 1
            else:
                countries[country] = 1


def populate_mauritania_other_404(country , mauritania_other_404):

        if country == "Mauritania":
            if  country in mauritania_other_404:
                mauritania_other_404[country] = mauritania_other_404[country] + 1
            else:
                mauritania_other_404[country] = 1

        elif country == "404":
            if  country in mauritania_other_404:
                mauritania_other_404[country] = mauritania_other_404[country] + 1
            else:
                mauritania_other_404[country] = 1
        else:
            if  "Abroad" in mauritania_other_404:
                mauritania_other_404["Abroad"] = mauritania_other_404["Abroad"] + 1
            else:
                mauritania_other_404["Abroad"] = 1
            

def populate_opearting_systems(opearting_systems , os):

        if os in opearting_systems:
            opearting_systems[os] = opearting_systems[os] + 1
        else:
            opearting_systems[os] = 1

def populate_devices(devices , device):
    if device in devices:
            devices[device] = devices[device] + 1
    else:
        devices[device] = 1

    
def sort_dates_keys(dates: dict):
    
    sorted_keys=sorted(dates.keys(), key=lambda x:x.lower())
    sorted_dates = {}

    for key in sorted_keys:
        sorted_dates[key] = dates[key]

    return sorted_dates


def populate_dates(visitDate , dates):

            split1 = visitDate.split(" ")
            split2 = split1[0].split("-")
            date = split2[0] + "-" + split2[1]

            if  date in dates:
                dates[date] = dates[date] + 1
            else:
                dates[date] = 1


def generate_base64_image(stats, title , rotate):

    x = list(stats.keys())
    y = list(stats.values())

    total = sum(y)

    """     x.insert(0, "Total")
    y.insert(0 , total ) """


    plt.subplots(figsize=(4, 4), dpi=100, tight_layout=True)
    plt.bar( x , y ,  color = "purple")


    #plt.bar(range(len(my_dict)), my_dict.values(), align='center')


    plt.figure(figsize=(15, 5))  # width:20, height:3
    plt.bar(x , y ,  color = "purple")

    plt.ylabel("Visiteurs Uniques" , weight='bold' ,  fontsize=12)

    mytimestamp = datetime.datetime.now()

    my_timestamp_trimmed = mytimestamp.strftime("%Y-%m-%d %H:%M:%S")
   
    plt.xlabel("Total = "+str(total)+"(100%) , timestamp : "+str(my_timestamp_trimmed), weight='bold' , fontsize=12) 
    plt.title(title , weight='bold',fontsize=12)

     
    
    for i in range(len(x)): 
        plt.text( i , y[i] ,  str(y[i]) +"\n(" +  str( float("{0:.1f}".format((y[i]/total) * 100)) )  + "%)" , ha="center" , va="bottom" )
    
    uniqueId = str(round(time.time() * 1000)) + "_"+str(random.randint(1, 10000))
    file = "./uploads/"+uniqueId+".png"

    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)

    plt.savefig(file)


    if rotate:
        image = Image.open(file)
        rotated_image = rotate_image(image, 270)
        rotated_image.save("./uploads/"+uniqueId+".png")


    """ image = Image.open(file)
    rotated_image = image.rotate(90)
    rotated_image.save(file) """
   


    with open(file, 'rb') as open_file:
        byte_content = open_file.read()

        # second: base64 encode read data
        # result: bytes (again)
    base64_bytes = b64encode(byte_content)

        # third: decode these bytes to text
        # result: string (in utf-8)
    base64_string = base64_bytes.decode('utf-8')
    os.remove(file)
    
    """ if os.path.exists(file):
        print("The file does exist")
        os.remove(file)

        if not(os.path.exists(file)):
            print("The file does not exist anymore")
        else:
            print("The file does not exist")  """


    return base64_string





def rotate_image(image, angle):
    """
    Rotates the given PIL Image object by the given angle without cropping sides.
    
    Args:
        image: The PIL Image object to rotate.
        angle: The angle to rotate the image by, in degrees.
        
    Returns:
        A new PIL Image object representing the rotated image.
    """


    if angle == 90:
        return image.transpose(Image.ROTATE_90)
    elif angle == 180:
        return image.transpose(Image.ROTATE_180)
    elif angle == 270:
        return image.transpose(Image.ROTATE_270)
    else:
        return image.rotate(angle, expand=True)


    # Convert the angle to radians
    radians = math.radians(angle)
    
    # Calculate the size of the rotated image
    width, height = image.size
    new_width = int(abs(width * math.cos(radians)) + abs(height * math.sin(radians)))
    new_height = int(abs(height * math.cos(radians)) + abs(width * math.sin(radians)))
    
    # Create a new image with the correct size and fill it with a white background
    new_image = Image.new('RGB', (new_width, new_height), (255, 255, 255))
    
    # Paste the rotated image onto the new image
    x_offset = (new_width - width) // 2
    y_offset = (new_height - height) // 2
    new_image.paste(image.rotate(angle, expand=True), (x_offset, y_offset))
    
    return new_image
# make api about countries regions and cities

""" db.statistics.aggregate([
  {
    $group: {
      _id: "$country",
      count: { $sum: 1 }
    }
  },
  {
    $group: {
      _id: null,
      unique_count: { $sum: 1 }
    }
  }
]) """