from django.contrib import admin

from django.contrib.admin import AdminSite
# Register your models here.
from django.core.urlresolvers import reverse

from models import Program, Site,Module,ModuleVideo,Student,Notification
from models import Instructor,ReviewSession,StudentBooking
from models import StudentProgress,StudentReview,StudentReviewComment
from django.contrib.auth.models import User, Group
from django_markdown.admin import AdminMarkdownWidget
from django_markdown.models import MarkdownField
from tabbed_admin import TabbedModelAdmin
from courses.readonly import ReadOnlyModelAdmin
from django.contrib.auth.admin import UserAdmin,GroupAdmin
from django.utils.safestring import mark_safe

class InstructorInline(admin.TabularInline):
    list_filter = ['site']
    fields = ('user','is_guru','is_remote','is_global_eval')
    model = Instructor
    
class StudentInline(admin.TabularInline):
    model = Student
    list_display = ('user','application_id')
    fields = ('application_id','user','instructor')

class SiteAdmin(TabbedModelAdmin):
    list_display = ('name','program','country','continent')
    
    tab_overview = (
        (None, {'fields': ( 'program','code','name')}),
        ("Other information", { 'fields': ('country','website',) })
    )
    tabs = [
       ('Information', tab_overview),
       ('Instructors', (InstructorInline,)),
       ('Students', (StudentInline,))
       
    ]
    
class SiteAdminInline(admin.TabularInline):
    fields = ('name','country')
    model = Site

class InstructorAdmin(admin.ModelAdmin):
    list_filter = ['site']
    list_display = ('user','site')
    
class ModuleVideoAdmin(admin.StackedInline):
    model = ModuleVideo
    extra = 1

class StudentBookingInline(admin.TabularInline):
    title = "Participation to weekly reviews and machine / final project"
    model = StudentBooking
    extra = 1
    
class StudentProgressInline(admin.TabularInline):
    model = StudentProgress
    extra = 1

class StudentReviewInline(admin.StackedInline   ):
    title = "Local and Global reviews"
    model = StudentReview
    fields = ('evaluator','session','get_module','date','notes')
    readonly_fields = ('get_module',)
    extra = 1
    
    
class StudentReviewCommentInline(admin.StackedInline   ):
    title = "Comments"
    model = StudentReviewComment
    extra = 1
    
class ReviewSessionsInline(admin.TabularInline):
    model = ReviewSession
    list_display = ('link','date','module')
    extra = 1
    readonly_fields = ('link',)
    def link(self,obj):
        url = ''
        url = reverse("admin:courses_review_session_change",args=(obj.id,))
        return mark_safe("<a href='%s'>Detail</a>" % (url))
        
    link.short_description = ""
    # the following is necessary if 'link' method is also used in list_display
    link.allow_tags = True

    

class ReviewSessionsAdmin(admin.ModelAdmin):
    list_display = ('date','module')
    inlines = [
        StudentBookingInline,
        # StudentReviewInline
    ]

class StudentAdmin(TabbedModelAdmin):
    list_filter = ['site']
    list_display = ('application_id','user', 'get_email', 'site')
    search_fields = ['user']

    # program = models.ForeignKey(Program,on_delete=models.CASCADE)
    # user = models.OneToOneField(User, on_delete=models.CASCADE)
    # site = models.ForeignKey(Site,on_delete=models.CASCADE)
    # application_id = models.CharField(max_length=255)
    # gitlab_user = models.CharField(max_length=255,blank=True)
    # website_url = models.URLField(blank=True)
    # final_project_slide_url = models.URLField(blank=True)
    # final_project_video_url = models.URLField(blank=True)
    #

    tab_overview = (
           (None, {'fields': ('user', 'program', 'site', 'application_id')}),
    )
    tab_log = (
        StudentBookingInline,
    )
    tab_reviews = (
        StudentReviewInline,
        
    )
    tab_progress = (
        StudentProgressInline,
    )
    # inlines = [
    #     StudentBookingInline,
    #     StudentProgressInline,
    #     StudentReviewInline
    # ]
    tabs = [
           ('Overview', tab_overview),
           ('Attendance', tab_log),
           ('Reviews', tab_reviews),
           ('Progress', tab_progress)
    ]
    
    def get_email(self, obj):
            return obj.user.email
    get_email.admin_order_field='user'
    get_email.short_description='Email'
    
    #self.application_id.short_description='Student id'
    
class StudentsAdminInline(admin.TabularInline):
    model=Student
    # fields=('user','get_email','site')
    fieldsets = [
            ('', {'fields': ['application_id','user','instructor','site']}),
    ]
    readonly_fields = (
        'application_id',
    )
        
    
    def get_email(self, obj):
            return obj.user.email
    get_email.admin_order_field='user'
    get_email.short_description='Email'
    

class ModuleAdminInline(admin.TabularInline):
    model=Module
    # list_display = ('id','date','name')
    fields = ('name','date','link')
    extra = 10
    show_change_link = True
    can_delete = False
    
    def get_readonly_fields(self,request, obj=None):
        if obj != None:
            return ( 'link',)
        else: 
            return ()
    
    def link(self, obj):
        url = reverse("admin:courses_module_change",args=(obj.id,))
        return mark_safe("<a href='%s'>Detail</a>" % (url))
    link.short_description = ""
    # the following is necessary if 'link' method is also used in list_display
    link.allow_tags = True
        
        
class ModuleAdmin(TabbedModelAdmin):
    list_display = ('date','name','program')
    list_filter = ['program']
    list_select_related = (
            'program',
        )
    # formfield_overrides = {MarkdownField: {'widget': AdminMarkdownWidget}}
    
    tab_overview = (
           (None, {'fields': ('name', 'program', 'date','webpage',)}),
    )
    # tab_information = (
    #      (None, {'fields': (  )}),
    # )
    tab_description = (
        (None, {'fields': (  'description', )}),
    )
    tab_outcomes = (
        (None, {'fields': ('outcomes',)}),
    )
    tab_videos = (
        ModuleVideoAdmin,
    )
    tab_reviews = (
        ReviewSessionsInline,
    )
    
    tabs = [
        ( 'Overview', tab_overview),
        # ( 'Information', tab_information),
        ( 'Description',tab_description ),
        ( 'Outcomes', tab_outcomes),
        ( 'Videos', tab_videos),
        # ( 'Assessment', tab_reviews)
    ]    

class ProgramAdmin(TabbedModelAdmin):
    
    tab_overview = (
           (None, {'fields': ('code', 'title', 'year') } ),
    )
    def get_readonly_fields(self, request, obj=None):
            if obj:
                return ['code']
            else:
                return []
    tab_modules = ( ModuleAdminInline, )
    tab_sites = (SiteAdminInline, )
    
    tabs = [
        ('Program', tab_overview),
        ('Modules', tab_modules),
        ('Sites', tab_sites),
        ('Students', ( StudentsAdminInline, ))
    ]
    
class MyUserAdmin(UserAdmin):
    add_fieldsets = (
            (None, {
                'classes': ('wide',),
                'fields': ('username','email', 'password1', 'password2'),
            }),
        )
    
    
class MyAdminSite(AdminSite):
        site_header = 'Academany Backoffice'
        site_title = 'Academany'
        
        

admin_site = MyAdminSite(name='myadmin')
admin_site.register(Notification)
admin_site.register(ReviewSession)
admin_site.register(User,MyUserAdmin)
admin_site.register(Group,GroupAdmin)
admin_site.register(Program,ProgramAdmin)
# admin.site.register(ReviewSession,ReviewSessionsAdmin)
admin_site.register(Module,ModuleAdmin)
admin_site.register(Site,SiteAdmin)
admin_site.register(Student,StudentAdmin)
admin_site.register(Instructor)
# admin.site.register(ModuleVideo,ModuleVideoAdmin)