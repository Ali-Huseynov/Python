
from django.urls import path, include
from .views import home,add_range

urlpatterns = [
    path("",  home , name="home"  ),
    path("add-range",  add_range , name="add_range"  )

]


