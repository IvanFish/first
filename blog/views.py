from django.contrib.auth import authenticate, login
from django.contrib import auth
from django.shortcuts import render
from django.utils import timezone
from .models import Post, Comment, UserLikes
from django.shortcuts import render, get_object_or_404,redirect, RequestContext
from .forms import PostForm, CommentForm, UserForm, UserProfileForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist



def post_list(request):
    posts=Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})
    
def post_detail(request, pk):
	post= get_object_or_404(Post, pk=pk)
	return render(request, 'blog/post_detail.html', {'post':post})
	
	
def mail(request):
	return render(request, 'blog/mail.html')
	
# Это вьюха регистрации
 
def register(request):
    registered = False
    
    if request.method == 'POST':
       user_form = UserForm(data=request.POST)
       profile_form = UserProfileForm(data=request.POST)
       
       if user_form.is_valid() and profile_form.is_valid():
          user = user_form.save()
          user.set_password(user.password)
          user.save()
          
          profile =profile_form.save(commit = False)
          profile.user = user
          profile.save()
          registered = True
          
       else:
          print(user_form.errors, profile_form.errors)
          
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
        
    return render(request, 'blog/register.html', 
                  {'user_form': user_form, 'profile_form': profile_form, 'registered': registered})   
                  
def user_login(request):

    # Если запрос HTTP POST, пытаемся извлечь нужную информацию.
    if request.method == 'POST':
        # Получаем имя пользователя и пароль, вводимые пользователем.
        # Эта информация извлекается из формы входа в систему.
                # Мы используем request.POST.get('<имя переменной>') вместо request.POST['<имя переменной>'],
                # потому что request.POST.get('<имя переменной>') вернет None, если значения не существует,
                # тогда как request.POST['<variable>'] создаст исключение, связанное с отсутствем значения с таким ключом
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Используйте Django, чтобы проверить является ли правильным
        # сочетание имя пользователя/пароль - если да, то возвращается объект User.
        user = authenticate(username=username, password=password)

        # Если мы получили объект User, то данные верны.
        # Если получено None (так Python представляет отсутствие значения), то пользователь
        # с такими учетными данными не был найден.
        if user:
            # Аккаунт активен? Он может быть отключен.
            if user.is_active:
                # Если учетные данные верны и аккаунт активен, мы можем позволить пользователю войти в систему.
                # Мы возвращаем его обратно на главную страницу.
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                # Использовался не активный аккуант - запретить вход!
                return HttpResponse("Ваш аккаунт заблокирован.")
        else:
            # Были введены неверные данные для входа. Из-за этого вход в систему не возможен.
            print ("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Неверные данные для входа.")

    # Запрос не HTTP POST, поэтому выводим форму для входа в систему.
    # В этом случае скорее всего использовался HTTP GET запрос.
    else:
        # Ни одна переменная контекста не передается в систему шаблонов, следовательно, используется
        # объект пустого словаря...
        return render(request, 'blog/login.html', {})                            




@login_required	
def post_new(request):
	
	if request.method =="POST":
	     form = PostForm(request.POST)
	     
	     if form.is_valid():
	         post = form.save(commit=False)
	         post.author = request.user
	         post.save()
	         return redirect('post_detail', pk=post.pk)
	         
	else:
	            
	         form = PostForm()
	return render(request, 'blog/post_edit.html', {'form' : form})

@login_required	
def post_edit(request, pk):
	post = get_object_or_404(Post, pk=pk)
	
	if request.method =="POST":
	     form = PostForm(request.POST, instance=post)
	     
	     
	     if form.is_valid():
	         post = form.save(commit=False)
	         post.author = request.user
	         post.save()
	         return redirect('post_detail', pk=post.pk)
	         
	else:
	            
	         form = PostForm(instance=post)
	return render(request, 'blog/post_edit.html', {'form' : form})
	
def add_comment_to_post(request, pk):
	post = get_object_or_404(Post, pk=pk)
	if request.method == "POST":
	    form = CommentForm(request.POST)
	    if form.is_valid():
	        comment = form.save(commit=False)
	        comment.post = post
	        comment.save()
	        return redirect('post_detail', pk=post.pk)
	        
	else:
	    form = CommentForm()
	    
	return render(request, 'blog/add_comment_to_post.html', {'form': form}) 

@login_required	
def post_draft_list(request):
	posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
	return render(request, 'blog/post_draft_list.html', {'posts':posts}) 

@login_required	
def post_publish(request, pk):
	post = get_object_or_404(Post, pk=pk)
	post.publish()
	return redirect('post_detail', pk=pk) 

@login_required	
def post_remove(request, pk):
	post = get_object_or_404(Post, pk=pk)
	post.delete()
	return redirect('post_list')
	
@login_required
def comment_approve(request, pk):
	comment = get_object_or_404(Comment, pk=pk)
	comment.approve()
	return redirect('post_detail', pk=comment.post.pk)
	
@login_required
def comment_remove(request, pk):
	comment = get_object_or_404(Comment, pk=pk)
	post_pk = comment.post.pk
	comment.delete()
	return redirect('post_detail', pk=post_pk)
	

	
def add_like(request, pk):
    try:
        post = get_object_or_404(Post, pk=pk)
        user = auth.get_user(request)
        if user.is_authenticated():
            user_likes = UserLikes.objects.filter(user_id=user.id, post_id=post.id)
            if user_likes.count() == 0:
                post.likes += 1
                post.save()
                UserLikes(user=user, post=post, like=True).save()
        return redirect('post_detail', post.pk)
    except ObjectDoesNotExist:
        return Http404
	
def add_dislike (request, pk):
	try:
	    post = get_object_or_404(Post, pk=pk)
	    user = auth.get_user(request)
	    if user.is_authenticated():
	        user_likes = UserLikes.objects.filter(user_id=user.id, post_id=post.id)
	        if user_likes.count() == 0:
	            post.dislikes += 1
	            post.save()
	    return redirect ('post_detail', post.pk)             
	except ObjectDoesNotExist:
	    return Http404
	

	        
	    
	
	
	         

	
   


