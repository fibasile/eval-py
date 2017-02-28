from django.contrib.admin.sites import AdminSite
from tabbed_admin import TabbedModelAdmin
from models import Program, Site,Module,ModuleVideo,Student
from models import Instructor,ReviewSession,StudentBooking
from models import StudentProgress,StudentReview,StudentReviewComment


class StudentDashboardSite(AdminSite):
    pass
    #or overwrite some methods for different functionality

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

    tabs = [
        ( 'Overview', tab_overview),
        # ( 'Information', tab_information),
        ( 'Description',tab_description ),
        ( 'Outcomes', tab_outcomes),
    ]  
    


dashboard = StudentDashboardSite(name="studentdashboard")   
dashboard.register(Module,ModuleAdmin)
