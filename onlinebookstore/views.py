from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    context = {'user_authenticated': True, 'username': request.user.username}
    return render(request, 'home.html', context)
