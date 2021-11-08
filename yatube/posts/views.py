from django.conf import settings as s
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CommentForm, PostForm
from .models import Comment, Follow, Group, Post, User


def index(request):
    post_list = Post.objects.all()
    paginator = Paginator(post_list, s.POSTS_COUNT)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    is_index = True
    context = {
        'page_obj': page_obj,
        'is_index': is_index,
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    post_list = group.groups.all()
    paginator = Paginator(post_list, s.POSTS_COUNT)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    is_index = False
    context = {
        'group': group,
        'page_obj': page_obj,
        'is_index': is_index,
    }
    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    author = User.objects.get(username=username)
    post = Post.objects.filter(author=author)
    count = post.count()
    paginator = Paginator(post, s.POSTS_COUNT)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    is_profile = True
    following = False
    if request.user == author:
        its_me = True
    else:
        its_me = False
    if request.user.is_authenticated:
        follow_list = Follow.objects.filter(user=request.user)
        authors = [fol.author for fol in follow_list]
        if author in authors:
            following = True
    context = {
        'author': author,
        'page_obj': page_obj,
        'count': count,
        'is_profile': is_profile,
        'following': following,
        'its_me': its_me,
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    post = Post.objects.get(id=post_id)
    form = CommentForm(request.POST or None)
    try:
        comments = Comment.objects.filter(post=post)
    except Comment.DoesNotExist:
        comments = None
    count = Post.objects.filter(author=post.author).count()
    title = post.text[:30]
    context = {
        'comments': comments,
        'form': form,
        'post': post,
        'title': title,
        'count': count,
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    groups = Group.objects.all()
    form = PostForm(request.POST or None, files=request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        context = {
            'groups': groups,
            'form': form,
        }
        post = form.save(False)
        post.author = request.user
        post.save()
        username = post.author.username
        return redirect(f'/profile/{username}/')
    form = PostForm()
    context = {
        'groups': groups,
        'form': form,
    }
    return render(request, 'posts/create_post.html', context)


@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user.username != post.author.username:
        return redirect(f'/profile/{post.author.username}/')
    groups = Group.objects.all()
    is_edit = True
    form = PostForm(
        request.POST or None, instance=post,
        files=request.FILES or None
    )
    if request.method == 'POST' and form.is_valid():
        context = {
            'form': form,
            'is_edit': is_edit,
            'post': post,
            'groups': groups,
            'post_id': post_id,
        }
        form.save()
        return redirect(f'/posts/{post.id}/')
    form = PostForm()
    context = {
        'form': form,
        'is_edit': is_edit,
        'post': post,
        'groups': groups,
        'post_id': post_id,
    }
    return render(request, 'posts/create_post.html', context)


@login_required
def add_comment(request, post_id):
    post = Post.objects.get(id=post_id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('posts:post_detail', post_id=post_id)


@login_required
def follow_index(request):
    follow_list = Follow.objects.filter(user=request.user)
    authors = [fol.author for fol in follow_list]
    post_list = Post.objects.filter(author__in=authors)
    paginator = Paginator(post_list, s.POSTS_COUNT)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    follow = True
    context = {
        'page_obj': page_obj,
        'follow': follow,
    }
    return render(request, 'posts/follow.html', context)


@login_required
def profile_follow(request, username):
    author = User.objects.get(username=username)
    follow_count = Follow.objects.filter(
        user=request.user,
        author=author,
    ).count()
    if request.user != author and follow_count == 0:
        Follow.objects.create(
            user=request.user,
            author=author,
        )
    return redirect('posts:profile', username=username)


@login_required
def profile_unfollow(request, username):
    author = User.objects.get(username=username)
    Follow.objects.filter(user=request.user, author=author).delete()
    return redirect('posts:profile', username=username)
