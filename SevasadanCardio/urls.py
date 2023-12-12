"""SevasadanCardio URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from application import views
from django.contrib.auth.decorators import login_required
# from . import views

urlpatterns = [
    # path('secure/', login_required(views.secure_view), name='secure_view'),
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('login', views.login, name='login'),
    path('admin_login', views.admin_login, name='admin_login'),
    path('register', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('admin_portal', views.admin_portal, name='admin_portal'),
    path('register_specialist', views.register_specialist, name='register_specialist'),
    path('register_lab_assistant', views.register_lab_assistant, name='register_lab_assistant'),
    path('lab_assistant_list', views.lab_assistant_list, name='lab_assistant_list'),
    path('specialist_home/<int:id>', views.specialist_home, name='specialist_home'),
    path('view_specialist_previous_reports/<int:id>', views.view_specialist_previous_reports, name='view_specialist_previous_reports'),
    path('view_assistant_previous_reports/<int:id>', views.view_assistant_previous_reports, name='view_assistant_previous_reports'),
    path('lab_assistant_home/<int:id>', views.lab_assistant_home, name='lab_assistant_home'),
    path('upload_success', views.upload_success, name='upload_success'),
    path('show_report/<int:report_id>/', views.show_report, name='show_report'),
    path('all_patient_list/', views.all_patient_list, name='all_patient_list'),
    path('about_us/', views.about_us, name='about_us'),
    path('contact_us/', views.contact_us, name='contact_us'),
]
