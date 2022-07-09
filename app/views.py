from unittest.util import safe_repr
from django.shortcuts import render,redirect,HttpResponse
from pkg_resources import safe_name
from .models import Todo
# Create your views here.

def index(request):
    data = Todo.objects.all().order_by('-created_date')
    if request.method == 'POST':
        name = request.POST['name']
        if name == '':
            error = 'Please enter to-do item'
            return render(request, 'index.html', {'error': error,'data':data})
        post = Todo(content=name)
        post.save()
        return redirect('index')
    q = request.GET.get('q')
    if q:
        search = Todo.objects.filter(content__icontains=q)
        count = search.count()
        return render(request, 'index.html',{'data': search,'q':q,'count':count})
    if q == '':
        return redirect('index')
    return render(request, 'index.html',{'data': data})

def delete(request, id):
    try:
        data = Todo.objects.get(id=id)
        data.delete()
    except Todo.DoesNotExist:
        return redirect('index')
    return redirect('index')

def delete_all(request):
    data = Todo.objects.all()
    data.delete()
    return redirect('index')

def update(request,id):
    try:
        data = Todo.objects.get(id=id)
        if request.method == 'POST':
            data.content = request.POST['todo']
            data.save()
            return redirect('index')
    except Todo.DoesNotExist:
        error = "Todo item not found"
        return render(request,'update.html',{'error':error})
    return render(request, 'update.html',{'data':data})