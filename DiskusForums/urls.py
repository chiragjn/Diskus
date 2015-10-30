from django.conf.urls import patterns, include, url
from django.contrib import admin
from Diskus import views
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static


admin.autodiscover()
urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.home, name='home'),
    url(r'^login/', views.login_user, name="login"),
    url(r'^register/', views.register_user, name="register"),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
    url(r'^forgot-password/$', views.forgot_password, name="forgot-password"),
    url(r'^verify/$', views.verify_user, name='verify_user'),
    url(r'^profile/(?P<slug>[\w-]+)/$', views.profile, name="profile"),
    url(r'^profile/(?P<slug>[\w-]+)/edit/$', views.profile_edit, name="profile-edit"),
    url(r'^category/(?P<slug>[\w-]+)/$', views.get_all_category_threads, name='category_threads'),
    url(r'^category/(?P<slug_cat>[\w-]+)/thread/(?P<slug_thread>[\w-]+)/$', views.get_thread, name='thread'),
    url(r'^category/(?P<slug_cat>[\w-]+)/thread/(?P<slug_thread>[\w-]+)/post/(?P<post_number>\d+)/rpost/(?P<relative_post_number>\d+)$', views.view_post, name='post'),
    url(r'^makepost/$', views.make_post, name='post_create'),
    url(r'^category/(?P<slug_cat>[\w-]+)/thread/(?P<slug_thread>[\w-]+)/editpost/(?P<post_number>\d+)$', views.edit_post, name='post_edit'),
    url(r'^category/(?P<slug_cat>[\w-]+)/thread/(?P<slug_thread>[\w-]+)/savepost/(?P<post_number>\d+)$', views.save_edited_post, name='post_save'),
    url(r'^new-thread/$', views.start_new_thread, name='thread_create_form'),
    url(r'^make-new-thread/$', views.post_new_thread, name='thread_object_create'),
    url(r'^category/(?P<slug_cat>[\w-]+)/thread/(?P<slug_thread>[\w-]+)/deletepost/(?P<post_number>\d+)$', views.delete_post, name='delete_post'),
    url(r'^add-category/$', views.add_category, name='add_category'),
]



#Don't really matter as we are now using Cling from dj-static
if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += patterns('', url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
                                'document_root': settings.MEDIA_ROOT, }),)
else:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(
       settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)