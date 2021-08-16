from django.contrib.auth import authenticate,login,logout
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.utils import timezone
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView, View, TemplateView
from django import http
from .models import Token,ArticleModel,ContactUs
from .forms import ArticleModelForm,EditProfileForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.conf import settings
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from .forms import commentForm



class IndexView(TemplateView):
    template_name = 'home_page.html'


class RegisterView(View):
    def post(self,request):
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')

        queryset=User.objects.filter(Q(username=username)|Q(first_name=first_name)|Q(email=email))
        if queryset:
            for i in queryset:
                if i.username==username:
                    return render(request, 'home_page.html',{'message' : 'this username already exists'})
                if i.email==email:
                    return render(request, 'home_page.html', {'message' : 'this email already exists'})
        else:
            password = request.POST.get('password')
            if password:
                user = User.objects.create(first_name=first_name, last_name=last_name,username=username, email=email)
                user.set_password(password)
                user.save()
                recipient_list=[email]
                email_from = settings.EMAIL_HOST_USER
                subject = 'Registeration successfull'
                message = "Hi {}, your email id {} has been registered successfully! \nThanks\nMRSSV".format(username,recipient_list[0])
                send_mail( subject, message, email_from, recipient_list )
                return render(request, 'home_page.html',{'message':'Successfully registered, Please login.'})
            else:
                return render(request, 'home_page.html',{'message':'Please enter the password'})


class LoginView(TemplateView):
    template_name = 'home.html'


class LoginUser(View):
    def post(self, request):
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        if username and password:
            try:
                user_object = User.objects.get(username=username)
                if user_object:
                    authenticated = authenticate(request, username=username, password=password)
                    if authenticated is not None:
                        login(request, authenticated)
                        return redirect('/dashboard/')
                    else:
                        message = 'invalid password'
                        return render(request, "home_page.html", {'message': message})
            except ObjectDoesNotExist:
                error = "Invalid credentials"
                return render(request, 'home_page.html', {'message1': error})
        else:
            message2 = "must enter username and password in the fields"
            return render(request, 'home_page.html', {'message2': message2})


def Logout_view(request):
    logout(request)
    return redirect('/')


def updateProfile(request):
    user = get_object_or_404(User,pk = request.user.id)
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=user)
        if form.is_valid():
            user = form.save()
        return redirect('/dashboard/')
    else:
        form = EditProfileForm(instance=user)

    return render(request, 'profile_edit.html',{'form':form})


#@method_decorator(login_required)
class Dashboard(ListView):
    model = ArticleModel
    template_name = 'article/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'search' in self.request.GET:
            query = self.request.GET.get('search')
            context['article'] = ArticleModel.objects.filter(author__username__icontains=query)
        else:
            context['article'] = ArticleModel.objects.filter(published_date__lte=timezone.now())
        graph_topics = {}
        graph_topics['News'] = ArticleModel.objects.filter(topic='news').count()
        graph_topics['Architecture'] = ArticleModel.objects.filter(topic='arch').count()
        graph_topics['Health'] = ArticleModel.objects.filter(topic='heal').count()
        graph_topics['Politics'] = ArticleModel.objects.filter(topic='politics').count()
        graph_topics['Sports'] = ArticleModel.objects.filter(topic='sports').count()
        graph_topics['Beautytips'] = ArticleModel.objects.filter(topic='beauty').count()
        graph_topics['Others'] = ArticleModel.objects.filter(topic='other').count()
        context['graph'] = graph_topics
        return  context


@login_required(login_url='/login_view/')
def  article_create(request,):
    if request.method == "POST":
        article = ArticleModelForm(request.POST)
        if article.is_valid():
            post = article.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('article_preview', pk=post.pk)
    else:
        article = ArticleModelForm()
    return render(request, 'article/article_create_view.html', {'article':article})


def article_preview(request,pk):
    article = get_object_or_404(ArticleModel,pk=pk)
    # return render(request, 'article/article_detail.html', {'article':article})
    if request.method=="POST":
        form=commentForm(request.POST)
        if form.is_valid():
            comment=form.save(commit=False)
            comment.post=article
            comment.save()
            return render(request, 'article/article_detail.html', {'article':article})
            # return render('post_detail.html',slug=post.slug)
    else:
        form=commentForm()
                
    return render(request,'article/article_detail.html',{'article':article,'form':form})
    


def article_delete(request,pk):
    article = get_object_or_404(ArticleModel, pk=pk)
    if  article.author == request.user:
        if request.method == "GET":
            article.delete()
        return http.HttpResponseRedirect('/dashboard/')
    else:
        return render(request, 'article/article_delete.html', {'article': "You cannot delete other's posts!"})

def  article_update(request,pk):
    post = get_object_or_404(ArticleModel, pk=pk)
    if post.author == request.user:
        if request.method == "POST":
            article = ArticleModelForm(request.POST, instance=post)
            if article.is_valid():
                post = article.save(commit=False)
                post.save()
                return redirect('article_preview', pk=post.pk)
        else:
            article = ArticleModelForm(instance=post)
        return render(request, 'article/article_create_view.html', {'article':article})
    else:
        return render(request, 'article/article_update.html', {'article': "You cannot update other's posts!"})


def unpublished_article(request):
    articles= ArticleModel.objects.filter(published_date__isnull=True)
    return render(request,'article/unpublished_article.html',{'articles':articles})


def publish_article(request,pk):
    article = get_object_or_404(ArticleModel, pk=pk)
    article.publish()
    return redirect('/dashboard/')


def article_graph(request):
    graph_topics = {}
    graph_topics['News'] = ArticleModel.objects.filter(topic='news').count()
    graph_topics['Architecture'] = ArticleModel.objects.filter(topic='arch').count()
    graph_topics['Health'] = ArticleModel.objects.filter(topic='heal').count()
    graph_topics['Politics'] = ArticleModel.objects.filter(topic='politics').count()
    graph_topics['Sports'] = ArticleModel.objects.filter(topic='sports').count()
    graph_topics['Beautytips'] = ArticleModel.objects.filter(topic='beauty').count()
    graph_topics['Others'] = ArticleModel.objects.filter(topic='other').count()
    return render(request, "pie_chart.html", {'graph_topics': graph_topics})


def Contact_page(request):
    name=request.POST.get('name')
    email=request.POST.get('email')
    subject=request.POST.get('subject')
    message=request.POST.get('message')
    ContactUs(name=name,email=email,subject=subject,message=message).save()
    recipient_list=[email]
    email_from = settings.EMAIL_HOST_USER
    send_mail( subject, message, email_from, recipient_list )
    return render(request, 'home_page.html', {'message': 'Your message has been sent. Thank you!'})
