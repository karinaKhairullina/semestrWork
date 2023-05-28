from django.shortcuts import render, redirect
from subscribe.forms import SubscriberForm
from subscribe.models import Subscriber



def home_view(request):
    return render(request, 'home.html')


def QA_view(request):
    return render(request, 'Q&A.html')

def termsUse_view(request):
    return render(request, 'termsUse.html')


def subscribe(request, user_id):
    if request.method == 'POST':
        form = SubscriberForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            subscriber, created = Subscriber.objects.get_or_create(email=email)
            subscriber.is_subscribed = True
            subscriber.save()
            return redirect('home')
    else:
        form = SubscriberForm()
    return render(request, 'home.html', {'form': form})