from django.shortcuts import render
from account.models import User
from django.contrib.auth.decorators import login_required


@login_required
def show_profile(request):
    user = User.objects.get(username=request.user)
    degree = user.degree
    context = {
        'user':user,
        'degree':degree,
    }
    return render(request, "perfil.html", context)