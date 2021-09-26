from django.urls import path

from . import views

#Order is very important
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry>",views.entry,name="entry"),
    path("edit/<str:entry>",views.edit,name="edit"),
    path("search",views.search,name="search"),
    path("similar_entries",views.similar_entries,name="similar_entries"),
    path("new_entry",views.new_entry,name="new_entry"),
    path("save",views.succes,name="save"),
    path("save_edit",views.save_edit, name="save_edit"),
    path("random",views.random_entry,name="random"),
    path("<str:any>",views.non_existant,name="non_existant")#Don't change this path order in the list

]
