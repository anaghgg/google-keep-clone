from . import views
from django.urls import path

app_name='api'

urlpatterns=[
    path('notes-list',views.notes_list,name="noteslist"),
    path('add-note',views.add_note,name="addnote"),
    path('edit-note/<str:pk>',views.edit_note,name="editnote"),
    path('user',views.get_user,name="user"),
]
