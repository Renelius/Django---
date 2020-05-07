from django.urls import path, include, re_path
from .views import index, by_rubric, page_Bd,\
     MyRegisterUser, MyLogoutView, comment, user_activate,\
    profile, Bdcreate, editBd,deleteBd, searchBd, password_change, Mylogin

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('index', index, name='index'),
    path('<int:rubric_id>/', by_rubric, name='by_rubric'),
    path('add/', Bdcreate, name='add'),
    path('login', Mylogin, name='login'),
    path('register', MyRegisterUser.as_view(), name='register'),
    path('logout', MyLogoutView.as_view(), name='logout'),
    path('comment/<int:bd_id>', comment, name='comment'),
    path('check_email/<str:sign>', user_activate, name='check_email'),
    path('profile/<str:username>', profile, name='profile'),
    path('editBd/<int:bb_pk>', editBd, name='editBd'),
    path('deleteBd/<int:bb_pk>', deleteBd, name='deleteBd'),
    path('searchBd', searchBd, name='searchBd'),
    path('social/', include('social_django.urls', namespace='social')),
    path('password_change', password_change, name='password_change'),
    path('page_Bd/<int:bb_pk>', page_Bd, name='page_Bd'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)