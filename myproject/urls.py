"""myproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


from boards import views
from django.urls import path
from django.conf import settings
from django.contrib import admin
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.views.generic.base import TemplateView 
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [

    # URL for root  ('/')
    path('', TemplateView.as_view(template_name='home.html'), name='root'),

    # URL for "/admin"
    url('admin/', admin.site.urls),

    # URL for Signup
    path('signup/', views.signup, name='signup'),

    # URLs for login and logout
    path('accounts/', include('django.contrib.auth.urls')),

    # URL for "account_activation_sent/" and thus go to views.Home() in viws.$
    path('verification/',  views.verifyEmail, name='verification'),

    # URL to activate the email confirmation of user and thus go to views.activate in views.py
    path('activate/<uidb64>/<token>/',views.activateUser, name='activate'),

    # URL for good login page
    path('login/', TemplateView.as_view(template_name='index.html'), name='log'),

    # URL for '/automation/' to automate the appliances
    path('automation/', views.autoPage, name='automation'),

    # URL for actuation of aplliances
    path(r'automation/<appliance>/<action>/', views.auto, name='automation'),


]+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

