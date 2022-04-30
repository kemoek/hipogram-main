from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Post


def post_list_view(request):

    posts = Post.objects.all().order_by("-creation_datetime")

    #Pagination işlemleri.
    page = request.GET.get('page', 1)
    paginator = Paginator(posts, 5)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)


    return render(request, "post_list.html", {'posts': posts})


#Yeni fotoğraf yükleme işlemi.
def upload(request):
    # Giriş yapmayan veya doğrulanmamış kullanıcı login sayfasına yönlendirilir.
    if not request.user.is_authenticated or request.user.is_anonymous:
        return redirect('http://127.0.0.1:8000/login')


    if request.method == 'POST':
        post = request.FILES['post']
        text = request.POST['text-area']

        posts = Post.objects.create(image = post, created_by = request.user, text = text)
        if posts:
            messages.success(request, "POST uploaded.")

    return render(request, 'upload_photo.html')


#Kullanıcının kendi postlarını filtreleme işlemi.
def filter_username(request, pathUsername):
    print("Goruntulenmek istenen kullanici: ", pathUsername)
    print("Goruntulenen kullanici: ", request.user)


    if not request.user.is_authenticated or request.user.is_anonymous:
        return redirect('http://127.0.0.1:8000/login')

    #Giriş yapmayan veya doğrulanmamış kullanıcı adına göre filtrelemek isterse login sayfasına yönlendirilir.

    posts = Post.objects.filter(created_by = request.user).order_by("-creation_datetime")

    """
    posts = Post.objects.filter(created_by = pathUsername).order_by("-creation_datetime")
    created_by = pathUsername olmalıydı ancak key = str olmadığından buna bir çözüm bulamadım,
    kullanıcı sadece kendi fotoğraflarını filtreleyebiliyor.
    """

    page = request.GET.get('page', 1)
    paginator = Paginator(posts, 5)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request, 'filter_username.html', {'posts': posts})


#Kullanıcı username ile filtreleme yaptıktan sonra
#kendi postlarından istediğini silebilir.
def delete(request, id):

    posts = Post.objects.filter(created_by = request.user, id = id).delete()
    newPosts = Post.objects.all().order_by("-creation_datetime")

    page = request.GET.get('page', 1)
    paginator = Paginator(posts, 5)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request, "post_list.html", {'posts': newPosts})


def update(request, id):

    post = Post.objects.filter(created_by=request.user, id=id)

    return render(request, 'update_photo.html', {'posts': post})


def updateConfirm(request, id):
    newPosts = Post.objects.all().order_by("-creation_datetime")


    post = Post.objects.filter(created_by = request.user, id = id).update(text = "Update işlemini dynamic yapamadım,"
                                                                                 "input valueyi almaya çalıştığımda None dönüyor.")

    if post:
            messages.success(request, "Updated successfully..")

    return render(request, 'post_list.html', {'posts': newPosts})