from django.urls import path
from rest_framework.views import APIView
from . import views
from .views import RdvApi, RdvDetailsApi,AdministreDetailsApi,EvenementAPi,RdvByUserApi,Logout
from rest_framework.authtoken import views


urlpatterns = [
    #path('article/', views.article_list ),
    #path('article/', ArticleApi.as_view()),
    path('login/',views.obtain_auth_token),
    path('logout/',Logout.as_view()),
    path('viewset/rdv/', RdvApi.as_view()),
    path('viewset/evenements/', EvenementAPi.as_view()),
    #path('article/detail/<int:id>', views.RdvDetailsApi), 
    path('viewset/rdv/<int:id>', RdvDetailsApi.as_view() ),
    path('viewset/rdv/administre/<int:id>', RdvByUserApi.as_view() ),
    path('viewset/administre/<int:id>', AdministreDetailsApi.as_view() ),
]