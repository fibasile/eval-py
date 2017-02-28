from django.conf.urls import url
from dashboard import views
from django.contrib.auth.decorators import login_required, permission_required

urlpatterns = [
    url(r'^$', login_required(views.HomePageView.as_view(),login_url='/login/'),name="dashboard"),
    url(r'inbox$', login_required(views.InboxView.as_view(),login_url='/login/')),
    url(r'account$', login_required(views.AccountView.as_view(),login_url='/login/')),
    url(r'profile$', login_required(views.ProfileView.as_view(),login_url='/login/')),
    url(r'programs$', login_required(views.ProgramsView.as_view(),login_url='/login/')),
    url(r'programs/(?P<program_slug>\w+)', login_required(views.ProgramView.as_view(),login_url='/login/'))
]