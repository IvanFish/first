from django.db import models
from django.utils import timezone
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.conf import settings


SHORT_TEXT_LEN = 400

class Post(models.Model):
    author = models.ForeignKey('auth.User')
    title = models.CharField(max_length=200)
    text = RichTextUploadingField(blank=True, default='')
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    likes = models.IntegerField(verbose_name='Нравится', default = 0)
    dislikes = models.IntegerField(verbose_name='Не нравится' , default = 0)
	
    

    def publish (self):
        self.published_date=timezone.now()
        self.save()

    def __str__(self):
        return self.title
        
    def approved_comments(self):
	    return self.comments.filter(approved_comment=True)

    def get_short_text(self):
        if len(self.text) > SHORT_TEXT_LEN:
            return self.text [:SHORT_TEXT_LEN]
        else:
            return self.text

        
class Comment(models.Model):
	post = models.ForeignKey('blog.Post', related_name='comments')
	author = models.CharField(max_length=200)
	text = models.TextField()
	created_date = models.DateTimeField(default=timezone.now)
	approved_comment = models.BooleanField(default=False)
		
	def approve(self):
		self.approved_comment = True
		self.save()
		
	def __str__(self):
		return self.text
		
class UserProfile(models.Model):
	user = models.OneToOneField(User)
	website = models.URLField(blank=True)
	
	def __str__(self):
	    return self.user.username
	    
class UserLikes(models.Model):
    class Meta:
        db_table = 'app_blog_user_likes'
        verbose_name = 'оценку пользователя'
        verbose_name_plural = 'Оценки пользователей'
    UserModel = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')
    user = models.ForeignKey(UserModel, verbose_name="Пользователь")
    post = models.ForeignKey(Post, verbose_name="Статья")
    like = models.BooleanField(verbose_name="Нравится", default=False)
    dislike = models.BooleanField(verbose_name="Не нравится", default=False)
    
    def __str__(self):
        return self.user.username


		
	    
		
