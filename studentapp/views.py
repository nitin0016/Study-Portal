from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User,auth
from django.views.decorators.cache import never_cache

import requests
from .models import*
import wikipedia
from .forms import*
from django.views import generic
from youtubesearchpython import VideosSearch
from django.contrib.auth.decorators import login_required
# Create your views here.
@never_cache
def home(request):
    return render(request,'home.html',{})

@never_cache
@login_required
def notes(request):
    if request.method=="POST":
        form=NotesForm(request.POST)
        if form.is_valid():
            notes=Notes(user=request.user,title=request.POST['title'],description=request.POST['description'])
            notes.save()
        messages.success(request,f"Notes added from {request.user.username} Successfully!")    
    else:
        form=NotesForm()
    notes=Notes.objects.filter(user=request.user)
    context={'notes':notes,'form':form}
    return render(request,'notes.html',context)

@never_cache
@login_required
def delete_note(request,pk):
    Notes.objects.get(id=pk).delete()
    return redirect("notes")

 
def notedetails(request,pk):
    data=Notes.objects.get(id=pk)
    return render(request,'notes_detail.html',{'data':data})

@never_cache
@login_required
def homework(request):
    if request.method=='POST':
        form=HomeworkForm(request.POST)
        if form.is_valid():
            try:
                finished=request.POST['is_finished']
                if finished=='on':
                    finished=True
                else:
                    finished=False
            except:
                finished=False
            homework=Homework(
                user=request.user,
                subject=request.POST['subject'],
                title=request.POST['title'],
                description=request.POST['description'],
                due=request.POST['due'],
                is_finished=finished
            )                
            homework.save()
            messages.success(request,f"Homework added from {request.user.username} !!!")
    else:        
        form=HomeworkForm()
    homework=Homework.objects.filter(user=request.user)
    if len(homework)==0:
        homework_done=True
    else:
        homework_done=False    
    context={'homework':homework,'form':form,'homework_done':homework_done}
    return render(request,'homework.html',context)

@never_cache
@login_required
def update_homework(request,pk=None):
    homework=Homework.objects.get(id=pk)
    if homework.is_finished == True:
        homework.is_finished = False
    else:
        homework.is_finished = True
    homework.save()
    return redirect('homework')        

@never_cache
@login_required
def delete_homework(request,pk=None):
    Homework.objects.get(id=pk).delete()
    return redirect('homework')

@never_cache
def youtube(request):
    if request.method=="POST":
        form=DashboardForm(request.POST)
        text=request.POST['text']
        video=VideosSearch(text,limit=10)
        result_list=[]
        for i in video.result()['result']:
            result_dict={
                'input':text,
                'title':i['title'],
                'duration':i['duration'],
                'thumbnail':i['thumbnails'][0]['url'],
                'channel':i['channel']['name'],
                'link':i['link'],
                'views':i['viewCount']['short'],
                'published':i['publishedTime']
            }

            desc=''
            if i['descriptionSnippet']:
                for j in i['descriptionSnippet']:
                    desc+=j['text']
            result_dict['description']=desc
            result_list.append(result_dict)
            context={
                'form':form,
                'results':result_list
            }
        return render(request,'youtube.html',context)
    else:
        form=DashboardForm
    return render(request,'youtube.html',{'form':form})

@never_cache
@login_required
def todo(request):
    if request.method=="POST":
        form=TodosForm(request.POST)
        if form.is_valid():
            try:
                finished=request.POST['is_finished']
                if finished=='on':
                    finished=True
                else:
                    finished=False
            except:    
                    finished=False
            todo=Todo(
                user=request.user,
                title=request.POST['title'],
                is_finished=finished
            )    
            todo.save()
            messages.success(request,f"Todos added from {request.user.username} !!!")
    else:
        form=TodosForm()
    todo=Todo.objects.filter(user=request.user)
    if len(todo)==0:
        todos_done=True 
    else:
        todos_done=False    
    return render(request,'todo.html',{'todo':todo,'form':form,'todos_done':todos_done})

@never_cache
@login_required
def updatetodo(request,pk=None):
    todo=Todo.objects.get(id=pk)
    if todo.is_finished == True:
        todo.is_finished = False
    else:
        todo.is_finished = True
    todo.save()
    return redirect('todo')        
    
@never_cache
@login_required
def deletetodo(request,pk=None):
    Todo.objects.get(id=pk).delete()
    return redirect('todo')

@never_cache
def books(request):
    if request.method=="POST":
        form=DashboardForm(request.POST)
        text=request.POST['text']
        url='https://www.googleapis.com/books/v1/volumes?q='+text
        r=requests.get(url)
        answer=r.json()
        result_list=[]
        for i in range(10):
            result_dict={
                'title':answer['items'][i]['volumeInfo']['title'],
                'subtitle':answer['items'][i]['volumeInfo'].get('subtitle'),
                'description':answer['items'][i]['volumeInfo'].get('description'),
                'count':answer['items'][i]['volumeInfo'].get('PageCount'),
                'categories':answer['items'][i]['volumeInfo'].get('categories'),
                'rating':answer['items'][i]['volumeInfo'].get('pageRating'),
                'thumbnail':answer['items'][i]['volumeInfo'].get('ImageLinks'),
                'preview':answer['items'][i]['volumeInfo'].get('previewLink'),
                
            }

            result_list.append(result_dict)
            context={
                'form':form,
                'results':result_list
            }
        return render(request,'books.html',context)
    else:
        form=DashboardForm
    return render(request,'books.html',{'form':form})

@never_cache
def dictionary(request):
    if request.method=="POST":
        form=DashboardForm(request.POST)
        text=request.POST['text']
        url="https://api.dictionaryapi.dev/api/v2/entries/en/"+text
        r=requests.get(url)
        answer=r.json()
        try:
            phonetics=answer[0]['phonetics'][0]['text']
            audio=answer[0]['phonetics'][0]['audio']
            definition=answer[0]['meanings'][0]['definitions'][0]['definition']
            example=answer[0]['meanings'][0]['definitions'][0]['example']
            synonyms=answer[0]['meanings'][0]['definitions'][0]['synonyms']
            context={
                'form':form,
                'input':text,
                'phonetics':phonetics,
                'audio':audio,
                'definition':definition,
                'example':example,
                'synonyms':synonyms
            }
        except:
            context={'form':form,
                     'input':''


            }
    else:
        form=DashboardForm()
        context={'form':form}
    return render(request,'dictionary.html',context) 
@never_cache
def WikiPedia(request):
    if request.method=='POST':
        text=request.POST['text']
        form=DashboardForm(request.POST)
        search=wikipedia.page(text)
        context={
            'form':form,
            'title':search.title,
            'link':search.url,
            'details':search.summary
        }
        return render(request,'wiki.html',context)
    else:
        form=DashboardForm()
        context={
            'form':form
        }
    return render(request,'wiki.html',context)

@never_cache
def register(request):
    if request.method=='POST':
        form=RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username=form.cleaned_data.get('username')
            messages.success(request,f"Account created for {username} !!!")
            return redirect('login')
    else:        
        form=RegistrationForm()
    context={
        'form':form
    }
    return render(request,'register.html',context)
@never_cache
def login(request):
    return render(request,"login.html",)

@never_cache
@login_required
def profile(request):
    homework=Homework.objects.filter(is_finished=False,user=request.user)
    todo=Todo.objects.filter(is_finished=False,user=request.user)
    if len(homework)==0:
        homework_done=True
    else:
        homework_done=False
    if len(todo)==0:
        todos_done=True
    else:
        todos_done=False
    context={
        'homework':homework,
        'todo':todo,
        'homework_done':homework_done,
        'todos_done':todos_done
        
    }                
    return render(request,'profile.html',context)

@never_cache
def logout(request):
    auth.logout(request)
    return render(request,'logout.html')
    