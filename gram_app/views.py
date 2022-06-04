from django.shortcuts import render

def home(request):
    context = {}
    return render(request, 'gram_app/index.html',context )
