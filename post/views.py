from django.shortcuts import render, redirect, reverse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from post.forms import PostForm, CommentForm
from post.models import Post, Comment


# def get_recommend_users(user):
#     all = set()
#     followings = user.following.all()
#     for following in followings:
#         following_followings = following.following.all()
#         for following_following in following_followings:
#             all.add(following_following)
#     if len(all) < 5:
#         pass
#     return 'XD'

@login_required
def post_upload(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.user = request.user
            new_post.save()
            return render(
                request,
                'post/post_upload_done.html'
            )
    else:
        form = PostForm()
    return render(
        request,
        'post/post_upload.html',
        {
            'form': form
        }
    )

@login_required
def post_list(request):
    # recommend_users = get_recommend_users(request.user)
    posts = Post.objects.all()
    paginator = Paginator(posts, 10)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    return render(
        request,
        'post/post_list.html',
        {
            'posts': posts
        }
    )

@login_required
def post_detail(request, id):
    post = Post.objects.get(id=id)
    return render(
        request,
        'post/post_detail.html',
        {
            'post': post
        }
    )

@login_required
def post_like(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        post = Post.objects.get(id=id)
        if request.user not in post.user_like.all():
            post.user_like.add(request.user)
            data = {
                'like_count': post.user_like.count(),
                'is_like': True
            }
        else:
            post.user_like.remove(request.user)
            data = {
                'like_count': post.user_like.count(),
                'is_like': False
            }
        return JsonResponse(data)

@login_required
def get_post(request):
    id = request.GET.get('id')
    post = Post.objects.get(id=id)
    comments = post.comments.all()
    comment_users = [comment.user for comment in comments]
    comment_user_avatars = [comment_user.get_avatar() for comment_user in comment_users]
    comment_user_names = [comment_user.first_name for comment_user in comment_users]
    comment_user_profiles = [reverse('account:user_profile', kwargs={'username': comment_user.username}) for comment_user in comment_users]
    comment_contents = [comment.body for comment in comments]
    data = {
        'first_name': post.user.first_name,
        'avatar': post.user.get_avatar(),
        'image_url': post.image.url,
        'post_body': post.body,
        'like_count': post.user_like.count(),
        'comment_user_avatars': comment_user_avatars,
        'comment_user_names': comment_user_names,
        'comment_user_profiles': comment_user_profiles,
        'comments': comment_contents
    }
    if request.user in post.user_like.all():
        data.update({'is_like': True})
    else:
        data.update({'is_like': False})
    return JsonResponse(data)

@login_required
def comment(request):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            id = request.POST.get('id')
            post = Post.objects.get(id=id)
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()
            data = {
                'comment_user_avatar': comment.user.get_avatar(),
                'comment_user_name': comment.user.first_name,
                'comment_user_profile': reverse('account:user_profile', kwargs={'username': comment.user.username}),
                'comments': comment.body
            }
            return JsonResponse(data)
        return JsonResponse({'message': 'Error.'})
        

