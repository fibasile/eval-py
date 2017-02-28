from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django_markdown.models import MarkdownField
from countries_plus.models import Country

# Create your models here.
class Program(models.Model):
    code = models.CharField(max_length=20)
    title = models.CharField(max_length=200)
    description = models.TextField()
    year = models.IntegerField(default=2017)
    def __str__(self):
        return self.title


class Site(models.Model):
    code = models.CharField(max_length=60)
    name = models.CharField(max_length=60,default="")
    program = models.ForeignKey(Program,on_delete=models.CASCADE)
    country = models.ForeignKey(Country)
    website = models.URLField()
    @property 
    def continent(self):
        if self.country:
            return self.country.continent
        return ''
        
    def __str__(self):
        return self.code
        

class Module(models.Model):
    program = models.ForeignKey(Program,on_delete=models.CASCADE)
    name =  models.CharField(max_length=255)
    description = MarkdownField()
    outcomes = MarkdownField()
    webpage =  models.URLField(blank=True)
    date = models.DateTimeField()
    def __str__(self):
        return '%s - %s' % (self.program.title, self.name)
        
class ReviewSession(models.Model):
    module = models.ForeignKey(Module,on_delete=models.CASCADE)
    date = models.DateTimeField()
    title = models.CharField(max_length=255,default="Weekly Review")
    def __str__(self):
        return '%s - %s' % (self.title, self.date)
    class Meta:
        verbose_name = "Review"
    
    

class Student(models.Model):
    program = models.ForeignKey(Program,on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    instructor = models.ForeignKey('Instructor',blank=True)
    site = models.ForeignKey(Site,on_delete=models.CASCADE)
    application_id = models.CharField(max_length=255)
    gitlab_user = models.CharField(max_length=255,blank=True)
    website_url = models.URLField(blank=True)
    final_project_slide_url = models.URLField(blank=True)
    final_project_video_url = models.URLField(blank=True)

    
    def progress(self):
        return 0
    
    def is_complete(self):
        return False

    def is_graduated(self):
        return False
    
    def __str__(self):
        return str(self.user)

    def save(self):
        self.program = self.site.program
        super(Student,self).save()
        
    # @receiver(post_save, sender=User)
    # def create_user_profile(sender, instance, created, **kwargs):
    #     if created:
    #         Profile.objects.create(user=instance)
    #
    # @receiver(post_save, sender=User)
    # def save_user_profile(sender, instance, **kwargs):
    #     instance.profile.save()

class Instructor(models.Model):
    program = models.ForeignKey(Program,on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    site = models.ForeignKey(Site,on_delete=models.CASCADE)
    is_guru = models.BooleanField()
    is_remote = models.BooleanField()
    is_global_eval = models.BooleanField()
    website_url = models.URLField(blank=True)
    def __str__(self):
        first= self.user.first_name
        last= self.user.last_name
        if not first:
            first = self.user.username
        return '%s %s' % (first,last)
        
    def save(self):
        self.program = self.site.program
        super(Instructor,self).save()

    
class StudentBooking(models.Model):
    session = models.ForeignKey(ReviewSession)
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    attended = models.BooleanField()
    confirmed = models.BooleanField()
    class Meta:
        verbose_name = "participation"
    
class StudentProgress(models.Model):
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    module = models.ForeignKey(Module,on_delete=models.CASCADE)
    progress = models.IntegerField(default=0)
    completed = models.BooleanField()
    date = models.DateTimeField()  
    class Meta:
        verbose_name = "certificate"
          
    
class StudentReview(models.Model):
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    evaluator = models.ForeignKey(Instructor,on_delete=models.CASCADE)
    session = models.ForeignKey(ReviewSession)
    date = models.DateTimeField()
    notes = MarkdownField()
    
    
    def get_module(self):
        return self.session.module
    get_module.short_description = 'Module'
    
    @property
    def comments(self):
        return 'Test'
    def __str__(self):
        return '%s by %s' % (str(self.session), self.evaluator)
    
class StudentReviewComment(models.Model):
    author = models.ForeignKey(User);
    date = models.DateTimeField()
    comment = MarkdownField()
    review = models.ForeignKey(StudentReview,on_delete=models.CASCADE)
        
class Notification(models.Model):
    NOTIFICATION_CHOICE = (
        ('info','Info'),
        ('error','Error'),
        ('debug','Debug')
    )
    user = models.ForeignKey(User)
    date = models.DateTimeField()
    message = models.CharField(max_length=255)
    kind = models.CharField(choices=NOTIFICATION_CHOICE, max_length=8)
        
        
class ModuleVideo(models.Model):
    VIDEO_CHOICES = (
        ('review', 'Review'),
        ('lecture', 'Lecture'),
        ('misc', 'Misc'),
        )
        
    name =  models.CharField(max_length=255)
    kind = models.CharField(choices=VIDEO_CHOICES,default='review',max_length=8) 
    module = models.ForeignKey(Module,on_delete=models.CASCADE)
    url = models.URLField()
    
    class Meta:
        verbose_name = "video"
    