from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from .register_form import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib import messages
from django.contrib.auth.models import User
from blog.models import Post

# Create your views here.
def register(request):
    if request.method=='POST':
        form=UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request,f"{username} Your account is registered Successfully")
            return redirect('login')

    else:
        form = UserRegisterForm()

    return render(request,'user/register.html',{'form':form})


@login_required
def profile(request, author):
    if request.method=='POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile,
                                    data=request.POST,
                                    files=request.FILES)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request,f"Your Profile has been Updated!")
            profile_url = reverse('profile', args=[request.user])
            return redirect(profile_url)
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form =ProfileUpdateForm(instance=request.user)

    current_user = User.objects.filter(username=author).first()
    posts = Post.objects.filter(author=current_user)
    number_of_articles = Post.published.filter(author=current_user).count()

    context = {
        'u_form':u_form,
        'p_form':p_form,
        'posts':posts,
        'current_user':current_user,
        'number_of_articles' : number_of_articles,
    }
    return render(request, 'user/profile.html', context)

