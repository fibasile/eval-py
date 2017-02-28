from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from django.views import generic

from courses.models import Student,Instructor, Notification,Program,StudentBooking,ReviewSession
# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger('django')

def populateCtx(req):
    ctx = {
        "title":"Academany Dashboard",
        "students": req.user.student_set.all(),
        "instructors":  req.user.instructor_set.all()
    }
    programs = []
    program_ids = []
    for s in ctx['students']:
        if not s.program.id in program_ids: 
            programs.append({ 'program' : s.program, 'role':'student'})
            program_ids.append(s.program.id)
    for s in ctx['instructors']:
        if not s.program.id in program_ids: 
            programs.append({ 'program' : s.program, 'role':'instructor'})            
            program_ids.append(s.program.id)
    ctx['programs'] = programs
    
    return ctx

class HomePageView(TemplateView):
    def get(self, request, **kwargs):
        ctx = populateCtx(request)
        return render(request, 'dashboard/index.html', context=ctx)
        
class InboxView(generic.ListView):
    model = Notification
    template_name = 'dashboard/inbox.html'
    #     context_object_name = 'latest_question_list'
    #
    def get_queryset(self):
        """Return the last five published questions."""
        return Notification.objects.filter(user=self.request.user).order_by('-date')[:20]
    # def get(self, request, **kwargs):
    #     return render(request, 'dashboard/inbox.html', context=None)
    
class ProfileView(TemplateView):
    def get(self, request, **kwargs):
        return render(request, 'dashboard/profile.html', context=None)

class AccountView(TemplateView):
    def get(self, request, **kwargs):
        return render(request, 'dashboard/account.html', context=None)
        
class ProgramsView(TemplateView):
    def get(self, request, **kwargs):
        ctx = populateCtx(request)
        # logger.error('programs')
        return render(request, 'dashboard/programs.html', context=ctx)
        
class ProgramView(TemplateView):
    def get(self, request, **kwargs):
        slug = kwargs['program_slug']
        program = Program.objects.filter(code=slug)
        if len(program) > 0:
            program = program[0]
        
        student = Student.objects.filter(user=request.user,program=program)
        instructor = Instructor.objects.filter(user=request.user,program=program)
        modules = program.module_set.all()
        sessions = ReviewSession.objects.filter(module__in = modules)
        
        
        reviews = []
        bookings = []
        if len(student)>0:
            progress = student[0].studentprogress_set.all()
            reviews = student[0].studentreview_set.all()
            bookings = StudentBooking.objects.filter(student=student)
        
        return render(request, 'dashboard/program.html', context={ 
            "program" : program,
            "modules" : modules,
            "student" : student,
            "progress" : progress,
            "sessions" : sessions,
            "reviews" : reviews,
            "students" : len(instructor) > 0 and instructor[0].student_set.all() or [],
            "instructor" : instructor,
            "bookings" : bookings,
            "is_student": len(student)>0, 
            "is_instructor": len(instructor)>0, 
            "is_global_eval": 0
        })