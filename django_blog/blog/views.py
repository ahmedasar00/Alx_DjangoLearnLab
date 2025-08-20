from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import CustomUserCreationForm, CommentForm
from .models import Post, Comment
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy


def register(request):
    """
    Handle user registration.
    - If POST: validate and create user, log them in, redirect to profile.
    - If GET: show registration form.
    """
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
    """
    Handle user login.
    - If POST: authenticate user and redirect to profile if valid.
    - If invalid: show error message.
    - If GET: render login page.
    """
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
    """
    Handle user logout.
    - Log out the current user.
    - Redirect to login page with a message.
    """
    logout(request)
    messages.info(request,'you have been logged out.')
    return redirect('login')


@login_required 
def profile(request):
    """
    Display and update user profile.
    - On POST: update email and save.
    - On GET: render profile page.
    """
    if  request.method == 'POST':
        email = request.POST['email']
        request.user.email = email
        request.user.save()
        messages.success(request, 'profile updated successfully!')
        return redirect('profile')
    return render(request, 'blog/profile.html')



class PostListView(ListView):
    """
    Display a list of all blog posts.
    """
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name='posts'
    

class PostDetailView(DetailView):
    """
    Display details of a single blog post.
    """
    model = Post 
    template_name = 'blog/post_detail.html'


class PostCreateView(LoginRequiredMixin, CreateView):
    """
    Allow authenticated users to create a new post.
    """
    model = Post
    fields = ['title', 'content']
    template_name = 'blog/post_form.html'
    
    def form_valid(self, form):
        """Assign the logged-in user as the post author before saving."""
        form.instance.author = self.request.user
        return super().form_valid(form)    


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    Allow the post author to update their post.
    """
    model = Post
    fields = ['title', 'content']
    template_name = 'blog/post_form.html'
    
    def test_func(self):
        """Ensure that only the post author can update."""
        post = self.get_object()
        return self.request.user == post.author
    

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    Allow the post author to delete their post.
    """
    model= Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = '/posts'
    
    def test_func(self):
        """Ensure that only the post author can delete."""
        post = self.get_object()
        return self.request.user == post.author



class CommentListView(ListView):
    """
    Display all comments related to a specific post.
    """
    model = Comment
    template_name = 'blog/comment_list.html'
    context_object_name = 'comments'
    
    def get_queryset(self):
        """Filter comments for the given post."""
        self.post = get_object_or_404(Post, pk=self.kwargs['post_pk'])
        return Comment.objects.filter(post=self.post)
    
    def get_context_data(self, **kwargs):
        """Add the related post object to context."""
        context = super().get_context_data(**kwargs)
        context['post'] = self.post
        return context


class CommentCreateView(LoginRequiredMixin, CreateView):
    """
    Allow authenticated users to add a new comment to a post.
    """
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'
    
    def form_valid(self, form):
        """Set the comment's post and author before saving."""
        post = get_object_or_404(Post, pk=self.kwargs['post_pk'])
        form.instance.post = post
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        """Redirect back to the post detail page after comment creation."""
        return reverse_lazy('post-detail', kwargs={'pk': self.kwargs['post_pk']})


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    Allow the comment author to update their comment.
    """
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'
    
    def form_valid(self, form):
        """Ensure the logged-in user remains the comment author."""
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        """Only the comment's author can update it."""
        comment = self.get_object()
        return self.request.user == comment.author


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    Allow the comment author to delete their comment.
    """
    model = Comment
    template_name = 'blog/delete_comment.html'
    
    def get_success_url(self):
        """Redirect back to the related post after comment deletion."""
        return self.object.post.get_absolute_url()
    
    def test_func(self):
        """Only the comment's author can delete it."""
        comment = self.get_object()
        return self.request.user == comment.author
