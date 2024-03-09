from django.contrib import admin
from django.urls import path
from newsapi.views import login_view, logout_view, stories_view, delete_story_view  # Import the views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/login', login_view),  
    path('api/logout', logout_view), 
    path('api/stories', stories_view, name='stories_view'),
    path('api/stories/<int:key>', delete_story_view, name='delete_story_view'),
    
]
