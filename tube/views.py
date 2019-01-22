# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect,HttpResponse,HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.contrib.auth.models import Group, User
from django.contrib.auth import authenticate,login,logout
from django.views.generic import View
#from tastypie.models import ApiKey
from django.db import models
#from accounts.models import CustomUser
from .forms import VideoCreationForm,VideoChangeForm
from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from.models import Video
from django.contrib import messages
from django.utils import timezone


# Create your views here.
class CreateVideoView(TemplateView):
    form_class = VideoCreationForm
    success_url = reverse_lazy('home')
    template_name = 'tube/create_video.html'

    def get(self, request):
        form = self.form_class
        args = {'form': form,"warning":"Your video will be reviewed and posted on our page."}
        return render(request,self.template_name,args)

    def post(self,request):
        form = self.form_class(request.POST)
        if form.is_valid():
            #group = Group.objects.get(name='Patrons')
            #title = form.cleaned_data['title']
            #intro_text = form.cleaned_data['intro_text']
            desc = form.cleaned_data['vid_desc']
            lesson = self.form_valid(form)
            lesson.user = request.user
            lesson.vid_desc = str(desc)
            try:
                lesson.video = request.FILES['video']
            except Exception as e:
                messages.success(request, "Please add a video")
                return redirect('create_video')
            else:
                lesson.save()
                messages.success(request, "You have succefully added a video. Thanks")
                return redirect('create_video')
        else:
            messages.success(request, "There was an error, make sure all fields are filled and image is attached.")
            return redirect('create_video')
        args = {'form': form,"warning":"There was an error, make sure all fields are filled and image is attached."}
        return render(request, self.template_name, args)

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        return obj


class VideoListView(ListView):
    model = Video
    def get_context_data(self, **kwargs):
        users_list = []
        context = super(VideoListView, self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        #all_users = CustomUser.objects.all()
        #for user in all_users:
        #    if get_time_diff(user) < 60:
        #        users_list.append(user)
                #users_list.append(get_time_diff(user))
        #if self.request.user in users_list:
        #    context['online_users'] = users_list.remove(self.request.user)
        #else:
        #     context['online_users'] = users_list
        #context['number_online'] = len(users_list)

        #context['product_list'] = Product.objects.filter(reviewed=True)
        #sms_list1 = []
        #sms_list2 = []
        #sms_list3 = []
        video_list = Video.objects.all()
        #for each in lesson_list:
        #    if len(sms_list1) <= 10:
        #        sms_list1.append(each)
        #    elif len(sms_list2) <= 10:
        #        sms_list2.append(each)
        #    else:
        #        sms_list3.append(each)
        context['video_list'] = video_list
        #context['lesson_list1'] = sms_list1
        #context['lesson_list2'] = sms_list2
        #context['lesson_list3'] = sms_list3
        context['object'] = Video.objects.filter(status="p")[0]
        #yesterday = (datetime.now() - timedelta(1)).date()
        #today = datetime.today().date()
        #tricks = Trick.objects.order_by('date_created')
        #if len(tricks) < 1:
        #    tricks = Trick.objects.all()
        #if len(tricks) != 0:
        #    context['trick'] = tricks[len(tricks)-1]
        return context
    def get_queryset(self):
            return Video.objects.filter(status="p")

def get_time_diff(user):
    if user.last_activity:
        now = datetime.utcnow().replace(tzinfo=utc)
        timediff = now - user.last_activity
        return timediff.total_seconds()


class VideoDetailView(DetailView):
    model = Video
    def get_context_data(self, **kwargs):
        #from random import sample
        #people_ymk = []
        context = super(VideoDetailView, self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        #my_list = Product.objects.filter(reviewed=True)[::-1]
        #my_list2 = Product.objects.filter(reviewed=True).order_by('date_created')[:]
        #if self.object.id < 25:
        #    context['next'] = self.object.id+1
        #else:
        #    context['next'] = 1
        #if self.object.id > 1:
        #    context['prev'] = self.object.id-1
        #else:
        #    context['prev'] = 25
        #context['products'] = my_list2
        #context['products2'] = my_list
        #context['comments'] = Comment.objects.filter(module=self.object)

        #if self.request.user.is_authenticated:
            #friends = self.request.user.friends.all()
            #context['friends'] = friends.exclude(id=(self.request.user.id))
         #   people = CustomUser.objects.exclude(id=(self.request.user.id))
            #for i in people:
            #    if i not in friends:
            #        if i not in people_ymk:
            #            people_ymk.append(i)
            #context['users'] = sample(people_ymk,10)
        #yesterday = (datetime.now() - timedelta(1)).date()
        #today = datetime.today().date()
        #tricks = Trick.objects.order_by('date_created')
        #if len(tricks) < 1:
        #    tricks = Trick.objects.all()
        #if len(tricks) != 0:
        #    context['trick'] = tricks[len(tricks)-1]
        #context['object_list'] = Lesson.objects.filter(status="p").exclude(id=self.object.id)
        return context

    def get_queryset(self):
            return Video.objects.filter(status="p")


