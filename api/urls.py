from django.urls import re_path
from api import views 
 
urlpatterns = [ 
    re_path(r'^api/tutorials$', views.tutorial_list),
    re_path(r'^api/create_ad$', views.create_ad),



    re_path(r'^api/getAds$', views.getsAds),

    re_path(r'^api/getAdDetails$', views.getAdDetails),
    re_path(r'^api/getAdsNearMe$', views.getAdsNearMe),
    re_path(r'^api/updateAd$', views.updateAd),
    re_path(r'^api/deleteAd$', views.deleteAd),
    re_path(r'^api/login$', views.login),
    re_path(r'^api/getSomething$', views.getSomething),

    re_path(r'^api/getMachineLearning$', views.getMachineLearning ),
    re_path(r'^api/getUniqueVisitorsCount$', views.getUniqueVisitorsCount),
    
    re_path(r'^api/getUniqueVisitorsOfAllTime$', views.getUniqueVisitorsOfAllTime ),

    re_path(r'^api/getCountriesForLast24Hours$', views.getCountriesForLast24Hours ),
    




    re_path(r'^api/getVisistsCountLast24Hours$', views.getVisistsCountLast24Hours ),
    re_path(r'^api/getUniqueVisitorsThatVisitedForTheFirstTimeEverInTheLast30Days$', views.getUniqueVisitorsThatVisitedForTheFirstTimeEverInTheLast30Days ),
    re_path(r'^api/getUniqueVisitorsThatVisitedForTheFirstTimeEverInTheLast24Hours$', views.getUniqueVisitorsThatVisitedForTheFirstTimeEverInTheLast24Hours ),
    re_path(r'^api/getUniqueVisitorsLast24Hours$', views.getUniqueVisitorsLast24Hours ),
    re_path(r'^api/getUniqueVisitorsLast30Days$', views.getUniqueVisitorsLast30Days ),
    
    re_path(r'^api/getAllCountries$', views.getAllCountries ),
    re_path(r'^api/getUniqueVisitorsFromAndFromOutsideMauritania$', views.getUniqueVisitorsFromAndFromOutsideMauritania ),
    re_path(r'^api/getGraphs$', views.getGraphs ),
    re_path(r'^api/getRegionsOfCountry$', views.getRegionsOfCountry ),
    re_path(r'^api/getCitiesOfRegion$', views.getCitiesOfRegion ),

    re_path(r'^api/getUniqueVisitorsPerMonth$', views.getUniqueVisitorsPerMonth ),
    re_path(r'^api/getUniqueVisitorsPerOs$', views.getUniqueVisitorsPerOs ),
    re_path(r'^api/getUniqueVisitorsPerDevice$', views.getUniqueVisitorsPerDevice ),
    re_path(r'^api/getUniqueVisitorsPerCountry$', views.getUniqueVisitorsPerCountry ),
    re_path(r'^api/getUniqueVisitorsPerRegion$', views.getUniqueVisitorsPerRegion ),
    re_path(r'^api/getUniqueVisitorsPerCity$', views.getUniqueVisitorsPerCity ),




    #re_path(r'^api/extractTextFromPdf$', views.extractTextFromPdf ),
    

    
]

 