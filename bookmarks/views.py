from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.models import User
from django.shortcuts import render_to_response, get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from bookmarks.forms import RegistrationForm, BookmarkSaveForm, SearchForm
from bookmarks.models import Bookmark, Link, Tag

def main(request):
    #if request.user.is_authenticated():
        #return HttpResponseRedirect('/user/%s' % request.user.username)
    return render(request, 'main_page.html')


def user_page(request, username):
#    try:
#        user = User.objects.get(username=username)
#    except User.DoesNotExist:
#        raise Http404('Requested user not found.')
    user = get_object_or_404(User, username=username)
    bookmarks = user.bookmark_set.order_by('-id')

    return render(request, 'user_page.html', {
        'username': username,
        'bookmarks': bookmarks,
        'show_tags': True,
        'show_edit': username==request.user.username,
    } )


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
            return redirect('/register/success/')
    else:
        form = RegistrationForm()
    return render(request, 'registration/register.html', {'form':form } )

def _save_bookmark(request, form):
    # Create or get link.
    link, dummy = Link.objects.get_or_create(
        url=form.cleaned_data['url']
    )
    # Create or get bookmark.
    bookmark, created = Bookmark.objects.get_or_create(
        user=request.user,
        link=link
    )
    # Update bookmark title.
    bookmark.title = form.cleaned_data['title']
    # If the bookmark is being updated, clear old tag list.
    if not created:
        bookmark.tag_set.clear()
        # Create new tag list.
    tag_names = form.cleaned_data['tags'].split()
    for tag_name in tag_names:
        tag, dummy = Tag.objects.get_or_create(name=tag_name)
        bookmark.tag_set.add(tag)
        # Save bookmark to database.
    bookmark.save()
    return bookmark

@login_required
def bookmark_save(request):
    ajax = 'ajax' in request.GET
    if request.method == 'POST':
        form = BookmarkSaveForm(request.POST)
        if form.is_valid():
            bookmark = _save_bookmark(request, form)
            if ajax:
                context = {
                'bookmarks': [bookmark], ###must be a iterable list
                'show_edit': True,
                'show_tags': True,
            }
                return render(request, 'bookmark_list.html', context)
            else:
                return redirect('/user/%s/' % request.user.username)
        else:
            if ajax:
                return HttpResponse(u'failure')

    elif 'url' in request.GET:
        url = request.GET['url']
        title = tags = ''
        try:
            link = Link.objects.get(url=url)
            bookmark = Bookmark.objects.get(
                link=link,
                user=request.user
            )
            title = bookmark.title
            tags = ' '.join(
                tag.name for tag in bookmark.tag_set.all()
            )
        except (Link.DoesNotExist, Bookmark.DoesNotExist):
            pass
        form = BookmarkSaveForm({
            'url': url,
            'title': title,
            'tags': tags,
        })
    else:
        form = BookmarkSaveForm()

    if ajax:
        return render(request, 'bookmark_save_form.html', {'form':form})
    else:
        return render(request, 'bookmark_save.html', {'form':form})


def tag_page(request, tag_name):
    tag = get_object_or_404(Tag, name=tag_name)
    bookmarks = tag.bookmarks.order_by('-id')
    return render(request, 'tag_page.html', {
        'bookmarks': bookmarks,
        'tag_name': tag_name,
        'show_tags': True,
        'show_user': True,
    })


def tag_cloud(request):
    MAX_WEIGHT = 5
    tags = Tag.objects.order_by('name')
    # Calculate tag, min and max counts.
    min_count = max_count = tags[0].bookmarks.count()
    for tag in tags:
        tag.count = tag.bookmarks.count()
        if tag.count < min_count:
            min_count = tag.count
        if max_count < tag.count:
            max_count = tag.count
        # Calculate count range. Avoid dividing by zero.
    range = float(max_count - min_count)
    if range == 0.0:
        range = 1.0
        # Calculate tag weights.
    for tag in tags:
        tag.weight = int(
            MAX_WEIGHT * (tag.count - min_count) / range
        )

    return render(request, 'tag_cloud.html', {'tags':tags})

def search_page(request):
    form = SearchForm()
    bookmarks = []
    query='nothing'
    show_results = False
    if 'query' in request.GET:
        show_results = True
        query = request.GET['query'].strip()
        if query:
            form = SearchForm({'query' : query})
            bookmarks = Bookmark.objects.filter(title__icontains=query)[:10]
    tc = {
        'form': form,
        'bookmarks': bookmarks,
        'show_results': show_results,
        'query': query,
        'show_tags': True,
        'show_user': True,
    }
    if request.GET.has_key('ajax'):
        return render(request, 'bookmark_list.html', tc)
    else:
        return render(request, 'search.html', tc)




def ajax_tag_autocomplete(request):
    if 'q' in request.GET:
        tags = Tag.objects.filter(
            name__istartswith=request.GET['q']
        )[:10]
        return HttpResponse(u'\n'.join(tag.name for tag in tags))
    return HttpResponse()