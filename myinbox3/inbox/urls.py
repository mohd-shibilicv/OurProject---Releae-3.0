from django.contrib import admin
from django.urls import path, include
from inbox import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('App.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    # path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/reset_done.html'), name='password_reset_done'),
    # path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="registration/reset_confirm.html"), name='password_reset_confirm'),
    # path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/reset_complete.html'), name='password_reset_complete'),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

handler500 = 'App.views.E_500'
handler404 = 'App.views.E_404'