from django.urls import path
from . import views
from . import list
from . import timebox
from django.conf import settings
from django.conf.urls.static import static

# Define the path to different webpages. Represent the urls to different pages

urlpatterns = [
    path("", views.home, name="home"), #if we go to a homepage, where the path is default,
                                       # we're gonna view the view.index page that has a name of "index". view.index. index = function name
    path("<int:id>",views.todo, name="todo"), #the path is int we called it an id. That id is dynamic.
    path("todolist/", list.list, name="todolist"),
    path("timeboxing/", timebox.timebox, name="timeboxing"),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# path("<str:name>", views.idk, name="idk"),