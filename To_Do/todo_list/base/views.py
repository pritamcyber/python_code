from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
# from ..todo_list.settings import LOGIN_URL
from .models import Task
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView


from django.views.generic.edit import FormView,CreateView,DeleteView,UpdateView

from django.urls import reverse_lazy
from django.contrib.auth.mixins  import LoginRequiredMixin
from django.views.generic import View


from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from django.contrib.auth.views import LogoutView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login



class TaskLogout(View):
    template_name = 'logout.html'
    def get(self, request):
        logout(request)
        return HttpResponseRedirect('login')
# Create your views here.
class TaskList(LoginRequiredMixin,ListView):
    template_name = 'task_list.html'
    context_object_name  = 'task'
    model = Task
    def get_context_data(self, **kwargs) :
        
        context = super().get_context_data(**kwargs)
        # context["color"] =  'red' this is how you can add more detail  to your  object
        context['task'] = context['task'].filter(user = self.request.user)
        context['count'] = context['task'].filter(complete = False).count()

        search_input =  self.request.GET.get('search-area') or ''
        if search_input:
            context['task'] = context['task'].filter(title__startswith = search_input,title__icontains = search_input )
        context['search_input'] = search_input
        
        return context 

class RegisterPage(FormView):
    template_name  = 'register.html'
    form_class =  UserCreationForm
    redirect_authenticated_user = True
    success_url  = reverse_lazy('tasks')
    def form_valid(self,form):
        user =  form.save()
        
        if user is not None:
            login(self.request,user)
            

            
        
        return super(RegisterPage,self).form_valid(form)
    def get(self):
        if self.request.user.is_authenticated:
            return redirect('tasks')
    # def form.def form_valid(self, form):
    #     form
    #     return super().form_valid(form)
    

    
    
class TaskDetail(LoginRequiredMixin,DetailView):
    model = Task
    context_object_name  = 'tasks'
    template_name  = 'task_detail.html'
    


class TaskCreate(LoginRequiredMixin,CreateView):
    model  = Task
    fields  = ['title','description','complete']
    template_name = 'task_create.html'
    success_url  = reverse_lazy('tasks')
    
    def form_valid(self,form):
        form.instance.user = self.request.user
        return super(TaskCreate,self).form_valid(form)
    
    
class TaskUpdate(LoginRequiredMixin,UpdateView):
    model  = Task
    fields  = ['title','description','complete']

    template_name  = 'task_update.html'
    success_url = reverse_lazy('tasks')
    

class TaskDelete(LoginRequiredMixin,DeleteView):
    model  = Task
    context_object_name  = 'task'
    template_name = 'task_confirm_delete.html'
    success_url = reverse_lazy('tasks')


class CustomeLoigniew(LoginView):
    model =  User
    template_name ='login.html'
    fields = '__all__'
    redirect_authenticated_user = True
    success_url  = reverse_lazy('')

    def get_success_url(self):
        return reverse_lazy('tasks')