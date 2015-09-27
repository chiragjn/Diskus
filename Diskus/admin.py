from django.contrib import admin
from models import *

# Register your models here.
admin.site.register(Member)
admin.site.register(Category)
admin.site.register(Thread)
admin.site.register(Post)
admin.site.register(Report)
admin.site.register(ImageUploads)