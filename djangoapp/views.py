
from django.shortcuts import render
from .models import Project
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .forms import ProjectUploadForm
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth import login
from django.shortcuts import redirect
from .forms import SignUpForm, LoginForm
from django.contrib.auth import authenticate, login
from django.contrib.auth import login
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model
from .forms import SubmissionForm
from django.contrib.auth.decorators import login_required

# Create your views here.

def home(request):
    return render(request, 'index.html')
def homeAdmin(request):
    return render(request, 'admin/adminDashbord.html')
def homeTeacher(request):
    return render(request, 'teacher/teacherDashbord.html')
def homeStudent(request):
    return render(request, 'student/studentDashbord.html')


def register(request):
    msg = None
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            msg = 'user created'
            return redirect('/login')
        else:
            msg = 'form is not valid'
    else:
        form = SignUpForm()
    return render(request,'signup.html', {'form': form, 'msg': msg})


def login_view(request):
    form = LoginForm(request.POST or None)
    msg = None
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None and user.is_admin:
                login(request, user)
                return redirect('/adminpage/')
            elif user is not None and user.is_teacher:
                login(request, user)
                return redirect('/teacherpage/')
            elif user is not None and user.is_student:
                login(request, user)
                return redirect('/studentpage/')
            else:
                msg= 'invalid credentials'
        else:
            msg = 'error validating form'
    return render(request, 'login.html', {'form': form, 'msg': msg})


@login_required
def logout_view(request):
    logout(request)
    return redirect('index')# Redirige vers la page d'accueil ou une autre page de votre choix

def add_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Vous pouvez ajouter d'autres opérations ici si nécessaire
            return redirect('manage_users')  # Rediriger vers la page de gestion des utilisateurs
    else:
        form = UserCreationForm()
    return render(request, 'admin/user_create.html', {'form': form})


@login_required  # Assure que l'administrateur est connecté
def upload_project(request):
    if request.method == 'POST':
        form = ProjectUploadForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.uploaded_by = request.user
            project.status = 'in_progress'  # Statut initial du projet
            project.save()
            return redirect('/')  # Rediriger vers la page d'accueil
    else:
        form = ProjectUploadForm()
    return render(request, 'admin/uploadprojectAdmin.html', {'form': form})

@login_required  # Assure que l'administrateur est connecté
def manage_projects(request):
    projects = Project.objects.all()
    return render(request, 'admin/manageprojectAdmin.html', {'projects': projects})


User = get_user_model()
@login_required  # Assure que l'administrateur est connecté
def manage_users(request):
    users = User.objects.all()
    return render(request, 'admin/manageuser.html', {'users': users})

@login_required
def upload_project_teacher(request):
    if request.method == 'POST':
        form = ProjectUploadForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.uploaded_by = request.user
            project.status = 'in_progress'
            project.save()
            return redirect('my_projects_teacher')  # Rediriger vers la liste des projets de l'enseignant
    else:
        form = ProjectUploadForm()
    return render(request, 'teacher/upload_project_teacher.html', {'form': form})

@login_required
def my_projects_teacher(request):
    projects = Project.objects.filter(uploaded_by=request.user)
    return render(request, 'teacher/my_projects_teacher.html', {'projects': projects})

@login_required
def my_projects_student(request):
    projects = Project.objects.filter(uploaded_by=request.user)
    return render(request, 'student/my_projects_student.html', {'projects': projects})

@login_required
def submit_project(request, project_id):
    project = Project.objects.get(id=project_id)
    
    if request.method == 'POST':
        form = SubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.project = project
            submission.user = request.user
            submission.save()
            return redirect('my_projects_student')  # Rediriger vers la liste des projets de l'étudiant
    else:
        form = SubmissionForm()
    
    context = {'form': form, 'project': project}
    return render(request, 'submit_project.html', context)