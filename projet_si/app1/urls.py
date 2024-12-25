from django.contrib import admin

from django.urls import path,include

from . import views


from django.urls import path, include
urlpatterns = [ 
  path('app1/', include('app1.urls')),
  path('admin/', admin.site.urls),  # Django admin site URL
  path('', views.home, name='home'),  # Default URL for the application
  path('list_employes/',views.afficher_employes),
]