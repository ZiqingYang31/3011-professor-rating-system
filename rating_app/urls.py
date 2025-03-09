
from django.urls import path
from .views import (
    RegisterView, LoginView, ModuleInstanceListView,
    ProfessorRatingListView, ProfessorAverageRatingView, RatingCreateView
)
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"), 
    path("login/", LoginView.as_view(), name="login"),  
    path('api-token-auth/', obtain_auth_token, name='api-token-auth'),
    path("module-instances/", ModuleInstanceListView.as_view(), name="module-instances"),  
    path("professors/ratings/", ProfessorRatingListView.as_view(), name="professor-ratings"),  
    path("professors/<str:professor_id>/modules/<str:module_code>/average/", ProfessorAverageRatingView.as_view(), name="professor-average-rating"),
    path("ratings/", RatingCreateView.as_view(), name="rating-create"), 
]