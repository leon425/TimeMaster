from django.contrib import admin
from .models import ToDoList, Item, ToDoList_w, Item_w, ListOfWeekNum, TemplateList, TemplateItem, Images, Tools
# from .timebox_models import Timebox, ItemSchedule, ItemGoal, ItemPriority, ListOfWeekNum_2
from .timebox_models import *

# Register your models here.

admin.site.register(ToDoList)
admin.site.register(Item)
admin.site.register(ToDoList_w)
admin.site.register(Item_w)
admin.site.register(ListOfWeekNum)
admin.site.register(TemplateList)
admin.site.register(TemplateItem)
admin.site.register(Images)
admin.site.register(Tools)
admin.site.register(Timebox)
admin.site.register(ItemSchedule)
admin.site.register(ItemGoal)
admin.site.register(ItemPriority)
admin.site.register(ListOfWeekNum_2)
admin.site.register(Quarterly_goal)
admin.site.register(Monthly_goal)
admin.site.register(Weekly_goal)