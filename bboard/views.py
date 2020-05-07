from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, JsonResponse, HttpResponseRedirect, request
from .models import Bd, Rubric, Comment, comment_save, Images
from django.template import loader
from django.views.generic.edit import CreateView
from .forms import BdForm, AuthUserForm, RegisterUserForm, CommentForm, ChangePasswordForm, ImageForm
from django.urls import reverse_lazy, reverse
import os
from django.core.paginator import Paginator
from django.contrib.auth.views import FormView, LoginView, LogoutView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import DetailView
from django.contrib import messages
from django.core.signing import BadSignature
from .utilities import signer
from django.shortcuts import get_object_or_404
from django.dispatch import Signal
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth import password_validation
from django.forms import modelformset_factory
from samplesite import settings
import requests

def index(request):
    ''' :return: a list of all ads
    '''
    images = Images.objects.all()
    rubrics = Rubric.objects.all()
    bbs = Bd.objects.all()
    ccs=Comment.objects.all()
    paginator = Paginator(bbs, 2)
    if 'page' in request.GET:
        page_num = request.GET['page']
    else:
        page_num = 1
    page = paginator.get_page(page_num)
    context = {'page': page, 'bbs': page.object_list, 'rubrics': rubrics, 'ccs': ccs, 'images': images}
    return render(request, 'bboard/index.html', context)

def by_rubric(request, rubric_id):
    ''' :param rubric_id: number of rubric
        :return: a list od ads in this rubric
    '''
    bbs=Bd.objects.filter(rubric=rubric_id)
    rubrics=Rubric.objects.all()
    current_rubric = Rubric.objects.get(pk=rubric_id)
    context = {'bbs': bbs, 'rubrics': rubrics, 'current_rubric': current_rubric}
    return render(request, 'bboard/by_rubric.html', context)

@login_required(login_url='/bboard/login')
def Bdcreate(request):
    ''' :return: ad creation
    '''
    ImageFormSet = modelformset_factory(Images, form=ImageForm, extra=3)
    rubrics = Rubric.objects.all()
    if request.method=='POST':
        form=BdForm(request.POST)
        formset=ImageFormSet(request.POST, request.FILES, queryset=Images.objects.none())
        if form.is_valid() and formset.is_valid():
            new_Bd=form.save(commit=False)
            new_Bd.author=request.user
            new_Bd.save()
            for image in formset.cleaned_data :
                img=image['image']
                photo=Images(post=new_Bd, img=img)
                photo.save()
            messages.success(request, 'Cоздал!')
        else:
            price_errors = form.errors['price']
            messages.success(request, f'Error: {price_errors}')
            return HttpResponseRedirect('/bboard/add/')
        return HttpResponseRedirect('/bboard/index')
    else:
        form = BdForm()
        formset = ImageFormSet(queryset=Images.objects.none())
    return render(request, 'bboard/create.html', {'form': form, 'rubrics': rubrics, 'formset': formset})


def Mylogin(request):
    rubrics = Rubric.objects.all()
    if request.method == 'POST':
        password = request.POST['password']
        username = request.POST['username']
        recaptcha_response = request.POST.get('g-recaptcha-response')
        data = {
            'secret': settings.RECAPTCHA_PRIVATE_KEY,
            'response': recaptcha_response
        }
        r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data) #google captcha check
        result = r.json()
        user=authenticate(request, username=username, password=password)
        if user is not None and result['success']:
            login(request, user)
            messages.success(request, 'Вы вошли')
            return HttpResponseRedirect(f'/bboard/profile/{username}')
        else:
            messages.error(request, 'Неверный логин или пароль, или капчу забыл')
            return HttpResponseRedirect('/bboard/login')
    else:
        form=AuthUserForm
        context={'rubrics' :rubrics, 'form': form}
        return render(request, 'bboard/login.html', context)

class MyLogoutView(LogoutView):
    next_page='/bboard/index'


class MyRegisterUser(CreateView):
    model=User
    template_name = 'bboard/register.html'
    form_class = RegisterUserForm
    success_url = '/bboard/index'


def comment(request, bd_id):
    ''' :param bd_id:
        :return: comment creation
    '''
    rubrics = Rubric.objects.all()
    bbs = Bd.objects.all()
    if request.method=='POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment=form.save(commit=False)
            new_comment.bb=bbs.get(pk=bd_id)
            new_comment.save()
            comment_save.send(Comment, instance=new_comment)
            messages.success(request, 'Успех')
        return HttpResponseRedirect('/bboard/index')
    else:
        Comments = Comment.objects.all()
        context_comment=[]
        for ccs in Comments:
            if ccs.bb.pk==bd_id:
                context_comment.insert(0, ccs)
        comment_form=CommentForm
        context={'ccs': context_comment, 'form': comment_form, 'rubrics': rubrics}
        return render(request, 'bboard/comment.html', context)


def user_activate(request, sign):
    ''' :param sign: signed user
        :return: user activated
    '''
    try:
        username = signer.unsign(sign)
    except BadSignature:
        return HttpResponse('Что то не так!')
    user = get_object_or_404(User, username=username)
    template='bboard/activation_done.html'
    user.is_active = True
    user.is_activated = True
    user.save()
    return render(request, template)

@login_required(login_url='/bboard/login')
def profile(request, username):
    ''' :param username: user
        :return: user page
    '''
    images = Images.objects.all()
    author=User.objects.get(username=username)
    bbs=Bd.objects.filter(author=author)
    rubrics=Rubric.objects.all()
    context={'username':username, 'rubrics': rubrics, 'bbs': bbs, 'images': images}
    return render(request, 'bboard/profile.html', context)

@login_required(login_url='/bboard/login')
def editBd(request,bd_pk):
    ''' :param bd_pk: number of ad
        :return: ad editing
    '''
    bb=Bd.objects.get(pk=bd_pk)
    user = User.objects.get(username=bb.author.username)
    images=Images.objects.filter(bb=bb)
    ImageFormSet = modelformset_factory(Images, form=ImageForm, extra=3)
    rubrics = Rubric.objects.all()
    if request.method == 'POST':
        form = BdForm(request.POST, request.FILES, instance=bb)
        formset = ImageFormSet(request.POST, request.FILES, queryset=Images.objects.none())
        if form.is_valid() and formset.is_valid():
            bb.save()
            for i in images:
                i.delete()
            for image in formset.cleaned_data:
                img = image['image']
                photo = Images(post=bb, img=img)
                photo.save()
            messages.success(request, 'Редактировал!')
        else:
            messages.error(request, 'Не создал!')
        return HttpResponseRedirect(f'/bboard/profile/{user.username}')
    else:
        formset = ImageFormSet(queryset=Images.objects.none())
        form = BdForm(instance=bb)
    return render(request, 'bboard/editBd.html', {'form': form, 'rubrics': rubrics,
                                                  'bb': bb, 'formset': formset})


@login_required(login_url='/bboard/login')
def deleteBd(request, bb_pk):
    bb = Bd.objects.get(pk=bb_pk)
    user = User.objects.get(username=bb.author.username)
    images = Images.objects.filter(bb=bb)
    dir_project=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    for i in images:
        os.remove(dir_project+f'/media/{i.img}')
    bb.delete()
    messages.success(request, 'Удалил!')
    return HttpResponseRedirect(f'/bboard/profile/{user.username}')

def searchBd(request):
    word=request.GET.get('search')
    bbs=Bd.objects.filter(Q(title__icontains=word) | Q(content__icontains=word))
    rubrics = Rubric.objects.all()
    context = {'bbs': bbs, 'rubrics': rubrics}
    return render(request, 'bboard/searchBd.html', context)

def password_change(request):
    user=request.user
    rubrics = Rubric.objects.all()
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            new_pass = form.cleaned_data['password1']
            new_pass1 = form.cleaned_data['password2']
            try:
                password_validation.validate_password(new_pass)
            except Exception as e:
                messages.error(request, f'{e}')
                return HttpResponseRedirect('/bboard/password_change')
            if (user.check_password(password)) and (new_pass == new_pass1):
                user.set_password(new_pass)
                user.save()
                messages.success(request, 'Успех!')
                aut_user = authenticate(username=user.username, password=new_pass)
                login(request, aut_user)
                return HttpResponseRedirect('/bboard/password_change')
            else:
                messages.error(request, 'Внимательнее вводи данные!')
                return HttpResponseRedirect('/bboard/password_change')
    else:
        form = ChangePasswordForm()
        context={'form': form, 'rubrics': rubrics}
        return render(request, 'bboard/password_change_form.html', context)

def page_Bd(request, bd_pk):
    ''' :param bd_pk: number of ad
        :return: page of ad
    '''
    bb = Bd.objects.get(pk=bd_pk)
    rubrics = Rubric.objects.all()
    image = Images.objects.filter(bb=bb)
    coments=Comment.objects.filter(bb=bb)
    context = {'rubrics': rubrics, 'bb': bb, 'coments': coments, 'image':image}
    return render(request, 'bboard/page_Bd.html', context)

