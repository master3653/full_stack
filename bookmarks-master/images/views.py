from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ImageCreateForm
from .models import Image
from django.views.decorators.http import require_POST,require_GET
from django.http import JsonResponse
from common.decorators import ajax_required
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.http import HttpResponse
from actions.utils import create_action

import redis
from django.conf import settings
# Create your views here.

r = redis.StrictRedis(host=settings.REDIS_HOST,port=settings.REDIS_PORT,db=settings.REDIS_DB)
#装饰器判断用户登录
@login_required
def image_create(request):
    """
    添加图片视图
    """
    if request.method == 'POST':
        # form is sent
        form = ImageCreateForm(data=request.POST)
        if form.is_valid():
            # form data is valid
            cd = form.cleaned_data
            new_item = form.save(commit=False)
            # assign current user to the item
            new_item.user = request.user
            new_item.save()
            create_action(request.user, '添加图片', new_item)
            messages.success(request, '图片添加成功')
            # redirect to new created item detail view
            return redirect(new_item.get_absolute_url())
    else:
        # build form with data provided by the bookmarklet via GET
        form = ImageCreateForm(data=request.GET)

    return render(request, 'images/image/create.html', {'section': 'images',
                                                        'form': form})

def image_detail(request,id,slug):
    image = get_object_or_404(Image,id=id,slug=slug)
    total_views=r.incr('image:{}:views'.format(image.id))
    r.zincrby('image_ranking', image.id, 1)
    return render(request,'images/image/detail.html',{'sections':'images','image':image,'total_views':total_views})

#只允许POST请求，判断用户登录
@ajax_required
@login_required
@require_POST
def image_like(request):
    image_id = request.POST.get('id')
    action = request.POST.get('action')
    if image_id and action:
        try:
            image = Image.objects.get(id=image_id)
            if action == 'like':
                image.user_like.add(request.user)
                print("like")
                create_action(request.user, '喜欢', image)
                print("likes")
            else:
                image.user_like.remove(request.user)
            image.total_likes = image.user_like.count()
            image.total_likes.save()
            return JsonResponse({'status':'OK'})
        except:
            pass
    return JsonResponse({'status':'OK'})

@login_required
def image_list(request):
    images = Image.objects.all()
    print(images)
    paginator = Paginator(images, 8)
    print(paginator)
    try:
        page = request.GET.get('page','1')
        print("meicuo")
    except ValueError as e:
        print(e)
        page=1
    print(page)
    try:
        images = paginator.page(page)
        print("1")
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        print("2")
        images = paginator.page(1)
    except EmptyPage:
        print("出错了")
        if request.is_ajax():
            # If the request is AJAX and the page is out of range return an empty page
            return HttpResponse('')
        # If page is out of range deliver last page of results
        images = paginator.page(paginator.num_pages)
    if request.is_ajax():
        print("3")
        return render(request,'images/image/list_ajax.html',{'section': 'images', 'images': images})
    return render(request,'images/image/list.html',{'section': 'images', 'images': images})


@login_required
def image_ranking(request):
    # get image ranking dictionary
    image_ranking = r.zrange('image_ranking', 0, -1, desc=True)[:10]
    print(image_ranking)
    image_ranking_ids = [int(id) for id in image_ranking]
    print(image_ranking_ids)
    # get most viewed images
    most_viewed = list(Image.objects.filter(id__in=image_ranking_ids))
    print(most_viewed)
    most_viewed.sort(key=lambda x: image_ranking_ids.index(x.id))
    return render(request,
                  'images/image/ranking.html',
                  {'section': 'images',
                   'most_viewed': most_viewed})