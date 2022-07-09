from django.contrib import admin
from django.urls import path, include
from authentication import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('authentication.urls')),
    path('useradmin/',views.showadmin, name = 'showadmin'),
    path('delete/<int:id>',views.delete,name='delete'),
    path('<int:id>',views.update,name='update'),
]
