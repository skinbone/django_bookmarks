from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.models import User
from django.shortcuts import render_to_response, get_object_or_404, render
from django.contrib.auth import authenticate, login, logout
from bookmarks.forms import RegistrationForm

def main(request):
    if request.user.is_authenticated():
        #return HttpResponseRedirect('/user/%s' % request.user.username)
        return user_page(request, request.user.username)
    return render(request, 'main_page.html')


def user_page(request, username):
#    try:
#        user = User.objects.get(username=username)
#    except User.DoesNotExist:
#        raise Http404('Requested user not found.')
    user = get_object_or_404(User, username=username)
    bookmarks = user.bookmark_set.all()

    return render_to_response('user_page.html', {
        'username': username,
        'bookmarks': bookmarks,
    }, context_instance=RequestContext(request) )


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')


def register_page(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'],
                email=form.cleaned_data['email']
            )
            return HttpResponseRedirect('/register/success/')
    else:
        form = RegistrationForm()
    return render(request, 'registration/register.html', {'form':form } )