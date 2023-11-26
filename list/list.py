from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import ToDoList, Item, ToDoList_w, Item_w, ListOfWeekNum, TemplateList, TemplateItem, Images, Tools
from .timebox_models import Timebox, ItemSchedule, ItemGoal, ItemPriority, ListOfWeekNum_2
from .form import CreateNewList, ChangeListName, CreateNewItem
from django.contrib.auth import get_user_model # get the user list
import time
import math
from .dayFuture import dayFuture

def list(response):
    ls = ToDoList.objects.all()
    lw = ToDoList_w.objects.all()
    days = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
    weekly_todolist = False
    normal_todolist = False
    result = time.localtime(time.time())
    img_plus = Images.objects.get(name="plus")

    # Get a list of all weekNums
    listOfWeekNum = []
    for i in ListOfWeekNum.objects.all():
        if not(i.weekId in ListOfWeekNum.objects.all()):
            listOfWeekNum.append(i.weekId)

    # defining the ToDoList objects based on the form of ToDoList.objects.all().  #response.POST.get('newItem')[6:] == "submit{{list.id}}c{{i.id}}" == "submit24c23"   pretend that response.POST..... is the argument
    if ToDoList.objects.all() != None:
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
        
    #Check the existence of weekly todolist & normal todolist
    if ls.count() != 0:
        normal_todolist = True
    if lw.count() != 0:
        weekly_todolist = True
    
    if response.method == "POST": #check if the response works. (The declaration of the methods is in the list.html <form> tag)
        form = CreateNewItem(response.POST)  #all information from the form contains dictionary of all different attributes,
                                             # all different inputs. All the values you type are going to be saved in them.
                                             # So, it will create a new form that has values poputlated in them.
        form2 = ChangeListName(response.POST)
        form3 = CreateNewList(response.POST)

        form_w = CreateNewItem(response.POST) 
        form2_w = ChangeListName(response.POST)

        # Create new ToDoList
        if form3.is_valid():
            if response.POST.get("create_ls"):
                if response.user.is_authenticated == True: # if user is logged in
                    n = form3.cleaned_data["name"]
                    newList = ToDoList(name=n, user=response.user)
                    newList.save()

        # create New Item Weekly ToDoList
        if form_w.is_valid():# the form is going to get the data from response.POST and we access the data by using a dictionary.
            if response.POST.get('newItem_week'):
                t = checkTheIdWeekly(response.POST.get('newItem_week')[6:])
                n = form_w.cleaned_data["name"] # We get that data & use it to create a new ToDoList. name is the input of the label/Charfield in form.py
                t.item_w_set.create(text=n, complete=False).save() #Everytime we create a data that is valid (according to the input requirements) , we create a new Item

        # Create new Item Normal ToDoList
        if form.is_valid():# the form is going to get the data from response.POST and we access the data by using a dictionary.
            if response.POST.get('newItem'):
                t = checkTheId(response.POST.get('newItem')[6:])
                n = form.cleaned_data["name"] # We get that data & use it to create a new ToDoList. name is the input of the label/Charfield in form.py
                t.item_set.create(text=n, complete=False).save() #Everytime we create a data that is valid (according to the input requirements) , we create a new Item

        # Before, the weekId is int(str(result.tm_year)+str(math.ceil(result.tm_yday/7))). (202352). 'currentYear' + 'sortedWeekInAYear'

        # Create Weekly ToDoList
        if response.POST.get("create_template_ls"):
            weekId = result.tm_year*math.ceil(result.tm_yday/7) # currentYear * sortedWeekInAYear = sortedWeekSinceYear1 # 2023*29
            count2 = 0
            count3 = 0

            if ToDoList_w.objects.filter(weekNum=weekId).count() == 0: #if this week's list is empty, create one
                for i in range(len(days)):
                    thisMonday = dayFuture(str(result.tm_mday)+"/"+str(result.tm_mon)+"/"+str(result.tm_year),-result.tm_wday) # get this week mondays"s date
                    listName = days[i]+" "+dayFuture(thisMonday,i)
                    li = ToDoList_w(name=listName, user=response.user, weekNum=weekId)
                    li.save()
                    for item in TemplateItem.objects.filter(todolist__name__startswith=days[i]): #all items in current template days
                        te = Item_w(text=item.text, todolist=listName, complete=False)
                        te.save()
                w = ListOfWeekNum(weekId=weekId, user=response.user)
                w.save()
            else: #else, create for another week
                while True:
                    count2 += result.tm_year
                    count3 += 1
                    if not(weekId+count2 in listOfWeekNum):
                        for i in range(len(days)):
                            thisMonday = dayFuture(str(result.tm_mday)+"/"+str(result.tm_mon)+"/"+str(result.tm_year),7*count3-result.tm_wday) # get this week mondays"s date
                            listName = days[i]+" "+dayFuture(thisMonday,i)
                            li = ToDoList_w(name=listName, user=response.user, weekNum=weekId)
                            li.save()
                        w = ListOfWeekNum(weekId=weekId+count2, user=response.user)
                        w.save()
                        break
                      
        # Get Weekly Template 
        if response.POST.get("templateWeek"):
            TemplateList.objects.all().delete()
            # get name
            tw = ToDoList_w.objects.filter(weekNum=response.POST.get("templateWeek"))
            for list in tw:
                li = TemplateList(name=list.name, user=response.user)
                li.save()
                for item in list.item_w_set.all():
                    # it = TemplateItem(text=item.text, todolist=list.name, complete=False)
                    li.templateitem_set.create(text=item.text, complete=False).save()
                    # it.save()


        # Delete all Normal ToDoList
        if response.POST.get("delete_all_list"):
            ToDoList.objects.filter(user=response.user).delete()
            # deleteList = response.user.todolist_set.all()
            # deleteList.delete()
        
        # Delete all Weekly ToDoList
        if response.POST.get("delete_all_list_week"):
            ToDoList_w.objects.filter(user=response.user).delete()
            ListOfWeekNum.objects.filter(user=response.user).delete()
            listOfWeekNum.clear()
            # deleteList = response.user.todolist_set.all()
            # deleteList.delete()
        

        # save item Normal Todolist
        def save(list_id):
            if response.POST.get("save") == list_id:
                # for key, value in response.POST.items():
                #     if value.startswith("save") == True:
                #         list_id = value[4:]

                for item in Item.objects.all():
                    item_id = item.id
                    if list_id == str(item.todolist.id): # list_id = item.todolist.id = response.POST.get("save")  # Last line of code that I wrote
                        if response.POST.get(str(list_id)+"c"+str(item_id)) == "clicked":
                            item.complete = True
                        else:
                            item.complete = False
                        item.save()

        if response.POST.get("save"):
            save(response.POST.get("save"))
        # saving the complete/incomplete item is manual (you need to press the save button). If you want to do it automatically (save the complete without
        # pressing the save button), you have to switch the checkbox value & name like the deleteItem. Then, the code is the same with the deleteItem.

        # save item weekly todolist
        def save_week(list_id):
            if response.POST.get("save_week") == list_id:
                # for key, value in response.POST.items():
                #     if value.startswith("save") == True:
                #         list_id = value[4:]

                for item in Item_w.objects.all():
                    item_id = item.id
                    if list_id == str(item.todolist.id): # list_id = item.todolist.id = response.POST.get("save")  # Last line of code that I wrote
                        if response.POST.get(str(list_id)+"c"+str(item_id)) == "clicked_week":
                            item.complete = True
                        else:
                            item.complete = False
                        item.save()

        if response.POST.get("save_week"):
            save_week(response.POST.get("save_week"))

        # delete item normal todolist
        if response.POST.get("deleteItem"):
            t = checkTheId(response.POST.get('deleteItem')[6:])
            for i in t.item_set.all():
                if response.POST.get("deleteItem") == "delete"+str(t.id)+"c"+str(i.id):
                    t.item_set.get(id=i.id).delete() #use id instead of text because there can be many Item that have the same text.

        # delete item weekly todolist
        if response.POST.get("deleteItem_week"):
            t = checkTheIdWeekly(response.POST.get('deleteItem_week')[6:])
            for i in t.item_w_set.all():
                if response.POST.get("deleteItem_week") == "delete"+str(t.id)+"c"+str(i.id):
                    t.item_w_set.get(id=i.id).delete() #use id instead of text because there can be many Item that have the same text.

        # change list name normal todolist
        if form2.is_valid():
            if response.POST.get("change_ls"): 
                # t_id = int(response.POST.get("change_ls")) #ToDoList id
                print("hey")
                n = form2.cleaned_data["name"]
                oldlist = checkTheId(response.POST.get("change_ls"))
                oldlist_id = oldlist.id
                oldlist.delete()
                newlist = ToDoList(name=n, id=oldlist_id, user=response.user)
                newlist.save()
            
        # change list name weekly todolist
        if form2_w.is_valid():
            if response.POST.get("change_ls_week"): 
                n = form2_w.cleaned_data["name"]
                oldlist = checkTheIdWeekly(response.POST.get("change_ls_week"))
                oldlist_id = oldlist.id
                oldlist.delete()
                newlist = ToDoList_w(name=n, id=oldlist_id, user=response.user)
                newlist.save()

        # delete list normal todolist
        if response.POST.get("delete_ls"):
            deleteList = ToDoList(id=response.POST.get("delete_ls"), user=response.user)
            deleteList.delete()

        # delete list weekly todolist
        if response.POST.get("delete_ls_week"):
            deleteList = ToDoList_w(id=response.POST.get("delete_ls_week"), user=response.user)
            deleteList.delete()

        return HttpResponseRedirect('/todolist/') # To avoid "Form resubmission"

    # else:
    #     form = CreateNewItem()
    #     form2 = ChangeListName()
    #     form3 = CreateNewList()
    #     form_w = CreateNewItem() 
    #     form2_w = ChangeListName()


    form = CreateNewItem() # create a blank form and pass it to html. Must define it again
    form2 = ChangeListName()
    form3 = CreateNewList()
    form_w = CreateNewItem() 
    form2_w = ChangeListName()

    return render(response, "main/list.html", {"ls":ls, "lw":lw, "form":form, "form2":form2, "form3":form3, "form_w":form_w, "form2_w":form2_w, "weekly_todolist":weekly_todolist, "normal_todolist":normal_todolist, "img_plus":img_plus,}) #write all the forms here, or the form won't be render and sent to list.html

