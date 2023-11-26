from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Tools(models.Model):
    name = models.CharField(max_length=200)
    img = models.ImageField(null=True, blank=True, upload_to="images/")

    def __str__(self):
        return self.name

class ToDoList(models.Model): #this class is inherited from models.Model. We're creating a database object
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True) # foreign key of class User in django.contrib.auth.models. access it through
    name = models.CharField(max_length=200) # name is the name of the attribute. Models.... is the name of the field that we want to store in database

    def __str__(self):
        return self.name #if we want to print, it will come out

class ToDoList_w(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True) # foreign key of class User in django.contrib.auth.models. access it through
    name = models.CharField(max_length=200)
    weekNum = models.CharField(max_length=200, default=0)

    def __str__(self):
        return self.name

class Item(models.Model):
    todolist = models.ForeignKey(ToDoList, on_delete=models.CASCADE) # define that we use a foreign key, which is ToDoList object when we create an item
                                                                     # if we delete ToDoList, we delete Item aswell. ToDoList is associated with many todolist object
    text = models.CharField(max_length=300) # Basically it's a string of data. #You need a max length
    complete = models.BooleanField()

    def __str__(self):
        return self.text
    
class Item_w(models.Model):
    todolist = models.ForeignKey(ToDoList_w, on_delete=models.CASCADE) # define that we use a foreign key, which is ToDoList object when we create an item
                                                                     # if we delete ToDoList, we delete Item aswell. ToDoList is associated with many todolist object
    text = models.CharField(max_length=300) # Basically it's a string of data. #You need a max length
    complete = models.BooleanField()
    
    def __str__(self):
        return self.text
    
class ListOfWeekNum(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    weekId = models.IntegerField()

    def __str__(self):
        return self.weekId
    
class TemplateList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True) # foreign key of class User in django.contrib.auth.models. access it through
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    
class TemplateItem(models.Model):
    todolist = models.ForeignKey(TemplateList, on_delete=models.CASCADE) # define that we use a foreign key, which is ToDoList object when we create an item
                                                                     # if we delete ToDoList, we delete Item aswell. ToDoList is associated with many todolist object
    text = models.CharField(max_length=300) # Basically it's a string of data. #You need a max length
    complete = models.BooleanField()
    
    def __str__(self):
        return self.text
    
class Images(models.Model):
    name = models.CharField(max_length=300, default="img")
    image = models.ImageField(null=True, blank=True, upload_to="images/")

    def __str__(self):
        return self.name


'''
source = https://docs.djangoproject.com/en/4.2/topics/db/examples/many_to_one/

t = ToDoList(name="first list")
t.save()
t2 = ToDoList(name="second list")
i = Item(id=None, todolist=t, text="wake up", complete=False)
i.save()
j = Item.objects.all()
j.save()
# t.item_set.all() #<Item: wake up>
# i.todolist = first list
# i.todolist.id = 1
# t.item_set.count() = 1
# Item.objects.all() #<Item: wake up>

t = i.todolist

- create new item in first list via the ToDoList object
new_item = t.item_set.create(text="take a shower", complete=False) 
# new_item = <Item: take a shower>
# new_item.todolist.id = 1
# new_item.todolist = first list

- create new item casually. Another way
new_item2 = Item.objects.create(text="brush a teeth", complete=False, todolist=t) 

- move an item to a different todolist set/ToDoList.
t2.item_set.add(new_item2)
# new_item2.todolist = <Item: second list>

- filtering
Item.objects.filter(todolist__name="first list") # item in first list
t.item_set.filter(text__startswith="wake") # item in first list that starts with "wake"

- Deleting #if ToDoList is deleted, the Item inside of that ToDolist is also deleted
t.delete()
del_object = t.get(id=1)
del_object.delete() #delete ToDoList


'''