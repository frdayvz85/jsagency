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
from cloudinary_storage.storage import RawMediaCloudinaryStorage


# User=get_user_model()
# Create your models here.



class CustomUser(AbstractUser):
    is_user = models.BooleanField(default=False)
    is_employer = models.BooleanField(default=False)
    email = models.EmailField(unique=True)

class Admin(models.Model):
    admin = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Admin")
    profile_pic = models.ImageField(upload_to='images/', verbose_name="Profile image")


    def __str__(self):
        return self.admin.username

class About(models.Model):
    STATUS = (
        ('True', 'True'),
        ('False','False'),
    )
    image = models.ImageField(blank=True, upload_to='images/')
    description = RichTextUploadingField(blank=True, verbose_name="Description")
    status = models.CharField(max_length=10, choices=STATUS, default='False')
    created_date = models.DateTimeField(auto_now_add=True,verbose_name="Created date")
    updated_date = models.DateTimeField(auto_now=True, verbose_name="Updated date")
    
    def __str__(self):
        return self.status

class Testimonial(models.Model):
    fullname = models.CharField(blank=True, max_length=200, verbose_name="Full name")
    profession = models.CharField(blank=True, max_length=200, verbose_name="Profession")
    image = models.ImageField(blank=True, upload_to='images/', verbose_name="Image")
    description = RichTextUploadingField(blank=True, verbose_name="Description")
    created_date = models.DateTimeField(auto_now_add=True,verbose_name="Created date")
    updated_date = models.DateTimeField(auto_now=True, verbose_name="Updated date")
    
    def __str__(self):
        return self.fullname

class Team(models.Model):
    fullname = models.CharField(blank=True, max_length=200, verbose_name="Fullname")
    image = models.ImageField(blank=True, upload_to='images/', verbose_name="Image")
    specialty = models.CharField(blank=True, max_length=200, verbose_name="Speciality")
    facebook = models.CharField(blank=True, max_length=200, verbose_name="Facebook")
    twitter = models.CharField(blank=True, max_length=200, verbose_name="Twitter")
    linkedin = models.CharField(blank=True, max_length=200, verbose_name="Linkedin")
    created_date = models.DateTimeField(auto_now_add=True,verbose_name="Created date")
    updated_date = models.DateTimeField(auto_now=True, verbose_name="Updated date")
    
    def __str__(self):
        return self.fullname

class Term(models.Model):
    title = models.CharField(max_length=3000, verbose_name="Title")
    description = RichTextUploadingField(blank=True, verbose_name="Description")
    created_date = models.DateTimeField(auto_now_add=True,verbose_name="Created date")
    updated_date = models.DateTimeField(auto_now=True, verbose_name="Updated date")
    
    def __str__(self):
        return self.title


class Employer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="User")
    company_logo = models.ImageField(upload_to='images/', verbose_name="Company logo")
    profile_pic = models.ImageField(upload_to='images/', verbose_name="Profile image")
    phonenumber = models.CharField(blank=True, max_length=200, verbose_name="Phone number")
    mobilenumber = models.CharField(blank=True, max_length=200, verbose_name="Mobile number")
    companyname = models.CharField(max_length=200, verbose_name="Company name")
    companyinfo = RichTextUploadingField(blank=True, verbose_name="Company information") 
    city = models.CharField(blank=True, max_length=200, verbose_name="City")
    website = models.CharField(blank=True, max_length=200, verbose_name="Website")
    create_at = models.DateTimeField(auto_now_add=True,verbose_name="Created date")
    update_at = models.DateTimeField(auto_now=True, verbose_name="Updated date")


    def __str__(self):
        return self.user.username

class Employee(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="User")
    profile_pic = models.ImageField(upload_to='images/', default="images/default.png", verbose_name="Profile image")
    phonenumber = models.CharField(blank=True, max_length=200, verbose_name="Phone number")
    profession = models.CharField(blank=True, max_length=200, verbose_name="Profession")


    def __str__(self):
        return self.user.username

class Category(models.Model):
    title=models.CharField(max_length=20, verbose_name="Title")

    def __str__(self):
        return self.title

class Tag(models.Model):
    title=models.CharField(max_length=20, verbose_name="Title")

    def __str__(self):
        return self.title

class Post(models.Model):
    title=models.CharField(max_length=100, verbose_name="Title")
    overview=models.TextField(verbose_name="Overview")
    content = RichTextUploadingField(verbose_name="Content")
    comment_count=models.IntegerField(default=0, verbose_name="Comment count")
    view_count=models.IntegerField(default=0, verbose_name="View count")
    author=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Author")
    image = models.ImageField(verbose_name="Image")
    slug = models.SlugField( null=False, unique=True, verbose_name="Slug")
    categories = models.ManyToManyField(Category, verbose_name="Categories")
    tags = models.ManyToManyField(Tag, verbose_name="Tags")
    # featured = models.BooleanField()
    created_date = models.DateTimeField(auto_now_add=True,verbose_name="Created date")
    updated_date = models.DateTimeField(auto_now=True, verbose_name="Updated date")

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
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="User")
    timestamp=models.DateTimeField(auto_now_add=True,verbose_name="Created date")
    content = models.TextField(verbose_name="Content")
    post = models.ForeignKey('Post', related_name='comments', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class ContactFormMessage(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Read', 'Read'),
    )
    name = models.CharField(blank=True, max_length=50, verbose_name="Name")
    email = models.CharField(blank=True, max_length=50, verbose_name="Email")
    subject = models.CharField(blank=True, max_length=100, verbose_name="Subject")
    message = models.TextField(blank=True, max_length=555, verbose_name="Message")
    status = models.CharField(max_length=20, choices=STATUS, default='New', verbose_name="Status")
    ip = models.CharField(blank=True, max_length=20, verbose_name="IP")
    note = models.CharField(blank=True, max_length=200, verbose_name="Note")
    create_at = models.DateTimeField(auto_now_add=True,verbose_name="Created date")
    update_at = models.DateTimeField(auto_now=True, verbose_name="Updated date")

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
    phonenumber = models.PositiveIntegerField(blank=True, verbose_name="Phone number")
    email = models.EmailField(max_length=50, blank=True, verbose_name="Email")
    address = models.CharField(max_length=350, verbose_name="Address")
    status = models.CharField(max_length=10, choices=STATUS, verbose_name="Status")
    addressUrl = models.URLField(max_length=1200, blank=True, verbose_name="Address url")
    create_at = models.DateTimeField(auto_now_add=True,verbose_name="Created date")
    update_at = models.DateTimeField(auto_now=True, verbose_name="Updated date")
    

    def __str__(self):
        return self.email 

    class Meta:
        verbose_name = 'Contact'
        verbose_name_plural = 'Contact'


class JobCategory(models.Model):
    title=models.CharField(max_length=1250, verbose_name="Title")
    created_at = models.DateTimeField(auto_now_add=True,verbose_name="Created date")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated date")

    def __str__(self):
        return self.title
    class Meta:
        verbose_name = 'Job category'
        verbose_name_plural = 'Job category'

class Country(models.Model):
    country=models.CharField(max_length=750)
    created_at = models.DateTimeField(auto_now_add=True,verbose_name="Created date")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated date")

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
    salary = models.PositiveIntegerField(verbose_name="Salary")
    overview = models.CharField(max_length=2000, verbose_name="Overview")
    description = RichTextUploadingField(blank=True, verbose_name="Description") 
    employer=models.ForeignKey(Employer, on_delete=models.CASCADE, verbose_name="Employer")
    type = models.CharField(max_length=500, choices=TYPE, verbose_name="Type")
    worktype = models.CharField(max_length=500, choices=WORKTYPE, verbose_name="Work type")
    level = models.CharField(max_length=500, choices=ELEVEL, verbose_name="Level")
    experience = models.CharField(max_length=500, choices=EXXPERİENCE, verbose_name="Experience")
    jobcategory = models.ForeignKey(JobCategory,on_delete=models.CASCADE, verbose_name="Job category")
    # country = models.ForeignKey(Country,on_delete=models.CASCADE)
    country = CountryField(blank_label='(select country)')
    slug = models.SlugField(null=False, unique=True, verbose_name="Slug")
    create_at = models.DateTimeField(auto_now_add=True,verbose_name="Created date")
    update_at = models.DateTimeField(auto_now=True, verbose_name="Updated date")


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
    create_at = models.DateTimeField(auto_now_add=True,verbose_name="Created date")
    update_at = models.DateTimeField(auto_now=True, verbose_name="Updated date")

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
    # cv=models.FileField(verbose_name="Cv", blank=False,storage=RawMediaCloudinaryStorage())
    coverletter = models.TextField(verbose_name="Cover Letter",max_length=5000, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True,verbose_name="Applied time")

    def __str__(self):
        return self.employee.user.username

    class Meta:
        verbose_name = 'Application'
        verbose_name_plural = 'Applications'
    

class Social(models.Model):
    facebook = models.URLField(blank=True, max_length=500,verbose_name="Facebook")
    twitter = models.URLField(blank=True, max_length=500,verbose_name="Twitter")
    linkedin = models.URLField(blank=True, max_length=500,verbose_name="Linkedin")
    instagram = models.URLField(blank=True, max_length=500,verbose_name="Instagram")
    youtube = models.URLField(blank=True, max_length=500,verbose_name="Youtube")
    email = models.EmailField(blank=True, max_length=200,verbose_name="Email")
    created_date = models.DateTimeField(auto_now_add=True,verbose_name="Created date")
    updated_date = models.DateTimeField(auto_now=True,verbose_name="Updated date")
    
    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Social'
        verbose_name_plural = 'Socials'

class Intro(models.Model):
    image = models.ImageField(verbose_name="Image", blank=True, null=True)
    overview = models.TextField(verbose_name="Overview",max_length=700, blank=True, null=True)
    description = models.TextField(verbose_name="Description",max_length=2000, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True,verbose_name="Applied time")

    def __str__(self):
        return self.overview

    class Meta:
        verbose_name = 'Intro'
        verbose_name_plural = 'Intro'