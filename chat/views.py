from django.shortcuts import render,redirect,reverse
from django.views import View
from django.db.models import Case, When, Value, BooleanField,Q

from blog.models import NotificationModel
from account.models import Follow,User
from chat.models import ChatModel
from chat.forms import ChatModelForm

class ChatView(View):
    def get(self,request):
        form = ChatModelForm(request.POST)
        follow_objects_annotated = User.objects.annotate(
            is_followed=Case(
                When(user_info__youser=self.request.user, then=Value(True)),
                default=Value(False),
                output_field=BooleanField(),
            )
        )
        
        # Filter the annotated queryset to get the follow objects
        follow_list = follow_objects_annotated.filter(is_followed=True)
        context = {
            'form':form,
            'follow_list':follow_list,
        }
        return render(request,'chat.html',context)

    #def post(self,request):
    #    return render(request,'chat.html')



class MessageView(View):
    def get(self,request,userid):
        follow_objects_annotated = User.objects.annotate(
            is_followed=Case(
                When(user_info__youser=self.request.user, then=Value(True)),
                default=Value(False),
                output_field=BooleanField(),
            )
        )
        
        # Filter the annotated queryset to get the follow objects
        follow_list = follow_objects_annotated.filter(is_followed=True)
        #chat = ChatModel.objects.filter(Q(user = self.request.user) & Q(other_chat_user__id = userid)).order_by('created_at')
        chat = ChatModel.objects.filter(Q(user=self.request.user,other_chat_user__id=userid)|Q(user__id=userid,other_chat_user=self.request.user)).order_by('created_at')
        #chat = ChatModel.objects.all().order_by('created_at')
        context = {
            #'list_of_users': Follow.objects.all(),
            'chat':chat,
            'follow_list':follow_list,
            'form':ChatModelForm(request.POST),
        }
        return render(request,'chat.html',context)

    def post(self,request,userid):
        form = ChatModelForm(request.POST)
        if form.is_valid():
            form = form.save(commit = False)
            form.user = self.request.user
            form.other_chat_user = User.objects.get(id = userid)
            form.save()
            return redirect(reverse('chat:MessageView',args=(userid,)))
        context = {
            'form':ChatModelForm(request.POST)
        }
        return render(request,'chat.html',context)
