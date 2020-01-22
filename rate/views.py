from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse,Http404,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from .forms import NewProjectForm,NewProfileForm
from .models import Project,Profile,Rating
from .serializer import ProfileSerializer,ProjectSerializer
from rest_framework.response import Response
from rest_framework.views import APIView

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

# Create your views here.
@login_required(login_url='/accounts/login/')
def home(request):
    '''
    View for the main homepage.
    '''
    all_projects=Project.objects.all()
    logged_in_user = request.user
    logged_in_user_projects=Project.objects.filter(editor=logged_in_user)
    try:
        profile=Profile.objects.filter(editor=logged_in_user)
    except Profile.DoesNotExist:
        profile=None
    return render(request,'home.html',{"projects":logged_in_user_projects,"profile":profile,"allprojects":all_projects})
@login_required(login_url='/accounts/login/')
def add_project(request):
    current_user = request.user
    print(current_user)
    if request.method == 'POST':
        form = NewProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.editor = request.user
          
            project.save()
        return redirect('home')

    else:
        form = NewProjectForm()
    return render(request, 'new_project.html', {"form": form})

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
    

    
    # try:
    #     photo=Image.objects.get(id=photo_id)

    # except DoesNotExist:
    #     raise Http404()

    return render(request,'project.html',{"project":project_posted})

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
def display_profile(request,user_id):
    '''
    View for displaying a single profile
    '''
    try:
        single_profile=Profile.single_profile(user_id)              
        projects_posted=Project.user_projects(user_id)
        return render(request,'profiledisplay.html',{"profile":single_profile,"projects":projects_posted})
    except Profile.DoesNotExist:
        messages.info(request,'The user has not set a profile yet')
    except Project.DoesNotExist:
        messages.info(request,'The user has not posted a project yet')
        return redirect('home')

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
        
@login_required(login_url='/accounts/login/')
def add_rating(request):
    if request.method == "POST":      
        design = request.POST.get("design", None)
        usability = request.POST.get("usability", None)
        content = request.POST.get("content", None) 
    
    return render(request,'rate.html')