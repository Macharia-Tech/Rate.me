from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import SignUpForm,UserForm
from django.http import Http404,HttpResponseRedirect
from .forms import UserRegisterForm
from django.db import transaction
from django.contrib.auth import login,authenticate
from django.contrib.auth.models import User
# Create your views here.
def signup(request):
    if request.method == 'POST':
        form=SignUpForm(request.POST,request.FILES)
        if form.is_valid():
            user=form.save()
            user.refresh_from_db()
            user.profile.name=form.cleaned_data.get('name')

            user.profile.Bio=form.cleaned_data.get('Bio')

            user.profile.profile_image=form.cleaned_data.get('profile_image')
            user.save()
            raw_password=form.cleaned_data.get('password1')
            user=authenticate(username=user.username,password=raw_password)
            return redirect (home)
            login(request, user)
            return redirect (home)

    else:
        form=SignUpForm()
    return render (request,'signup.html',{'form':form})
@login_required(login_url='/accounts/login')
def home(request):
    title='Welcome to Instaphoto'
    current_user=request.user
    profile_info=Profile.objects.all()
    profile=Profile.objects.get(user=current_user)
    images=Image.objects.all()


    return render(request,'main/home.html',{"title":title,"profile_info":profile_info,"images":images})
@login_required(login_url='/accounts/login')
def index(request):
    title='Welcome to instagram'


    return render(request,'main/index.html',{"title":title})
@login_required
def first_profile(request,profile_id):
    current_id=request.user.id
    current_profile=Profile.objects.get(id=profile_id)
    try:
        profile_info =Profile.objects.get(id=profile_id)
    except DoesNotExsist:
        raise Http404()

    images =Image.objects.filter(profile=current_profile)
    follows=Profile.objects.get(id=request.user.id)
    is_follow=False
    if follows.follow.filter(id=profile_id).exists():
        is_follow=True

    following=follows.follow.all()
    followers=follows.user.who_following.all()
    return render(request,'main/profile.html',{"profile_info":profile_info,"images":images,"current_id":current_id,"is_follow":is_follow,"total_following":follows.total_following(),"following":following,"followers":followers})

def add_image(request):
    current_user=request.user
    profiles=Profile.get_profile()
    for profile in profiles:
        form=ImageForm(request.POST,request.FILES)
        profile_instance=Profile.objects.get(id=request.user.id)
        if request.method == 'POST':
            if form.is_valid():
                image=form.save(commit=False)
                image.profile=profile_instance
                image.save()
                return redirect(first_profile,request.user.id)

        else:
            form=ImageForm()

    return render(request,'main/image.html',{"form":form})

def details(request,image_id):
    current_image=Image.objects.get(id=image_id)
    images=Image.objects.get(id=image_id)


    is_liked=False
    if images.likes.filter(id=request.user.id).exists():
        is_liked = True

    try:
        image_details = Image.objects.get(id=image_id)
    except DoesNotExsist:
        raise Http404()

    images_profile=Image.objects.filter(id=image_id)

    comment_details=Comment.objects.filter(image=current_image)

    return render(request,'main/details.html',{"image_details":image_details,"comment_details":comment_details,"images":images,"is_liked":is_liked,"total_likes":images.total_likes(),"images_profile":images_profile})





def register(request):
    if request.method =='POST':

        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request,f' Your Account has been created for {username}!')
            return redirect('login')
    else:
        form=UserRegisterForm()
    return render(request, 'users/register.html',{'form':form})