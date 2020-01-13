from django.conf.urls import url,include
from .import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns=[
url(r'^signup/',views.signup,name='signup'),
url(r'^$',views.home,name='Home',),
url(r'^timeline/',views.index,name='Index'),
url(r'^profile/(\d+)',views.first_profile,name='Profile'),
url(r'^images/',views.add_image,name='Image'),
url(r'^search/',views.search_profile, name='Search'),
url(r'^nav/(\d+)',views.nav,name='Nav'),



]
if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
