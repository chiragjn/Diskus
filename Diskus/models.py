from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from DiskusForums import settings
import itertools


class Member(models.Model):
    user = models.OneToOneField(User)
    profile_image_url = models.CharField(max_length=1000,blank=True, default=settings.STATIC_URL + "image/user.png")
    type = models.IntegerField(default=0)
    date_of_birth = models.DateField(auto_now=True, null=False)
    details_visible = models.BooleanField(default=True)
    bio = models.CharField(max_length=500, default=None)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.user.username)
        super(Member, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.user.username


class Category(models.Model):
    name = models.CharField(max_length=100, null=False)
    date = models.DateTimeField(auto_now_add=True, null=False)
    slug = models.SlugField(unique=True, blank=True)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        instance = self
        max_length = 50
        instance.slug = orig = slugify(instance.name)[:max_length]

        for x in itertools.count(1):
            if not Category.objects.filter(slug=instance.slug).exists():
                break
            # Truncate the original slug dynamically. Minus 1 for the hyphen.
            instance.slug = "%s-%d" % (orig[:max_length - len(str(x)) - 1], x)
        super(Category, self).save(*args, **kwargs)
        return instance


class Thread(models.Model):
    category = models.ForeignKey(Category, default=None)
    pinned = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
    op = models.ForeignKey(Member, related_name="op_set")
    moderator = models.ForeignKey(Member, null=True, blank=True , related_name="moderator_set")
    title = models.CharField(max_length=100, null=False)
    locked = models.BooleanField(default=False)
    visible = models.BooleanField(default=True)
    last_modified = models.DateTimeField(auto_now= True,blank= True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Thread, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.title


class Post(models.Model):
    author = models.ForeignKey(Member)
    thread = models.ForeignKey(Thread)
    date = models.DateTimeField(auto_now_add=True)
    content = models.TextField(null=False)
    visible = models.BooleanField(default=True)

    def __unicode__(self):
        return str(self.pk)

    def save(self, *args, **kwargs):
        self.thread.save()
        super(Post, self).save(*args, **kwargs)

class Report(models.Model):
    member = models.ForeignKey(Member)
    post = models.ForeignKey(Post)
    date = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=500, null=False)
    resolved = models.BooleanField(default=False)

    def __unicode__(self):
        return self.post.pk + " is reported by " + self.member.user.username


class ImageUploads(models.Model):
    img = models.ImageField(upload_to='pic_folder/', default='pic_folder/None/no-img.jpg')
    name = models.CharField(max_length=15, default=None)


# Create your models here.