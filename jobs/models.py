from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils.text import slugify
import itertools
from django_countries.fields import CountryField


# User=get_user_model()
# Create your models here.



class CustomUser(AbstractUser):
    is_user = models.BooleanField(default=False)
    is_employer = models.BooleanField(default=False)
    email = models.EmailField(unique=True)

class Admin(models.Model):
    admin = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='images/')


    def __str__(self):
        return self.admin.username

class About(models.Model):
    STATUS = (
        ('True', 'True'),
        ('False','False'),
    )
    image = models.ImageField(blank=True, upload_to='images/')
    description = RichTextUploadingField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS, default='False')
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.status

class Testimonial(models.Model):
    fullname = models.CharField(blank=True, max_length=200)
    profession = models.CharField(blank=True, max_length=200)
    image = models.ImageField(blank=True, upload_to='images/')
    description = RichTextUploadingField(blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.fullname

class Team(models.Model):
    fullname = models.CharField(blank=True, max_length=200)
    image = models.ImageField(blank=True, upload_to='images/')
    specialty = models.CharField(blank=True, max_length=200)
    facebook = models.CharField(blank=True, max_length=200)
    twitter = models.CharField(blank=True, max_length=200)
    linkedin = models.CharField(blank=True, max_length=200)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.fullname

class Term(models.Model):
    title = models.CharField(max_length=3000)
    description = RichTextUploadingField(blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title


class Social(models.Model):
    facebook = models.CharField(blank=True, max_length=200)
    twitter = models.CharField(blank=True, max_length=200)
    behance = models.CharField(blank=True, max_length=200)
    linkedin = models.CharField(blank=True, max_length=200)
    url = models.URLField(blank=True, max_length=200)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.facebook

class Employer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # name = models.CharField(max_length=200, null=True)
    company_logo = models.ImageField(upload_to='images/')
    profile_pic = models.ImageField(upload_to='images/')
    phonenumber = models.CharField(blank=True, max_length=200)
    mobilenumber = models.CharField(blank=True, max_length=200)
    companyname = models.CharField(max_length=200)
    companyinfo = RichTextUploadingField(blank=True) 
    city = models.CharField(blank=True, max_length=200)
    website = models.CharField(blank=True, max_length=200)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.user.username

class Employee(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='images/', default="images/default.png")
    phonenumber = models.CharField(blank=True, max_length=200)
    profession = models.CharField(blank=True, max_length=200)


    def __str__(self):
        return self.user.username

class Category(models.Model):
    title=models.CharField(max_length=20)

    def __str__(self):
        return self.title

class Tag(models.Model):
    title=models.CharField(max_length=20)

    def __str__(self):
        return self.title

class Post(models.Model):
    title=models.CharField(max_length=100)
    overview=models.TextField()
    content = RichTextUploadingField()
    comment_count=models.IntegerField(default=0)
    view_count=models.IntegerField(default=0)
    author=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField()
    slug = models.SlugField( null=False, unique=True)
    categories = models.ManyToManyField(Category)
    tags = models.ManyToManyField(Tag)
    # featured = models.BooleanField()
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog-detail', kwargs ={
            'slug':self.slug
        })

    def _generate_slug(self):
        max_length = self._meta.get_field('slug').max_length
        value = self.title
        slug_candidate = slug_original = slugify(value, allow_unicode=True)
        for i in itertools.count(1):
            if not Post.objects.filter(slug=slug_candidate).exists():
                break
            slug_candidate = '{}-{}'.format(slug_original, i)

        self.slug = slug_candidate

    def save(self, *args, **kwargs):
        if not self.pk:
            self._generate_slug()

        super().save(*args, **kwargs)

    @property
    def get_comments(self):
        return self.comments.all().order_by('-timestamp')

    # @property
    # def get_comments1(self):
    #     return self.comments.filter(Comment.user.employer).order_by('-timestamp')
    
    @property
    def comment_count(self):
        return Comment.objects.filter(post=self).count()


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    timestamp=models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    post = models.ForeignKey('Post', related_name='comments', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class ContactFormMessage(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Read', 'Read'),
    )
    name = models.CharField(blank=True, max_length=50)
    email = models.CharField(blank=True, max_length=50)
    subject = models.CharField(blank=True, max_length=100)
    message = models.TextField(blank=True, max_length=555)
    status = models.CharField(max_length=20, choices=STATUS, default='New')
    ip = models.CharField(blank=True, max_length=20)
    note = models.CharField(blank=True, max_length=200)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'



class ContactInfo(models.Model):
    STATUS = (
        ('True', 'True'),
        ('False','False'),
    )
    phonenumber = models.PositiveIntegerField(blank=True)
    email = models.EmailField(max_length=50, blank=True)
    address = models.CharField(max_length=350)
    status = models.CharField(max_length=10, choices=STATUS)
    addressUrl = models.URLField(max_length=1200, blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return self.email 

    class Meta:
        verbose_name = 'Contact'
        verbose_name_plural = 'Contact'


class JobCategory(models.Model):
    title=models.CharField(max_length=1250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    class Meta:
        verbose_name = 'Job category'
        verbose_name_plural = 'Job category'

class Country(models.Model):
    country=models.CharField(max_length=750)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.country
    class Meta:
        verbose_name = 'Country'
        verbose_name_plural = 'Countries'
        
class Job(models.Model):
    TYPE = (
        ('Contract', 'Contract'),
        ('Internship', 'Internship'),
        ('Part time', 'Part time'),
    )
    WORKTYPE = (
        ('On-site', 'On-site'),
        ('Remote', 'Remote'),
        ('Hybrid', 'Hybrid'),
    )
    ELEVEL = (
        ('Not requested', 'Not requested'),
        ('Bachelor degre', 'Bachelor degre'),
        ('Master degree', 'Master degree'),
        ('PHD degree', 'PHD degree'),
    )
    EXXPERİENCE = (
        ('Not requested', 'Not requested'),
        ('Experience > 1', 'Experience > 1'),
        ('Experience > 3', 'Experience > 3'),
        ('Experience > 5', 'Experience > 5'),
    )
    jobtitle = models.CharField(max_length=500, verbose_name="Job title")
    salary = models.PositiveIntegerField()
    overview = models.CharField(max_length=2000)
    description = RichTextUploadingField(blank=True) 
    employer=models.ForeignKey(Employer, on_delete=models.CASCADE)
    type = models.CharField(max_length=500, choices=TYPE)
    worktype = models.CharField(max_length=500, choices=WORKTYPE)
    level = models.CharField(max_length=500, choices=ELEVEL)
    experience = models.CharField(max_length=500, choices=EXXPERİENCE)
    jobcategory = models.ForeignKey(JobCategory,on_delete=models.CASCADE)
    # country = models.ForeignKey(Country,on_delete=models.CASCADE)
    country = CountryField(blank_label='(select country)')
    slug = models.SlugField(null=False, unique=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.jobtitle

    def get_absolute_url(self):
        return reverse('job-detail', kwargs ={
            'slug':self.slug
        })
    def _generate_slug(self):
        max_length = self._meta.get_field('slug').max_length
        value = self.jobtitle
        slug_candidate = slug_original = slugify(value, allow_unicode=True)
        for i in itertools.count(1):
            if not Job.objects.filter(slug=slug_candidate).exists():
                break
            slug_candidate = '{}-{}'.format(slug_original, i)

        self.slug = slug_candidate

    def save(self, *args, **kwargs):
        if not self.pk:
            self._generate_slug()

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Job'
        verbose_name_plural = 'Jobs'



class Setting(models.Model):
    websitename=models.CharField(max_length=50, null=False, blank=False)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.websitename

class Subscribe(models.Model):
    email = models.EmailField(verbose_name="Email")
    timestamp = models.DateTimeField(auto_now_add=True,verbose_name="Subscribed time")

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Subscriber'
        verbose_name_plural = 'Subscribers'


class Application(models.Model):
    employee=models.ForeignKey(Employee, on_delete=models.CASCADE)
    job_id=models.ForeignKey(Job, on_delete=models.CASCADE)
    cv=models.FileField(verbose_name="Cv", blank=False)
    coverletter = models.TextField(verbose_name="Cover Letter",max_length=5000, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True,verbose_name="Applied time")

    def __str__(self):
        return self.employee.user.username

    class Meta:
        verbose_name = 'Application'
        verbose_name_plural = 'Applications'