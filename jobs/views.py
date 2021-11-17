from django.db.models import Q, Count
from django.shortcuts import render, redirect,get_object_or_404, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
import hashlib
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import authenticate, login, logout
from .forms import CommentForm, SignUpForm, ContactFormu, PostForm,JobForm,UserForm,AdminForm,EmployerForm,ApplicationFormu, EmployeeForm,SignUpFormEmployer,PasswordChangeForm
from django.contrib.auth.models import Group
from .models import *
from django.views.generic import CreateView
from django.utils.text import slugify
from .decorators import unauthenticated_user, allowed_users, admin_only
from datetime import datetime, timedelta
from django.utils import timezone
# from .filters import JobFilter
# from user.forms import UserProfileForm


# Create your views here.
def get_author(user):
    qs = Employee.objects.filter(user=user)
    if qs.exists():
        return qs[0]
    return None

def get_employer(user):
    qs = Employer.objects.filter(user=user)
    if qs.exists():
        return qs[0]
    return None
def get_type_count():
    querysetType = Job \
        .objects \
        .values('type') \
        .annotate(Count('type'))
    return querysetType
def get_worktype_count():
    querysetType = Job \
        .objects \
        .values('worktype') \
        .annotate(Count('worktype'))
    return querysetType

def get_experience_count():
    querysetExperience = Job \
        .objects \
        .values('experience') \
        .annotate(Count('experience'))
    return querysetExperience

def get_level_count():
    querysetLevel = Job \
        .objects \
        .values('level') \
        .annotate(Count('level'))
    return querysetLevel
def get_category_count():
    querysetCategory = Job \
        .objects \
        .values('jobcategory') \
        .annotate(Count('jobcategory'))
    return querysetCategory

def search(request):
    recent_posts = Post.objects.all().order_by('-created_date')[:3]
    categories = Category.objects.all()
    queryset = Post.objects.all()
    query = request.GET.get('q')
    if query:
        queryset = queryset.filter(
            Q(title__icontains=query) |
            Q(overview__icontains=query)
        ).distinct()

    context = {
        'queryset': queryset,
        'recent_posts':recent_posts,
        'categories':categories,
    }
    return render(request, 'mainpages/search-results.html', context)
def home(request):
    testimonials = Testimonial.objects.all().order_by('-id')
    # featured = Post.objects.filter(featured=True).order_by('-created_date')[0:3]
    #auto delete
    Job.objects.filter(create_at__lte=datetime.now()-timedelta(days=21)).delete()
    last_three = Post.objects.all().order_by('-created_date')[:3]
    comments = Comment.objects.all()
    comment_count = comments.count()
    popular_jobs = Job.objects.all().order_by('-id')[:5]
    last_three_job = Job.objects.all().order_by('-id')[:3]
    intros = Intro.objects.all().order_by('-id')

    # subscribe
    if request.method == 'POST':
        email = request.POST["subscribemail"]
        new_signup = Subscribe()
        new_signup.email = email
        if request.user.is_authenticated:
            messages.error(request, "You are registered that is why you can't subscribe. Thanks!")
            return redirect('/')
        new_signup.save()
        messages.success(request, 'You are subscribed. Thanks')
        return redirect('/')

    context = {
        'last_three':last_three, 
        'last_three':last_three,
        'comment_count':comment_count,
        'last_three_job':last_three_job,
        'popular_jobs':popular_jobs,
        'testimonials':testimonials,
        'intros':intros,
        }
    return render(request, 'mainpages/index.html', context)

def aboutUs(request):
    abouts = About.objects.get(pk=1)
    context = {'abouts':abouts}
    return render(request, 'mainpages/about-us.html', context)

# def foot(request):
#     footers = Social.objects.get(pk=1)
#     context = {'footers':footers}
#     return render(request, 'mainpages/footer.html', context)    

def testimonial(request):
    testimonials = Testimonial.objects.all()
    context = {'testimonials':testimonials}
    return render(request, 'mainpages/testimonials.html', context)

def team(request):
    teams = Team.objects.all()
    context = {'teams':teams}
    return render(request, 'mainpages/team.html',context)

def author(request):
    authors = Employee.objects.all()
    context = {'authors':authors}
    return render(request, 'mainpages/author.html',context)

def term(request):
    terms = Term.objects.all()
    context = {'terms':terms}
    return render(request, 'mainpages/terms.html', context)

def blog(request):
    posts = Post.objects.all()
    recent_posts = Post.objects.all().order_by('-created_date')[:3]
    tags = Tag.objects.all()
    tag_count = tags.count()
    categories = Category.objects.all()
    category_count = categories.count()
    # comments = Comment.objects.all()
    # comment_count = comments.count()

    paginator = Paginator(posts, 2)
    page_request_var = 'page'
    page = request.GET.get(page_request_var)
    try:
        paginated_queryset = paginator.page(page)
    except PageNotAnInteger:
        paginated_queryset = paginator.page(1) 
    except EmptyPage:
        paginated_queryset = paginator.page(paginator.num_pages)  

    
    popular_posts = Post.objects.all().order_by('-view_count')[:3]

    context = {
        'tags':tags,
        'categories':categories,
        'recent_posts':recent_posts,
        'popular_posts':popular_posts,
        # 'comment_count':comment_count,
        'category_count':category_count,
        'tag_count':tag_count,
        'queryset': paginated_queryset,
        'page_request_var': page_request_var,
        }
    return render(request, 'mainpages/blog-posts.html', context)

def blogDetail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    recent_posts = Post.objects.all().order_by('-created_date')[:3]
    popular_posts = Post.objects.all().order_by('-view_count')[:3]
    # comments = Comment.objects.filter(post=slug)
    # comment_count = comments.count()
    p = Comment.objects.order_by('timestamp').last()
    form = CommentForm(request.POST or None)
    print(p)
    post.view_count = post.view_count + 1
    post.save()
    
    if request.method == "POST":
        if form.is_valid():
            form.instance.user =request.user
            form.instance.post = post
            form.save()
            messages.success(request, "Your comment has been added succesfully. Thank you")
            return redirect(reverse("blog-detail", kwargs={
                'slug':post.slug
        }))

    context = {
        'post':post,
        'recent_posts':recent_posts,
        'popular_posts':popular_posts,
        # 'comments':comments,
        # 'comment_count':comment_count,
        'form':form
        }
    return render(request, 'mainpages/blog-post-details.html', context)

@login_required(login_url='login')
def blogCreate(request):
    title='Create'
    form = PostForm(request.POST or None, request.FILES or None)
    author = get_author(request.user)
    if request.method == "POST":
        if form.is_valid():
            form.instance.author = request.user
            form.save()
            messages.success(request, "Your Blog has been created succesfully. Thank you")
            return redirect(reverse("blog-detail", kwargs={
                'slug':form.instance.slug
            }))
    context = {
        'title':title,
        'form':form,
    }
    return render(request, 'mainpages/blog-create.html', context)

@login_required(login_url='login')
def blog_update(request, slug):
    title='Update'
    post = get_object_or_404(Post, slug=slug)
    form = PostForm(
        request.POST or None, 
        request.FILES or None, 
        instance=post)
    author = get_author(request.user)
    if request.method == "POST":
        if form.is_valid():
            form.instance.author = request.user
            form.save()
            messages.success(request, "Your Blog has been updated succesfully.")
            return redirect(reverse("blog-detail", kwargs={
                'slug':form.instance.slug
            }))
    context = {
        'title': title,
        'form':form,
        'post':post,
    }

    return render(request, 'mainpages/blog-create.html', context)

@login_required(login_url='login')
def blog_delete(request, slug):
    post = get_object_or_404(Post, slug=slug)
    post.delete()
    return redirect(reverse("blog"))



# @login_required(login_url='login')
# def userProfile(request):
#     user = request.user
#     form = EmployeeForm(instance=user)
#     context = {
#         'form':form,
#     }
#     return render(request, 'mainpages/employee-profile.html', context)

@login_required(login_url='login')
def userProfile(request):
    author = request.user.employee
    # form = EmployeeForm(instance=author)
    if request.method == 'POST':             #form post edildiyse
        form = EmployeeForm(request.POST, request.FILES, instance=author)
        userForm = UserForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid() and userForm.is_valid():
            form.save()   #veritabanina kaydet
            userForm.save() 
            messages.success(request, "Your Profile has been updated succesfully.")
            return HttpResponseRedirect('employee-profile')
    else:
        form = EmployeeForm(instance=author)
        userForm = UserForm(instance=request.user)
    context = {
        'form':form,
        'userForm':userForm,
    }
    return render(request, 'mainpages/employee-profile.html', context)

def contact(request):
    if request.method == 'POST':             #form post edildiyse
        form = ContactFormu(request.POST)
        if form.is_valid():
            data = ContactFormMessage()            # model ile baglanti kur
            data.name = form.cleaned_data['name']  #formdan bilgiyi al
            data.email = form.cleaned_data['email']
            data.subject = form.cleaned_data['subject']
            data.message = form.cleaned_data['message']
            data.ip = request.META.get('REMOTE_ADDR') #client computer ip address
            data.save()   #veritabanina kaydet
            messages.success(request, "Your Message has been sent succesfully. Thank you")
            return HttpResponseRedirect('contact')


    form = ContactFormu()

    contactInfo = ContactInfo.objects.get(pk=1)
    context = {'form':form, 'contactInfo':contactInfo}
    return render(request, 'mainpages/contact.html', context)

def registerUser(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = SignUpForm()
        if request.method =='POST':
            form = SignUpForm(request.POST)
            if form.is_valid():
                user = form.save()
                user.is_user=True 
                form.save()

                Employee.objects.create(
				        user=user
				)

                user = form.cleaned_data.get('username')
                messages.success(request, 'Profile was created succesfully for ' + user )
                return redirect('login')
                
    context = {'form':form}
    return render(request, 'mainpages/employee-register.html', context)

def registerType(request):
    return render(request, 'mainpages/registertype.html')

def registerEmployer(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = SignUpForm()
        profile_form = SignUpFormEmployer(request.POST)
        if request.method =='POST':
            form = SignUpForm(request.POST)
            profile_form = SignUpFormEmployer(request.POST or None)
            if form.is_valid() and profile_form.is_valid():
                user = form.save()
                user.is_employer=True
                user.save()
                profile = profile_form.save(commit=False)
                profile.user=user
                profile.save()
                
                user = form.cleaned_data.get('username')
                messages.success(request, 'Profile was created succesfully for ' + user )
                return redirect('login')
                
    context = {
        'form':form,
        'profile_form':profile_form
        }
    return render(request, 'mainpages/employer-register.html',context)

@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/')  #also can be redirect
        else:
            messages.info(request, 'Username or Password is wrong, please check again!')

    context = {}
    return render(request, 'mainpages/login.html', context)



def logoutUser(request):
    logout(request)
    return redirect('login')



@login_required(login_url='/login/')
def password_change(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('/')
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request,'accounts/password_change.html',{'form':form})




# for search 
def is_valid_queryparam(param):
    return param != '' and param is not None



def jobs(request):
    qs = Job.objects.all().order_by('-create_at')
    categories = JobCategory.objects.all()
    type_counts = get_type_count()
    worktype_counts = get_worktype_count()
    expereince_counts = get_experience_count()
    level_counts = get_level_count()
    category_counts = get_category_count()

    #auto delete
    Job.objects.filter(create_at__lte=datetime.now()-timedelta(days=21)).delete()

    # myFilter = JobFilter(request.GET, queryset=alljob)
    # alljob = myFilter.qs
    type = request.GET.get('type')
    worktype = request.GET.get('worktype')
    level = request.GET.get('level')
    experience = request.GET.get('experience')
    category = request.GET.get('category')

    if is_valid_queryparam(type):
        qs = qs.filter(type=type)

    if is_valid_queryparam(worktype):
        qs = qs.filter(worktype=worktype)

    if is_valid_queryparam(level):
        qs = qs.filter(level=level)
    
    if is_valid_queryparam(experience):
        qs = qs.filter(experience=experience)

    if is_valid_queryparam(category) and category != 'Choose...':
        qs = qs.filter(jobcategory__title=category)

    paginator = Paginator(qs, 4)
    page_request_var = 'page'
    page = request.GET.get(page_request_var)
    try:
        paginated_queryset = paginator.page(page)
    except PageNotAnInteger:
        paginated_queryset = paginator.page(1) 
    except EmptyPage:
        paginated_queryset = paginator.page(paginator.num_pages)

    context = {
        'queryset': paginated_queryset,
        'page_request_var': page_request_var,
        'type_counts':type_counts,
        'expereince_counts':expereince_counts,
        'level_counts':level_counts,
        'category_counts':category_counts,
        'worktype_counts':worktype_counts,
        'categories':categories,
    }
    return render(request, 'mainpages/job-listing.html', context)

def jobDetail(request, slug):
    jobs = get_object_or_404(Job, slug=slug)
    appliedJobs =Application.objects.filter(employee_id=request.user.employee, job_id_id=jobs.id).order_by('-timestamp')
    appliedJobss =Application.objects.all().order_by('-timestamp')
    print(appliedJobs)
    print(appliedJobss)
    # recent_jobs = Job.objects.all().order_by('-create_at')[:3]
    # user = request.user
    # form = EmployerForm(instance=user)
    # employer = get_object_or_404(Employer)
    # employer = Employer.objects.filter(name = request.user.first_name +" "+ request.user.last_name)
    
    form = ApplicationFormu()
    if request.method == 'POST':
        form = ApplicationFormu(request.POST, request.FILES or None )
        form1 = JobForm(request.POST or None, request.FILES or None)
        employee = get_author(request.user)
        if form.is_valid():
            apply=form.save(commit=False)
            apply.job_id =jobs
            form.instance.employee = employee
            form.save()
            messages.success(request, "Your have applied succesfully!")
            return redirect('/job-detail/'+jobs.slug)
        else:
            messages.error(request, "Something went wrong, Try again later!")
            return redirect("/")
            

    # form = ApplicationFormu(request.POST or None, request.FILES or None )
    # employee = get_author(request.user)
    # if request.method == "POST":
    #     if form.is_valid():
    #         apply = form.save()
    #         apply.job_id = jobs
    #         form.instance.employee = employee
    #         form.save()
    #         # Application.objects.create(
	# 		# 	        user=employee
	# 		# 	)
    #         messages.success(request, "Your Job has been created succesfully. Thank you")
    #         return redirect('/')
    #     else:
    #         messages.error(request, "Errrrroooooorrr")
    #         return redirect('/')

    context = {
        'jobs':jobs,
        # 'employer':employer,
        'form':form,
        'appliedJobs':appliedJobs,
        }

    return render(request, 'mainpages/job-details.html', context)


@login_required(login_url='login')
def jobCreate(request):
    title='Create'
    form = JobForm(request.POST or None, request.FILES or None)
    employer = get_employer(request.user)
    if request.method == "POST":
        if form.is_valid():
            job = form.save(commit=False)
            job.slug = slugify(job.jobtitle)
            form.instance.employer = employer
            form.save()
            messages.success(request, "Your Job has been created succesfully. Thank you")
            return redirect(reverse("job-detail", kwargs={
                'slug':form.instance.slug
            }))
    context = {
        'title':title,
        'form':form,
    }
    return render(request, 'mainpages/job-create.html', context)

@login_required(login_url='login')
def job_update(request, slug):
    title='Update'
    post = get_object_or_404(Job, slug=slug)
    form = JobForm(
        request.POST or None, 
        request.FILES or None, 
        instance=post)
    employer = get_employer(request.user)
    if request.method == "POST":
        if form.is_valid():
            job = form.save(commit=False)
            job.slug = slugify(job.jobtitle)
            form.instance.employer = employer
            form.save()
            messages.success(request, "Your Job has been updated succesfully.")
            return redirect(reverse("job-detail", kwargs={
                'slug':form.instance.slug
            }))
    context = {
        'title': title,
        'form':form,
        'post':post,
    }

    return render(request, 'mainpages/job-create.html', context)

@login_required(login_url='login')
def job_delete(request, slug):
    job = get_object_or_404(Job, slug=slug)
    job.delete()

    return redirect(reverse("jobs"))

# login_required(login_url='login')
# def employerProfile(request):
#     user = request.user
#     form = EmployerForm(instance=user)
#     context = {
#         'form':form,
#     }
#     return render(request, 'mainpages/employer-profile.html', context)

@login_required(login_url='login')
def employerProfile(request):
    # userForm = UserForm(instance=request.user)
    employer = request.user.employer
    # form = EmployerForm(instance=employer)
    if request.method == 'POST':             #form post edildiyse
        form = EmployerForm(request.POST, request.FILES, instance=employer)
        userForm = UserForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid() and userForm.is_valid():
            form.save() 
            userForm.save()  #veritabanina kaydet
            messages.success(request, "Your Profile has been updated succesfully.")
            return HttpResponseRedirect('employer-profile')
    else:
        form = EmployerForm(instance=employer)
        userForm = UserForm(instance=request.user)
    context = {
        'form':form,
        'userForm':userForm
    }
    return render(request, 'mainpages/employer-profile.html', context)

@login_required(login_url='login')
def adminProfile(request):
    admin = request.user.admin
    # form = EmployeeForm(instance=author)
    if request.method == 'POST':             #form post edildiyse  
        form = AdminForm(request.POST, request.FILES, instance=request.user.admin)
        userForm = UserForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid() and userForm.is_valid():
            form.save()   #veritabanina kaydet
            userForm.save() 
            messages.success(request, "Your Profile has been updated succesfully.")
            return HttpResponseRedirect('admin-profile')
    else:
        form = AdminForm(instance=request.user.admin)
        userForm = UserForm(instance=request.user)
    context = {
        'userForm':userForm,
        'form': form,
    }
    return render(request, 'mainpages/admin-profile.html', context)



def sharedJobs(request):
    jobs = Job.objects.filter(employer_id=request.user.employer).order_by('-create_at')
    print(jobs)
    context = {
        'jobs':jobs
    }
    return render(request, 'mainpages/shared-jobs.html', context)


def appliedJobs(request):
    jobs = Application.objects.filter(employee_id=request.user.employee).order_by('-timestamp')
    print(jobs)
    context = {
        'jobs':jobs
    }
    return render(request, 'mainpages/applied-jobs.html', context)


def error_404(request, exception):
    return render(request, 'errorpages/404.html', status=404)

def error_500(request):
    return render(request, 'errorpages/500.html', status=500)