from django.shortcuts import render,redirect
from .models import *
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.views.generic import DetailView
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .serializers import RecipeSerializer

@login_required(login_url='/login')
def add_recipe(request):
    if request.method == 'POST':
        data = request.POST

        receipe_name = data.get('recipe_name')
        receipe_description = data.get('recipe_description')
        receipe_image = request.FILES['recipe_image']

        # Get the current logged-in user
        user = request.user

        # Create the recipe associated with the user
        Receipe.objects.create(
            user=user,
            receipe_name=receipe_name,
            receipe_discription=receipe_description,
            receipe_image=receipe_image,
        )
        return redirect('add_recipe')

    # Retrieve recipes associated with the current user
    queryset = Receipe.objects.filter(user=request.user)

    if request.GET.get('search'):
        queryset = queryset.filter(receipe_name__icontains=request.GET.get('search'))

    context = {'receipes': queryset}
    return render(request, 'add_recipe.html', context)

def home(request):

    queryset = Receipe.objects.all()
    if request.GET.get('search'):
        queryset = queryset.filter(receipe_name__icontains = request.GET.get('search'))

    context = {'receipes': queryset}
    return render(request, 'home.html', context)
    
def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
       

        if not User.objects.filter(username=username).exists():
            messages.info(request, 'User not exist')
            return redirect('/login')
        user = authenticate(username = username , password = password)

        if user is None:
            messages.info(request, 'Invalid Password')
            return redirect('/login')
        else:
            login(request,user)
            return redirect('/')
    return render(request, 'login.html')

def logout_page(request):
    logout(request)
    return redirect('/login')

@user_passes_test(lambda u: not u.is_authenticated, login_url='')
def register_page(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = User.objects.filter(username = username)
        if user.exists():
            messages.info(request,'User already exists')
            return redirect('/register')

        user = User.objects.create(
            first_name=first_name,
            last_name=last_name,
            username=username
        )
        user.set_password(password)
        user.save()

        messages.info(request,'Account created successfully')
        return redirect('/')

    return render(request, 'register.html')

@login_required
def update_receipe(request, id):
    queryset = Receipe.objects.get(id=id)

    if request.method == "POST":
        data = request.POST

        receipe_name = data.get('receipe_name')
        receipe_description = data.get('receipe_description')
        receipe_image = request.FILES.get('receipe_image')

        queryset.receipe_discription = receipe_description
        queryset.receipe_name = receipe_name

        if receipe_image:
            queryset.receipe_image = receipe_image
        queryset.save()

        return redirect('add_recipe')

    context = {'Receipe': queryset}  
    return render(request, 'update_recipe.html', context)

@login_required
def delete_receipe(request , id):

    queryset = Receipe.objects.get(id=id)
    queryset.delete()
    return redirect('add_recipe')

class DetailReciepi(DetailView):
    model = Receipe
    template_name='detail.html'



class MyApiView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    # queryset=Receipe.objects.all()
    serializer_class=RecipeSerializer
    def get_queryset(self):
        user=self.request.user
        return Receipe.objects.filter(user=user)
