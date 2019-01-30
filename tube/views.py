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
from accounts.models import CustomUser
from .forms import VideoCreationForm,VideoChangeForm
from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from.models import Video,Comment
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
                video = request.FILES['video']
            except Exception as e:
                messages.error(request, "Please add a video")
                return redirect('create_video')
            else:
                if video.size > 10*1024*1024:
                    messages.error(request, "The video is too large.")
                    return redirect('create_video')
                else:
                    lesson.video = request.FILES['video']
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
        #obj.save()
        return obj


class VideoListView(ListView):
    model = Video
    def get_context_data(self, **kwargs):
        trend_list = []
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
        trend = Video.objects.all().order_by('views')
        for i in trend:
            trend_list.append(i)

        #for each in lesson_list:
        #    if len(sms_list1) <= 10:
        #        sms_list1.append(each)
        #    elif len(sms_list2) <= 10:
        #        sms_list2.append(each)
        #    else:
        #        sms_list3.append(each)
        context['video_list'] = video_list
        context['trend_list'] = trend_list[::-1]
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
        context['related_list'] = Video.objects.filter(category=self.object.category).exclude(id=self.object.id)
        context['comments'] = Comment.objects.filter(video=self.object)
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

    def get_object(self):
        obj = super().get_object()
        # Updates number of views
        obj.views += 1
        obj.save()
        return obj

def like(request,video_id):
    user = CustomUser.objects.get(id=request.user.id)
    video = Video.objects.get(id=video_id)
    videos_liked = list(user.videos_liked.all())
    videos_unliked = list(user.videos_unliked.all())
    if video not in videos_liked and video not in videos_unliked:
        video.likes += 1
        video.save()
        user.videos_liked.add(video)
        user.save()
        messages.error(request,"You liked this video")
        return redirect('/tube/video/{}/'.format(video_id))

    elif video not in videos_liked and video in videos_unliked:
        video.dislikes -= 1
        video.likes +=1
        video.save()
        user.videos_liked.add(video)
        user.videos_unliked.remove(video)
        user.save()
        messages.error(request,"You now liked this video")
        return redirect('/tube/video/{}/'.format(video_id))

    else:
        messages.error(request,"You already liked this video")
        return redirect('/tube/video/{}/'.format(video_id))


def unlike(request,video_id):
    user = CustomUser.objects.get(id=request.user.id)
    video = Video.objects.get(id=video_id)
    videos_liked = list(user.videos_liked.all())
    videos_unliked = list(user.videos_unliked.all())
    if video not in videos_liked and video not in videos_unliked:
        video.dislikes += 1
        video.save()
        user.videos_unliked.add(video)
        user.save()
        messages.error(request,"You unliked this video")
        return redirect('/tube/video/{}/'.format(video_id))

    elif video in videos_liked and video not in videos_unliked:
        video.likes -= 1
        video.dislikes +=1
        video.save()
        user.videos_unliked.add(video)
        user.videos_liked.remove(video)
        user.save()
        messages.error(request,"You unliked this video")
        return redirect('/tube/video/{}/'.format(video_id))
    else:
        messages.error(request,"You already unliked this video")
        return redirect('/tube/video/{}/'.format(video_id))


def del_comment(request,comment_id,lesson_id):
    comment = Comment.objects.get(id=comment_id)
    if request.user == comment.user:
        comment.delete()
        messages.success(request, "Comment deleted!")
        return redirect('/lessons/lesson/{}/'.format(lesson_id))
    messages.error(request, "You cannot delete this comment!")
    return redirect('/lessons/lesson/{}/'.format(lesson_id))


def api_likes(request,video_id):
    user = CustomUser.objects.get(id=request.user.id)
    video = Video.objects.get(id=video_id)
    videos_liked = list(user.videos_liked.all())
    videos_unliked = list(user.videos_unliked.all())
    if video not in videos_liked and video not in videos_unliked:
        video.likes += 1
        video.save()
        user.videos_liked.add(video)
        user.save()
        messages.error(request,"You liked this video")
        return redirect('/tube/video/{}/'.format(video_id))

    elif video not in videos_liked and video in videos_unliked:
        video.dislikes -= 1
        video.likes +=1
        video.save()
        user.videos_liked.add(video)
        user.videos_unliked.remove(video)
        user.save()
        messages.error(request,"You now liked this video")
        return redirect('/tube/video/{}/'.format(video_id))

    else:
        messages.error(request,"You already liked this video")
        return redirect('/tube/video/{}/'.format(video_id))

#from rest_framework.decorators import api_view
#from rest_framework.decorators import parser_classes
#from rest_framework.parsers import JSONParser
from django.http import JsonResponse

# @api_view(['GET'])
# @parser_classes((JSONParser,))
def api_like(request,video_id, format=None):
    """A view that can accept GET"""
    """Getting user, video object, videos liked by user and videos unliked by user"""
    user = CustomUser.objects.get(id=request.user.id)
    video = Video.objects.get(id=video_id)
    videos_liked = list(user.videos_liked.all())
    videos_unliked = list(user.videos_unliked.all())
    if video not in videos_liked and video not in videos_unliked:
        video.likes += 1
        video.save()
        user.videos_liked.add(video)
        user.save()
        #messages.error(request,"You liked this video")
        responseData = {
        'id': video_id,
        'message': "<i class='material-icons green-text center'>thumb_up</i>+1",
        'likes':video.likes,
        'unlikes':video.dislikes,
        'success':True}
        #'roles' : ['Admin','User']}
        return JsonResponse(responseData)
        #return redirect('/tube/video/{}/'.format(video_id))

    elif video not in videos_liked and video in videos_unliked:
        video.dislikes -= 1
        video.likes +=1
        video.save()
        user.videos_liked.add(video)
        user.videos_unliked.remove(video)
        user.save()
        #messages.error(request,"You now liked this video")
        #user.videos_liked.remove(video)
        responseData = {
        'id': video_id,
        'likes':video.likes,
        'unlikes':video.dislikes,
        'message': "<i class='material-icons green-text center'>thumb_up</i>+1",
        'success':True}
        #'roles' : ['Admin','User']}
        return JsonResponse(responseData)
        #return redirect('/tube/video/{}/'.format(video_id))

    else:
        video.likes -=1
        video.save()
        user.videos_liked.remove(video)
        user.save()
        #messages.error(request,"You already liked this video")
        responseData = {
        'id': video_id,
        'likes':video.likes,
        'unlikes':video.dislikes,
        'message': "<i class='material-icons red-text center'>thumb_up</i>-1",
        'success':False}
        #'roles' : ['Admin','User']}
        return JsonResponse(responseData)




def api_unlike(request,video_id):
    user = CustomUser.objects.get(id=request.user.id)
    video = Video.objects.get(id=video_id)
    videos_liked = list(user.videos_liked.all())
    videos_unliked = list(user.videos_unliked.all())
    if video not in videos_liked and video not in videos_unliked:
        video.dislikes += 1
        video.save()
        user.videos_unliked.add(video)
        user.save()
        #messages.error(request,"You unliked this video")
        responseData = {
        'id': video_id,
        'likes':video.likes,
        'unlikes':video.dislikes,
        'message': "<i class='material-icons red-text center'>thumb_down</i>+1",
        'success':False}
        #'roles' : ['Admin','User']}
        return JsonResponse(responseData)
        #return redirect('/tube/video/{}/'.format(video_id))

    elif video in videos_liked and video not in videos_unliked:
        video.likes -= 1
        video.dislikes +=1
        video.save()
        user.videos_unliked.add(video)
        user.videos_liked.remove(video)
        user.save()
        #messages.error(request,"You unliked this video")
        responseData = {
        'id': video_id,
        'likes':video.likes,
        'unlikes':video.dislikes,
        'message': "<i class='material-icons red-text center'>thumb_down</i>+1",
        'success':False}
        #'roles' : ['Admin','User']}
        return JsonResponse(responseData)
        #return redirect('/tube/video/{}/'.format(video_id))
    else:
        #messages.error(request,"You already unliked this video")
        video.dislikes -= 1
        video.save()
        user.videos_unliked.remove(video)
        user.save()
        responseData = {
        'id': video_id,
        'likes':video.likes,
        'unlikes':video.dislikes,
        'message': "<i class='material-icons green-text center'>thumb_down</i>-1",
        'success':True}
        #'roles' : ['Admin','User']}
        return JsonResponse(responseData)
        #return redirect('/tube/video/{}/'.format(video_id))


    #return JsonResponse({'received data': 'Hello'})


from django.utils.safestring import mark_safe
import json




def room(request, room_name):
    return render(request, 'tube/video_detail.html', {
        'room_name_json': mark_safe(json.dumps(room_name))
    })




