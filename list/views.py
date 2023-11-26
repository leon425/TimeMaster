from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import ToDoList, Item, ToDoList_w, Item_w, ListOfWeekNum, TemplateList, TemplateItem, Images, Tools
from .timebox_models import Timebox, ItemSchedule, ItemGoal, ItemPriority, ListOfWeekNum_2
from .form import CreateNewList, ChangeListName, CreateNewItem
from django.contrib.auth import get_user_model # get the user list
import time
import math
from .dayFuture import dayFuture



def index(response):
    ls = ToDoList.objects.get(id=1)  # get the object in database

    # if response.method == "POST": # the dict: {"save":["save"], "c1":[""],}
    #     pass

    return render(response,"main/base2.html", {"ls":ls})

def home(response):
    tools = Tools.objects.all()
    return render(response, "main/home.html", {"tools":tools,})

def todo(response,id): # parameter id is from the url.
    ls = ToDoList.objects.get(id=id)  # get the object in database
    item = ls.item_set.get(id=1)

    return HttpResponse("<h1>%s</h1><br></br><p>%s</p>" %(ls.name, str(item.text))) #display the name of ToDoList object that has the id according to the url page.
    # If we go to urlpage 1/, we'll get Tim's List and item of Tim's List with the id of 1.
    # return HttpResponse("<h1>%s<h1>" % id) # display the number in the webpage according to the id. #First step to display dinamic pages