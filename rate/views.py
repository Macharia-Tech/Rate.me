from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import SignUpForm,UserForm
from django.http import Http404,HttpResponseRedirect
from .forms import UserRegisterForm
from django.contrib.auth import login,authenticate
from django.contrib.auth.models import User
from rest_framework.views import APIView
from .models import  Project
from .serializer import ProjectSerializer
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
    title='Welcome to Project Rator'
    current_user=request.user
    profile_info=Profile.objects.all()
    profile=Profile.objects.get(user=current_user)
    images=Image.objects.all()


    return render(request,'main/home.html',{"title":title,"profile_info":profile_info,"images":images})
@login_required(login_url='/accounts/login')
def index(request):
    title='Welcome to Project Rator'


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

class ProfileList(APIView):
    '''
    End point that returns all the profile details such as bio,
    profile_pic,projects posted and contact information
    '''
    def get(self, request, format=None):
        all_profile = Profile.objects.all()
        serializers = ProfileSerializer(all_profile, many=True)
        return Response(serializers.data)

class ProjectList(APIView):
    '''
    End point that returns all projects posted and the details such as title,
    image,description and live link to the project
    '''
    def get(self, request, format=None):
        all_project = Project.objects.all()
        serializers = ProjectSerializer(all_project, many=True)
        return Response(serializers.data)
     

@login_required(login_url='/accounts/login/')
def add_project(request):
    current_user = request.user
    if request.method == 'POST':
        form = NewProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.editor = current_user
            project.save()
        return redirect('home')

    else:
        form = NewProjectForm()
    return render(request, 'new_project.html', {"form": form})

@login_required(login_url='/accounts/login/')
def new_profile(request):
    '''
    Used for creating a new profile for the user. It includes a profile photo, a bio and contact 
    '''
    current_user = request.user
    if request.method == 'POST':
        form = NewProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.editor = current_user
            profile.save()
        return redirect('home')

    else:
        form = NewProfileForm()
    return render(request, 'new_profile.html', {"form": form})    

@login_required(login_url='/accounts/login/')
def single_project(request,project_id):
    '''
    This method displays a single photo and its details such as comments, date posted and caption
    '''

    project_posted=Project.single_project(project_id)  
    imageId=Project.get_image_id(project_id)
    rating=Rating.get_rating_byproject_id(project_id)

    design=Rating.design
    usability=Rating.usability
    content=Rating.content

 
@login_required(login_url='/accounts/login/')
def add_rating(request):
    if request.method == "POST":      
        design = request.POST.get("design", None)
        usability = request.POST.get("usability", None)
        content = request.POST.get("content", None) 
    
    return render(request,'rate.html')
    
@login_required(login_url='/accounts/login/')
def search_title(request):
    '''
    This method searches for an image by using the name of the image
    '''
    if 'title' in request.GET and request.GET["title"]:
        search_term=request.GET.get("title")
        searched_titles=Project.search_by_title(search_term)
        message=f"{search_term}"

        return render(request,"search.html",{"message":message,"titles":searched_titles})
    else:
        message="You haven't searched for any term"
        return render(request,'search.html',{"message":message})


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