from django.conf.urls import url
from views import *
from django.views.static import serve

urlpatterns=[
    url(r'^home/$',home,name='home'),
    url(r'^market/(\d+)/(\d+)/(\d+)/$',market, name='market'),
    url(r'^cart/$', cart, name='cart'),
    url(r'^mine/$', mine, name='mine'),
    url(r'^login/$',login,name='login'),
    url(r'^register/$',register,name='register'),
    url(r'^checkuserid/$',checkuserid,name='checkuserid'),
    url(r'^quit/$',quit,name='quit'),
    url(r'changecart/(\d+)/',changecart,name='changecart'),
    url(r'saveorder/$',saveorder,name='saveorder'),
    url(r'media/(.*)',serve,{'document_root':os.path.join(settings.BASE_DIR,'static/media')}),
    url(r'^allchoice/$',allchoice,name='allchoice'),
]