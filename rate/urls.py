from django.conf.urls import url,include
from .import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views  as auth_views  

urlpatterns=[
    url(r'^admin/', admin.site.urls),
    url(r'',include('rate.urls'))
    url(r'^register/',views.register, name='register'),
    url(r'', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    url(r'^logout/', auth_views.LogoutView.as_view(), name='logout'),  
  



]
if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
