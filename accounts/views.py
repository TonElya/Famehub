from django.shortcuts import render
from django.contrib.auth.models import Group
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
# Create your views here.
from django.shortcuts import render, redirect,HttpResponse,HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.contrib.auth.models import Group, User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from django.views.generic import View
#from tastypie.models import ApiKey
from django.db import models
from .forms import CustomUserCreationForm,PatronCreationForm,PatronChangeForm
from django.contrib.auth import views
#from tastypie.models import create_api_key
import os
import binascii
from django.template.loader import render_to_string
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from .models import Patron
import json
import string
import random
from django.contrib.auth.hashers import make_password
from .models import CustomUser
from datetime import timedelta
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
#import pyrebase
import json
import os
from django.views.generic.detail import DetailView
from django.utils import timezone
#import online_users.models
from datetime import timedelta
import datetime
from django.views.generic import ListView
from tube.models import Video


"""config = {"apiKey": "AIzaSyCvL086JynApAhRlwALt5TnRkuh6ojKIA4",  "authDomain": "pywe-92968.firebaseapp.com",
            "databaseURL": "https://pywe-92968.firebaseio.com",  "storageBucket": "pywe-92968.appspot.com",
           "serviceAccount": "/home/Learn/mysite/static/fireapi/pywe-92968-a64c4a2fa3da.json"}
firebase = pyrebase.initialize_app(config)
#"projectId": "pywe-92968",
#"messagingSenderId": "591931135706"}
#"serviceAccount": "/home/theoelia/PycharmProjects/face_recog/pywe-92968-a64c4a2fa3da.json",}
firebase = pyrebase.initialize_app(config)

storage = firebase.storage()

auth = firebase.auth()
"""
class pywebase:
# authenticate a user
    def get_token(self,email="gregeace@gmail.com",password="hello222"):
        user = auth.sign_in_with_email_and_password(email,password )
        token = user['idToken']
        return token

    def upload_photo(self,firebase_path, file_path, token):
        try:
            storage.child(firebase_path).put(file_path,token)
        except Exception as e:
            content = e
            error = {"code": 401, "status": False, "error":content,"url":None}
            return error
        else:
            url = storage.child(firebase_path).get_url(token)
            success = {"url":url,"status":True,"code":201}
            return success


class CreateUserView(TemplateView):
    var1 = 0
    var2 = 1
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('home')
    template_name = 'signup.html'

    def get(self, request):
        form = self.form_class
        args={'form':form}
        return render(request,self.template_name, {'form':form})

    def post(self,request):
        form = self.form_class(request.POST)
        if form.is_valid():
            group = Group.objects.get(name='Patrons')
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            email = form.cleaned_data['email']
            user = self.form_valid(form)
            send_mail(
		    'Subject here',
		    'Here is the message.',
		    'pythonwithelli@gmail.com',
		    [email],
		    fail_silently=False,
            )
            if not self.is_member(user.id, 'Patrons'):
                user.groups.add(group)
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')
        args = {'form': form}
        return render(request, self.template_name, args)


    #def get(self,request):
    #    pass

    def get_context_data(self, **kwargs):
        context = super(CreateUserView, self).get_context_data(**kwargs)
        context.update({'var1': self.var1, 'var2': self.var2})
        return context
    #g = Group.objects.get(name='Retailers')
    #users = CustomUser.objects.all()
    #for u in users:
    #    g.user_set.add(u)
    def create_group(group_name):
        group = Group(name=group_name)
        group.save()

    def add_user_to_group(group_name,user_id):
        group = Group.objects.get(name='Retailers')
        #users = CustomUser.objects.all()
        user = CustomUser.objects.get(pk=user_id)
        user.groups.add(group)        # user is now in the "group_name" group

    def is_member(self,user_id,group_name):
        user = CustomUser.objects.get(pk=user_id)
        return user.groups.filter(name=group_name).exists()

    def is_in_multiple_groups(user_id,list_of_groups):
        user = CustomUser.objects.get(pk=user_id)
        return user.groups.filter(name__in=list_of_groups).exists()

    def form_valid(self, form):
        user = form.save()
        return user

    #def save(self, commit=True):
     #       user = super().save
      #      user.is_staff = False
       #     user.save()
        #    return user
    #g = Group.objects.get(name='Retailers')
    #users = CustomUser.objects.all()
    #for u in users:
    #    g.user_set.add(u)
    #template_name = 'registration/login.html'


class CreatePatronView(ListView):
    form_class = PatronCreationForm
    success_url = reverse_lazy('home')
    template_name = 'signup.html'

    def get(self, request):
        form = self.form_class
        args = {'form': form,"warning":"Provide a valid email"}
        return render(request,self.template_name,args)

    def post(self,request):
        pywebaseobj = pywebase()
        form = self.form_class(request.POST,request.FILES)
        if form.is_valid():
            group = Group.objects.get(name='Patrons')
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            email = form.cleaned_data['email']
            #img = request.FILES['user_img']
            user = self.form_valid(form)
            mytoken = binascii.hexlify(os.urandom(30)).decode()
            email_token = user.email_token

              #  messages.success(request, e)
             #   return redirect('signup')
            #else:
            #img = request.FILES['user_img']
            #user.user_img = img
            #user.save()

            ApiKey.objects.create(key=mytoken, user=user)
            #user.save()
            if not self.is_member(user.id, 'Patrons'):
                user.groups.add(group)
                user.is_patron = True
                user.save()
            msg_plain = render_to_string('welcome_email.txt', {'api_token': mytoken,'username':username,'email_token':email_token,'verification_link':"learn.pythonanywhere.com/accounts/email_verification/{}".format(email_token),'home_url':"learn.pythonanywhere.com"})
            msg_html = render_to_string('welcome_email.html', {'api_token': mytoken,'username':username, 'email_token':email_token,'verification_link':"learn.pythonanywhere.com/email_verification/{}".format(email_token),'home_url':"learn.pythonanywhere.com"})
            subject = "Welcome {}".format(username)
            send_mail(
            subject,
            msg_plain,
            'pythonwithellie@gmail.com',
            [email],
            html_message=msg_html,
            fail_silently=False,)
            try:
                img = user.user_img
            except Exception as e:
                pass
            else:
                pywebaseobj.upload_photo(firebase_path="users/{}".format(user.username),file_path =img,token = pywebaseobj.get_token())
            messages.success(request, "We have sent you an email. Check for your secret key.")
	    #subject, from_email, to = 'Welcome', 'pythonwithellie@gmail.com', email
	    #text_content = """""".format(mytoken)
	    #msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
	    #msg.attach_alternative(html_content, "text/html")
	    #msg.send()


		#models.signals.post_save.connect(create_api_key, sender=user)
            #user = authenticate(username=username, password=password)
            #login(request, user)
            return redirect('signup')

        args = {'form': form,"warning":"Provide a valid email"}
        return render(request, self.template_name, args)


    def create_group(group_name):
        group = Group(name=group_name)
        group.save()

    def add_user_to_group(group_name,user_id):
        group = Group.objects.get(name=group_name)
        #users = CustomUser.objects.all()
        user = CustomUser.objects.get(pk=user_id)
        user.groups.add(group)        # user is now in the "group_name" group

    def is_member(self,user_id,group_name):
        user = CustomUser.objects.get(pk=user_id)
        return user.groups.filter(name=group_name).exists()

    def is_in_multiple_groups(user_id,list_of_groups):
        user = CustomUser.objects.get(pk=user_id)
        return user.groups.filter(name__in=list_of_groups).exists()

    def form_valid(self, form):
        user = form.save()
        return user
    def get_context_data(self, **kwargs):
        context = super(CreatePatronView, self).get_context_data(**kwargs)
        context.update({'success': "We have sent you an email. Check for your secret key."})
        return context


    # g = Group.objects.get(name='Retailers')
    # users = CustomUser.objects.all()
    # for u in users:
    # g.user_set.add(u)


    #g = Group.objects.get(name='Retailers')
    #users = CustomUser.objects.all()
    #for u in users:
    #    g.user_set.add(u)
    #template_name = 'registration/login.html'
def email_verification(request, email_token=""):
    form_class = PatronCreationForm
    #success_url = reverse_lazy('home')
    template_name = 'email_verification.html'
    form = form_class
    args = {'form': form}
    try:
    	user = Patron.objects.get(email_token=email_token)
    except:
        messages.error(request, "Please you provided a wrong token.")
        return redirect('signup')
    else:
        user.email_confirmed = 1
        user.is_active = True
        user.is_staff = True
        user.save()
        #user = authenticate(username=user.username, password=user.password)
        login(request, user)
        messages.success(request, "Thanks for verifying your email.")
        return redirect("login")#HttpResponse(user)
    return render(request, template_name, args)

def para(request):
    template_name = 'para.html'
    return render(request,template_name)

def email_us(request):
    message = request.POST['message']
    email = request.POST['email']
    name = request.POST['name']
    subject = "Email from {}".format(name)
    try:
    	send_mail(subject,message+" From {}".format(email),'pythonwithellie@gmail.com',["theophylusnhutiphapha@gmail.com"],
			fail_silently=False,
			)

    except:
        messages.success(request, "Hi {}, There was a problem sending your message".format(name))
        return redirect('home')
    else:
        messages.success(request, "Hi {}, Your message has been sent to the team.".format(name))
        return redirect('home')

def create_users(request):
#    info = open("/home/Learn/mysite/all_users.json", "r+")
    json_data = {"usernames": ["TheoElia1", "Josefina"],"emails": ["gregeace@gmail.com", "effieboat@gmail.com"],"email_conf": [1, 1],"tokens": ["pbkdf2:sha256:50000$tUY4D9DS$1f8e6b3d40e97a17423999af2bd12b22b24d53db2071cf4a3c98c6cbe91a278c",
"pbkdf2:sha256:50000$3O7Z811p$9ce940deffb658190f102509a1fbe40eb21e0e73c5388cb58f8521cf9ec4a60a"],"resets": ["", ""]}
    #data = info.read()
    #json_data = json.loads(data)
    usernames = json_data['usernames']
    email_conf = json_data['email_conf']
    emails = json_data['emails']
    email_tokens = json_data['tokens']
    reset_tokens = json_data['resets']
    counter = 0
    my_user = []
    for each_user in usernames:
        chars=string.ascii_lowercase + string.digits
        password = ''.join(random.choice(chars) for _ in range(15))

        dj_password = make_password(password)
        obj = Patron(username=usernames[counter],password=dj_password,email=emails[counter],email_confirmed=email_conf[counter],email_token=email_tokens[counter],reset_token=reset_tokens[counter])
        if obj.email_confirmed == 1:
	        obj.is_active = True
        else:
	        obj.is_active = False
        obj.save()
        group = Group.objects.get(name='Patrons')
        obj.groups.add(group)
        obj.is_patron = True
        obj.save()
        my_user.append((each_user, password))
        mytoken = binascii.hexlify(os.urandom(30)).decode()
        ApiKey.objects.create(key=mytoken, user=obj)
        # Sending mail to user after successful creation
        msg_plain = render_to_string('email.txt', {'password':password,'api_token': mytoken,'username':usernames[counter],'email_token':email_tokens[counter],'home_url':'learn.pythonanywhere.com','verification_link':"learn.pythonanywhere.com/accounts/email_verification/{}".format(email_tokens[counter])})
        msg_html = render_to_string('email.html', {'password':password,'api_token': mytoken,'username':usernames[counter], 'email_token':email_tokens[counter],'home_url':'learn.pythonanywhere.com','verification_link':"learn.pythonanywhere.com/accounts/email_verification/{}".format(email_tokens[counter])})
        subject = "Hello Pywean, Some Great Changes."
        send_mail(
        subject,
        msg_plain,
        'pythonwithellie@gmail.com',
        [emails[counter]],
        html_message=msg_html,
        fail_silently=False,)
        add_image(usernames[counter]+".gif",obj)
        #messages.success(request, "We have sent you an email. Check for your secret key.")
        counter = counter + 1
    return HttpResponse(my_user)

def reset_password(request, reset_token):
    form_class = PatronChangeForm
    success_url = reverse_lazy('home')
    template_name = 'reset_password.html'
    form = form_class
    if request.method == "GET":
        args = {'form': form,"warning":"You provided a wrong token",'reset_token':reset_token}
        try:
            user = CustomUser.objects.get(reset_token=reset_token)
        except:
	        return render(request, template_name, args)
        else:
            args = {'form': form,"warning":"Please enter a new password",'reset_token':reset_token}
            return render(request, template_name, args)

    if request.method == "POST":
        args = {'form': form,"warning":"You provided a wrong token, please use correct token",'reset_token':reset_token}
        try:
	        user = CustomUser.objects.get(reset_token=reset_token)
        except:
            return render(request, template_name, args)
        else:
            user.set_password(request.POST['password1'])
            #user.reset_token = ""
            user.save()
	    	#user = authenticate(username=user.username, password=user.password)
            #login(request, user)
            messages.success(request, "Hi, Your password has been reset, login now.")
            return redirect('login')
        args = {'form': form,"warning":"Please make sure the password obeys the listed rules"}
        return render(request, template_name, args)
    return render(request, template_name, args)
    	    #HttpResponse(user)



class UserListView(ListView):
    model = CustomUser
    template_name = "accounts/home.html"

    def get_context_data(self, **kwargs):
        context = super(UserListView, self).get_context_data(**kwargs)
        context['now'] = timezone.now()

        context['staff'] = CustomUser.objects.filter(is_superuser=True)
        context['recent_vids'] = Video.objects.all()
        #context['product_list'] = Product.objects.filter(reviewed=True)
        return context
    def get_queryset(self):
            return CustomUser.objects.all()

def get_time_diff(user):
    if user.last_activity:
        now = datetime.datetime.utcnow().replace(tzinfo=utc)
        timediff = now - user.last_activity
        return timediff.total_seconds()



class UserDetailView(DetailView):
    model = CustomUser
    template_name = "accounts/home_detail.html"
    def get_context_data(self, **kwargs):
        context = super(UserDetailView, self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

    def get_queryset(self):
            return CustomUser.objects.all()

def add_image(filename,obj):
    #from io import BytesIO
    #from urllib.request import urlopen
    #from django.core.files import File
    # url, filename, model_instance assumed to be provided
    #response = urlopen("https://www.pythonanywhere.com/user/Learn/files/home/Learn/mysite/static/images/profile_placeholder.gif")
    #io = BytesIO(response.read())
    #obj.user_img.save(filename, File(io))

    from urllib.parse import urlparse
    import requests
    from django.core.files.base import ContentFile

    img_url = ""
    name = urlparse(img_url).path.split('/')[-1]
    # set any other fields, but don't commit to DB (ie. don't save())
    response = requests.get(img_url)
    if response.status_code == 200:
        obj.user_img.save(name, ContentFile(response.content), save=True)





