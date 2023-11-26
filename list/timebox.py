from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import ToDoList, Item, ToDoList_w, Item_w, ListOfWeekNum, TemplateList, TemplateItem, Images, Tools
from .timebox_models import Timebox, ItemSchedule, ItemGoal, ItemPriority, ListOfWeekNum_2, Quarterly_goal, Monthly_goal, Weekly_goal
from .form import *
from django.contrib.auth import get_user_model # get the user list
import time
import math
from .dayFuture import dayFuture


def timebox(response):
    tb = Timebox.objects.all()
    days = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
    result = time.localtime(time.time())
    img_plus = Images.objects.get(name="plus")
    this_week = math.ceil(result.tm_yday/7)
    quarterly_goal = Quarterly_goal.objects.all()
    monthly_goal = Monthly_goal.objects.all()
    weekly_goal = Weekly_goal.objects.all()
    
    # Function 
    def checkTheId(check):
        count = None
        for i in range(len(check)): #find the c
            if check[i].isalpha():
                count = i
                break
            if i == len(check)-1: #meaning i is in the end of the string
                count = len(check)
                break
        listId = check[:count]
        t = ToDoList.objects.get(id=int(listId)) 
        return t
    
    def checkTheIdWeekly(check):
        count = None
        for i in range(len(check)): #find the c
            if check[i].isalpha():
                count = i
                break
            if i == len(check)-1: #meaning i is in the end of the string
                count = len(check)
                break
        listId = check[:count]
        t = ToDoList_w.objects.get(id=int(listId)) 
        return t
    
    def checkItemId(check): #24c23            check = 23
        count = None
        for i in range(len(check)):
            if check[i].isalpha():
                count = i+1
        itemId = check[count:]
        return int(itemId)
        
    # Get a list of all weekNums
    listOfWeekNum_2 = []
    for i in ListOfWeekNum_2.objects.all():
        if not(i.weekId in ListOfWeekNum_2.objects.all()):
            listOfWeekNum_2.append(i.weekId)

    if response.method == "POST":

        form_w = CreateNewItem(response.POST) 
        form2_w = ChangeListName(response.POST)

        form_quarterly_goal = CreateQuarterlyGoal(response.POST)
        form_monthly_goal = CreateMonthlyGoal(response.POST)
        form_weekly_goal = CreateWeeklyGoal(response.POST) 
        form_goal = CreateNewItem(response.POST)
        form_priority = CreateNewItem(response.POST) 
        form_schedule = CreateNewItem(response.POST)
        form_time_schedule =CreateNewItem(response.POST) 
         
        
        # Create Weekly Timebox
        if form_monthly_goal.is_valid():
            if response.POST.get("create_monthly_goal"):
                if response.user.is_authenticated:
                    n = form_monthly_goal.cleaned_data["name"]
                    newGoal = Monthly_goal(name=n)
                    newGoal.save()

        if response.POST.get("create_template_tb"):
            weekId = result.tm_year*math.ceil(result.tm_yday/7) # currentYear * sortedWeekInAYear = sortedWeekSinceYear1 # 2023*29
            count2 = 0
            count3 = 0

            if Timebox.objects.filter(weekNum=weekId).count() == 0: #if this week's list is empty, create one
                for i in range(len(days)):
                    thisMonday = dayFuture(str(result.tm_mday)+"/"+str(result.tm_mon)+"/"+str(result.tm_year),-result.tm_wday) # get this week mondays"s date
                    listName = days[i]+" "+dayFuture(thisMonday,i)
                    li = Timebox(name=listName, user=response.user, weekNum=weekId)
                    li.save()
                    # for item in TemplateItem.objects.filter(todolist__name__startswith=days[i]): #all items in current template days
                    #     te = Item_w(text=item.text, todolist=listName, complete=False)
                    #     te.save()
                w = ListOfWeekNum_2(weekId=weekId, user=response.user)
                w.save()
            else: #else, create for another week
                while True:
                    count2 += result.tm_year
                    count3 += 1
                    if not(weekId+count2 in listOfWeekNum_2):
                        for i in range(len(days)):
                            thisMonday = dayFuture(str(result.tm_mday)+"/"+str(result.tm_mon)+"/"+str(result.tm_year),7*count3-result.tm_wday) # get this week mondays"s date
                            listName = days[i]+" "+dayFuture(thisMonday,i)
                            li = Timebox(name=listName, user=response.user, weekNum=weekId)
                            li.save()
                        w = ListOfWeekNum_2(weekId=weekId+count2, user=response.user)
                        w.save()
                        break

        # Delete all Weekly Timebox
        if response.POST.get("delete_all_tb_week"):
            Timebox.objects.filter(user=response.user).delete()
            ListOfWeekNum_2.objects.filter(user=response.user).delete()
            listOfWeekNum_2.clear()
            # deleteList = response.user.todolist_set.all()
            # deleteList.delete()

        # Create Quarterly_Goals
        if form_quarterly_goal.is_valid():
            if response.POST.get("create_quarterly_goal"):
                n = form_quarterly_goal.cleaned_data["name"]
                newgoal = Quarterly_goal(name=n, user=response.user)
                newgoal.save()

        # delete Quarterly_Goals
        if response.POST.get("delete_quarterly_goal"):
            deleteGoal = Quarterly_goal(id=response.POST.get("delete_quarterly_goal"), user=response.user)
            deleteGoal.delete()          

        # Create Monthly_Goals
        if form_monthly_goal.is_valid():
            if response.POST.get("create_monthly_goal"):
                n = form_monthly_goal.cleaned_data["name"]
                newgoal = Monthly_goal(name=n, user=response.user)

        # delete Monthly_Goals
        if response.POST.get("delete_monthly_goal"):
            deleteGoal = Monthly_goal(id=response.POST.get("delete_monthly_goal"), user=response.user)
            deleteGoal.delete()
                
        # delete itemGoal weekly todolist
        if response.POST.get("deleteItemGoal_week"):
            t = checkTheIdWeekly(response.POST.get('deleteItem_week')[6:])
            for i in t.itemGoal_w_set.all():
                if response.POST.get("deleteItem_week") == "delete"+str(t.id)+"c"+str(i.id):
                    t.itemGoal_w_set.get(id=i.id).delete() #use id instead of text because there can be many Item that have the same text.

        
        # delete list weekly timebox
        if response.POST.get("delete_tb_week"):
            deleteList = Timebox(id=response.POST.get("delete_ls_week"), user=response.user)
            deleteList.delete()

        # change tb name weekly timebox
        if form2_w.is_valid():
            if response.POST.get("change_tb_week"): 
                n = form2_w.cleaned_data["name"]
                oldlist = checkTheIdWeekly(response.POST.get("change_tb_week"))
                oldlist_id = oldlist.id
                oldlist.delete()
                newlist = Timebox(name=n, id=oldlist_id, user=response.user)
                newlist.save()

         # create New ItemGoal Weekly ToDoList
        if form_w.is_valid():# the form is going to get the data from response.POST and we access the data by using a dictionary.
            if response.POST.get('newItem_week'):
                t = checkTheIdWeekly(response.POST.get('newItem_week')[6:])
                n = form_w.cleaned_data["name"] # We get that data & use it to create a new ToDoList. name is the input of the label/Charfield in form.py
                t.itemGoal_w_set.create(text=n, complete=False).save() #Everytime we create a data that is valid (according to the input requirements) 
    
        # save item weekly todolist
        # def save_week(list_id):
        #     if response.POST.get("save_week") == list_id:
        #         # for key, value in response.POST.items():
        #         #     if value.startswith("save") == True:
        #         #         list_id = value[4:]

        #         for item in Item_w.objects.all():
        #             item_id = item.id
        #             if list_id == str(item.todolist.id): # list_id = item.todolist.id = response.POST.get("save")  # Last line of code that I wrote
        #                 if response.POST.get(str(list_id)+"c"+str(item_id)) == "clicked_week":
        #                     item.complete = True
        #                 else:
        #                     item.complete = False
        #                 item.save()

        # if response.POST.get("save_week"):
        #     save_week(response.POST.get("save_week"))
        
        return HttpResponseRedirect('/timeboxing/')

    
    form_w = CreateNewItem() 
    form2_w = ChangeListName()
    form_quarterly_goal = CreateQuarterlyGoal()
    form_monthly_goal = CreateMonthlyGoal()
    form_weekly_goal = CreateWeeklyGoal() 
    form_goal = CreateNewItem()
    form_priority = CreateNewItem() 
    form_schedule = CreateNewItem()
    form_time_schedule =CreateNewItem() 
    
    return render(response, "main/timebox.html", {"tb":tb, "quarterly_goal":quarterly_goal, "monthly_goal":monthly_goal, "weekly_goal":weekly_goal, "form_w":form_w, "form2_w":form2_w, "this_week":this_week, "form_quarterly_goal":form_quarterly_goal, "form_monthly_goal":form_monthly_goal, "form_weekly_goal":form_weekly_goal, "form_goal":form_goal, "form_priority":form_priority, "form_schedule":form_schedule, "form_time_schedule":form_time_schedule,})