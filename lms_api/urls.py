from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.landing_page, name='landing'),
    path('login.html/', views.signup_page, name='login'),
    path('signup.html/', views.signup_page, name='signup'),
    path('courses/', views.courses_page, name='courses'),
    path('courses/detail/', views.course_detail_page, name='course_detail'),
    path('lectures/detail/', views.lecture_detail_page, name='lecture_detail'),
    path('assignments/detail/', views.assignment_detail_page, name='assignment_detail'),
    path('admin/', admin.site.urls),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('api/v1/accounts/', include('modules.accounts.urls')),
    path('api/v1/courses/', include('modules.courses.urls')),
    path('api/v1/lectures/', include('modules.lectures.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
