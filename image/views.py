from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from image.forms import ImageForm
from image.models import Image


def get_recommend_users(user):
    all = set()
    followings = user.following.all()
    for following in followings:
        following_followings = following.following.all()
        for following_following in following_followings:
            all.add(following_following)
    if len(all) < 5:
        pass
    return 'XD'

@login_required
def image_upload(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            new_image = form.save(commit=False)
            new_image.user = request.user
            new_image.save()
            return render(
                request,
                'image/image_upload_done.html'
            )
    else:
        form = ImageForm()
    return render(
        request,
        'image/image_upload.html',
        {
            'form': form
        }
    )

@login_required
def image_list(request):
    recommend_users = get_recommend_users(request.user)
    images = Image.objects.all()
    paginator = Paginator(images, 10)
    page = request.GET.get('page')
    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        images = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        images = paginator.page(paginator.num_pages)
    return render(
        request,
        'image/image_list.html',
        {
            'images': images
        }
    )

# @login_required
# def image_detail(request, id):
#     image = Image.objects.get(id=id)
#     return render(
#         request,
#         'image/image_detail.html',
#         {
#             'image':image
#         }
#     )

@login_required
def image_like(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        image = Image.objects.get(id=id)
        if request.user not in image.user_like.all():
            image.user_like.add(request.user)
            data = {
                'like_count': image.user_like.count(),
                'is_like': True
            }
        else:
            image.user_like.remove(request.user)
            data = {
                'like_count': image.user_like.count(),
                'is_like': False
            }
        return JsonResponse(data)

@login_required
def get_image(request):
    id = request.GET.get('id')
    image = Image.objects.get(id=id)
    data = {
        'first_name': image.user.first_name,
        'avatar': image.user.get_avatar(),
        'image_url': image.image.url,
        'image_description': image.description,
        'like_count': image.user_like.count()
    }
    if request.user in image.user_like.all():
        data.update({'is_like': True})
    else:
        data.update({'is_like': False})
    return JsonResponse(data)
