from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import CustomUserCreationForm
from .models import Post
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin



def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username= form.cleaned_data.get('username')
            messages.success(request,f'Account created for {username}!')
            login(request,user)
            return redirect('profile')
    else:
        form = CustomUserCreationForm()
    return render(request,'blog/register.html', {'form':form})

def user_login(request):
    if request.method == 'POST':
        username= request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username = username , password = password)
        if user is not None:
            login(request,user)
            return redirect('porfile')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'blog/login.html')

def user_logout(request):
    logout(request)
    messages.info(request,'you have been logged out.')
    return redirect('login')


@login_required 
def profile(request):
    if  request.method == 'POST':
        email = request.POST['email']
        request.user.email = email
        request.user.save()
        messages.success(request, 'profile updated successfully!')
        return redirect('profile')
    return render(request, 'blog/profile.html')




class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name='posts'
    
class PostDetailView(DeleteView):
    model = Post 
    template_name = 'blog/post_detail.html'

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']
    template_name = 'blog/post_form.html'
    
    def form_vaild (self, form):
        form.instance.author = self.request.user
        return super().form_vaild(form)    
    
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']
    template_name = 'blog/post_form.html'
    
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
    
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model= Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = '/posts'
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author