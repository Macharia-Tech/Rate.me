from django.conf.urls import url,include
from .import views
from django.conf import settings
from django.conf.urls.static import static
from . import views 

urlpatterns=[
 
    url('^$',views.home,name='home'),
    url(r'^search/',views.search_title,name='search_title'),
    url(r'^project/(\d+)',views.single_project,name='project'),
    url(r'^add/project$', views.add_project, name='add-project'),
    url(r'^new/profile$', views.new_profile, name='new-profile'),
    url(r'^rate$',views.add_rating,name='rate'),
    url(r'displayprofile/(?P<user_id>\d+)$',views.display_profile,name='displayprofile'),
    url(r'^api/profile/$', views.ProfileList.as_view()),
    url(r'^api/project/$', views.ProjectList.as_view()),
    
    
  



]
if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
