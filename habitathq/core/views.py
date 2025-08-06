from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Notice, Complaint, Visitor, Post
from .forms import ComplaintForm, VisitorForm, PostForm, CommentForm, ProfileUpdateForm
from django.contrib import messages
from django.utils import timezone
from django.core.exceptions import PermissionDenied
from django.utils import timezone
from .forms import CustomUserCreationForm
# Create your views here.



@login_required
def dashboard(request):
    
    
    # for new post by user
    if 'submit_post' in request.POST:
        post_form = PostForm(request.POST)
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.author = request.user
            post.society = request.user.society
            post.save()
            messages.success(request, 'Your post has been published!')
            return redirect('dashboard')
        
        
    
    # handles new Comment Creation under Post by another user 
    if 'submit_comment' in request.POST:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.post = Post.objects.get(id=request.POST.get('post_id'))
            comment.save()
            messages.success(request, 'Your comment was added!')
            return redirect('dashboard')
        
        
    post_form = PostForm()
    comment_form = CommentForm()
    
    
    
    # get the society of loggedin user
    user_society = request.user.society
    
    # fetch all published notices from that society
    notices = Notice.objects.filter(society= user_society, is_published=True)
    
    #Fetch upcoming visitors for the current user
    today = timezone.localdate()
    upcoming_visitors = Visitor.objects.filter(
        visiting_for=request.user,
        expected_datetime__date__gte=today # gte = greater than or equal to
    ).order_by('expected_datetime')
    
    #Fetch all posts from the soceity.
    posts = Post.objects.filter(society=user_society)
    
    context={'notices': notices, 'visitors': upcoming_visitors, 'posts': posts,
             'post_form': post_form,'comment_form': comment_form,}
    return render(request, 'core/dashboard.html', context)






def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            
            user.username = user.email
            
            user.save()
            # You can add a success message here if you want
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'core/signup.html', {'form': form})



@login_required
def create_complaint(request):
    if request.method == 'POST':
        # Create a form instance with the submitted data
        form = ComplaintForm(request.POST)
        if form.is_valid():
            # Create a complaint object but don't save to database yet
            complaint = form.save(commit=False)
            # Assign the current user as the one who raised the complaint
            complaint.raised_by = request.user
            # Now, save the complaint to the database
            complaint.save()
            # Show a success message
            messages.success(request, 'Your complaint has been successfully submitted!!')
            # Redirect to the dashboard
            return redirect('dashboard')
    else:
        # If it's a GET request, create a blank form
        form = ComplaintForm()

    return render(request, 'core/create_complaint.html', {'form': form})



@login_required
def add_visitor(request):
    if request.method == 'POST':
        form = VisitorForm(request.POST)
        if form.is_valid():
            visitor = form.save(commit=False)
            visitor.visiting_for = request.user
            visitor.save()
            messages.success(request, 'Visitor has been pre-registered successfully!')
            return redirect('dashboard')
    else:
        form = VisitorForm()

    return render(request, 'core/add_visitor.html', {'form': form})




@login_required
def security_view(request):
    # Check if the user has the 'SECURITY' role
    if request.user.role != 'SECURITY':
        raise PermissionDenied

    # --- handlee button click (POST Request) ---
    if request.method == 'POST':
        visitor_id = request.POST.get('visitor_id')
        action = request.POST.get('action')
        
        try:
            visitor = Visitor.objects.get(id=visitor_id)
            if action == 'ARRIVED':
                visitor.status = 'ARRIVED'
                visitor.arrival_time = timezone.now()
            elif action == 'DEPARTED':
                visitor.status = 'DEPARTED'
                visitor.departure_time = timezone.now()
            visitor.save()
            messages.success(request, f"{visitor.full_name}'s status updated.")
        except Visitor.DoesNotExist:
            messages.error(request, "Visitor not found.")
        
        return redirect('security_view')

    #  display the Page (GET Request) 
    today = timezone.localdate()
    expected_visitors = Visitor.objects.filter(
        visiting_for__society=request.user.society,
        expected_datetime__date=today
    ).order_by('expected_datetime')

    context = {
        'expected_visitors': expected_visitors,
        'today': today,
    }
    return render(request, 'core/security_view.html', context)


#this is for several users like security, resident. 
@login_required
def redirect_after_login(request):
    if request.user.role == 'SECURITY':
        return redirect('security_view')
    else: # For ADMIN and RESIDENT
        return redirect('dashboard')
    
    
    
    
@login_required
def community_feed(request):
    # Get all posts from the society of the logged-in user
    posts = Post.objects.filter(society=request.user.society)
    
    context = {
        'posts': posts
    }
    return render(request, 'core/community_feed.html', context)





@login_required
def like_post(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.user in post.likes.all():
        # User has already liked the post, so unlike it
        post.likes.remove(request.user)
    else:
        # user has not liked the pist, so like it
        post.likes.add(request.user)
    return redirect('dashboard')




@login_required
def profile_update(request):
    if request.method == 'POST':
        # Pass request.POST and request.FILES to the form
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('dashboard')
    else:
        # Pre-populate the form with the user's current data
        form = ProfileUpdateForm(instance=request.user)

    context = {
        'form': form
    }
    return render(request, 'core/profile_update.html', context)