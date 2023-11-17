from django.shortcuts import render
from django.http import JsonResponse,HttpResponseRedirect
from .database import Database
import os
import requests

def home_page(request) -> render:
    return render(request , "index.html")


def ConnectDatabase():
        # environment variables
        data = {
            "DATABASE_HOST": os.environ['DATABASE_HOST'],
            "DATABASE_USER": os.environ['DATABASE_USER'],
            "DATABASE_NAME": os.environ['DATABASE_NAME'],
            "DATABASE_PASSWORD": os.environ['DATABASE_PASSWORD'],
            "SECRET_KEY": os.environ['SECRET_KEY'],
        }
        # database_obj = Database(
        #     host = constants.DATABASE_HOST,
        #     user = constants.DATABASE_USER,
        #     password = constants.DATABASE_PASSWORD,
        #     database_ = constants.DATABASE_NAME,
        # )
        database_obj = Database(
            host = data['DATABASE_HOST'],
            user = data['DATABASE_USER'],
            password = data['DATABASE_PASSWORD'],
            database_ = data['DATABASE_NAME']
        )
        database_obj.connect()
        return database_obj


def Upload_To_Database(link) -> bool:
        database_obj = ConnectDatabase()
        database_obj.insert(table_name='video_links',
                            table_headers=['link'],
                            values=[link])
        database_obj.commit_and_disonnect() 
        return True  



def AddLink(request) -> home_page:
    if request.method == 'POST':
        link = request.POST.get("insta_link")
        Upload_To_Database(link)
        return HttpResponseRedirect('/')


def FetchLink(request) -> dict:  
    database_obj = ConnectDatabase()
    try:
        response = database_obj.fetch_first_row("video_links")[0]
        database_obj.delete_first_row("video_links")
        database_obj.commit_and_disonnect() 
        if response:
            data = {
                "status" : True,
                "response" : response,
            }
            return JsonResponse(data)
    except Exception as E:
        database_obj.commit_and_disonnect()
        print(E)
        data = {
            "status" : False,
        }
        return JsonResponse(data)

def download_remaining(request):
    site = "PRIVATE URL : NOT FOR PUBLIC"

    response = requests.get(site)
    if response.status_code == 200:
        return HttpResponseRedirect("/")
    else:
        response = {
            'status':False,
            'errro':'website did not respond'
        }
        return JsonResponse(response)

def view_remaining(request):
    site = "PRIVATE URL : NOT FOR PUBLIC"
    
    response = requests.get(site)
    if response.status_code == 200:
        return JsonResponse(response.json())
    else:
        response = {
            'status':False,
            'errro':'website did not respond'
        }
        return JsonResponse(response)
    
    


