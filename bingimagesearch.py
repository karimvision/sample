# bing image grabber using bing api
# note that the limit if 5000 queries per month, anything beyong that is not free
# try using different queries for each 500 images like press conference soccer, press conference real madrid, etc

from bing_search_api import BingSearchAPI
import urllib
import socket
import sys
import os
# set this timeout to prevent long download times
from socket import timeout
socket.setdefaulttimeout(3)

# ACCOUNT KEY can be found in the bing developer site under Account information tab
# https://datamarket.azure.com/dataset/5BA839F1-12CE-4CCE-BF57-A49D98D29A44
my_key = "DKlYIGGFAm2nPBu9ACSBIAvulMATwoAey53ceP87f6o"

#get input params
query_string = raw_input("Enter the query:")
image_count = raw_input("Enter the image count: ")

#check if image_count is an integer
try:
    image_count=int(image_count)
except ValueError:
    print "The image count must be an integer"
    sys.exit(-1)

#check if image_count lies within a range of 1 to 1000, you can change this upper limit
r=range(1,500)
if image_count not in r:
    print "the image count must be between 1 to 500"
    sys.exit(-1)

download_path = raw_input("Enter the full Download Path: ")
# check download path and create directory
if os.path.exists(download_path):
    #the path is there
    pass
elif os.access(os.path.dirname(download_path), os.W_OK):
    #the path does not exists but write privileges are given, make directory
    os.makedirs(download_path)
else:
    #can not write there
    print "invalid file path or it does not have write privileges"
    sys.exit(-1)

#use the bing container to grab images
bing = BingSearchAPI(my_key)

# see https://msdn.microsoft.com/en-us/library/dd560913.aspx for more filters
params = {'ImageFilters':'""', # e.g 'ImageFilters':'"Face:Face"'
          '$format': 'json',
          '$top': image_count,
          '$skip': 0}
bingJson = bing.search('image',query_string,params).json() # use image+web to get both image and web results
results_list = bingJson['d']['results'][0]['Image']

#download image from the results list, count increments the index in the results list, fileCount denotes the total number of files in the save path
count=0
fileCount=0
#make seperate directory for each query to group data
save_path = download_path+"/"+query_string+"/"
if not os.path.exists(save_path):
    os.makedirs(save_path)
else:
    #if the path exists start downlading from the largest index of files, this will keep the old images
    path, dirs, files = os.walk(save_path).next()
    fileCount=len(files)


for result in results_list:
    if count>=fileCount:
        print "Downloading " +result['MediaUrl'] + " ....."
        # catch the timeout exception while downloading image from image url
        try:
         urllib.urlretrieve(result['MediaUrl'] ,save_path+query_string+(count).__str__() + ".jpg")
        except Exception,e:
         print 'caught an exceptiom downloading image failed :('

    count+=1