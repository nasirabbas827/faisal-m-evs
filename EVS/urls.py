from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path


urlpatterns = [
    path('', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('change_password/', views.change_password, name='change_password'),
    path('logout/', views.user_logout, name='logout'),
    path('election/<int:election_id>/', views.view_election_details, name='election_details'),
    path('cast_vote/<int:election_id>/<int:candidate_id>/', views.cast_vote, name='cast_vote'),
    path('election_results/', views.election_results, name='election_results'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
