from django.shortcuts import render, redirect, get_object_or_404
from authorization.models import User
from .forms import CommentForm, SearchForm
from .models import Post, Like, Comment


def subscription(request):
    """
    Отображает ленту подписок пользователя.

    Args:
        request (HttpRequest): HTTP-запрос.

    Returns:
        HttpResponse: HTTP-ответ.

    """
    user = request.user
    subscribed_users = user.subscriptions.all()

    posts = Post.objects.filter(user__in=subscribed_users)
    comment_form = CommentForm()
    search_form = SearchForm()

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            post_id = comment_form.cleaned_data['post_id']
            text = comment_form.cleaned_data['text']
            post = get_object_or_404(Post, pk=post_id)
            comment = Comment(user=user, post=post, text=text)
            comment.save()
            return redirect('subscription')

        search_form = SearchForm(request.POST)
        if search_form.is_valid():
            username = search_form.cleaned_data['username']
            search_results = User.objects.filter(username__icontains=username)
            search_heading = 'Найти пользователя:'
            context = {
                'posts': posts,
                'comment_form': comment_form,
                'search_form': search_form,
                'search_results': search_results,
                'search_heading': search_heading,
            }
            return render(request, 'subscription.html', context)

    user_comments = Comment.objects.filter(user=user)

    context = {
        'posts': posts,
        'comment_form': comment_form,
        'search_form': search_form,
        'user_comments': user_comments,
    }
    return render(request, 'subscription.html', context)


def like_post(request, post_id):
    """
    Лайкает указанный пост.

    Args:
        request (HttpRequest): HTTP-запрос.
        post_id (int): Идентификатор поста.

    Returns:
        HttpResponse: HTTP-ответ.

    """
    user = request.user
    post = get_object_or_404(Post, pk=post_id)

    if not Like.objects.filter(user=user, post=post).exists():
        Like.objects.create(user=user, post=post)

    return redirect('subscription')


def subscribe(request, user_id):
    """
    Подписывается на указанного пользователя.

    Args:
        request (HttpRequest): HTTP-запрос.
        user_id (int): Идентификатор пользователя.

    Returns:
        HttpResponse: HTTP-ответ.

    """
    user = request.user
    to_subscribe = get_object_or_404(User, pk=user_id)
    user.subscriptions.add(to_subscribe)
    return redirect('subscription')




