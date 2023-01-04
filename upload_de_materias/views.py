from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test


from django.http import HttpResponseRedirect
from .forms import UploadFileForm

# Imaginary function to handle an uploaded file.
@user_passes_test(lambda u: u.is_superuser)
def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            return HttpResponseRedirect('upload_finalizado')
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})

def handle_uploaded_file(f):
    with open('file/upload.xlsx', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

@user_passes_test(lambda u: u.is_superuser)
def upload_finalizado(request):
   return render(request,"upload_finalizado.html")
