from django.conf.urls import patterns,include, url
from django.contrib import admin
from Diskus import views

admin.autodiscover()
urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.home, name='home'),
    url(r'^login/', views.login_user, name="login"),
    url(r'^register/', views.register_user, name="register"),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
    url(r'^forgot-password/$', views.forgot_password, name="forgot-password"),
    url(r'^profile/(?P<slug>[\w-]+)/$', views.profile, name="profile"),
    url(r'^category/(?P<slug>[\w-]+)/$', views.get_all_category_threads, name='category_home'),
    url(r'^category/(?P<slug_cat>[\w-]+)/thread/(?P<slug_thread>[\w-]+)/$', views.get_thread, name='category_home'),
    url(r'^makepost/$', views.make_post, name='post_create'),
    url(r'^new-thread/$', views.start_new_thread, name='thread_create_form'),
    url(r'^make-new-thread/$', views.post_new_thread, name='thread_create')



]


from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()  # this serves static files and media files.
    # in case media is not served correctly
    urlpatterns += patterns('',
                            url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
                                'document_root': settings.MEDIA_ROOT, }),)
else:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
