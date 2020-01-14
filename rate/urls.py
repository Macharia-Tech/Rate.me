from django.conf.urls import url,include
from .import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views  as auth_views  

urlpatterns=[
 
    url(r'^register/',views.register, name='register'),
    url(r'', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    url(r'^logout/', auth_views.LogoutView.as_view(), name='logout'),
    url(r'^project/(\d+)',views.single_project,name='project'),
    url(r'^add/project$', views.add_project, name='add-project'),
    url(r'^new/profile$', views.new_profile, name='new-profile'),
    url(r'displayprofile/(?P<user_id>\d+)$',views.display_profile,name='displayprofile'),
    url(r'^api/merch/$', views.ProjectList.as_view())  
  



]
if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
