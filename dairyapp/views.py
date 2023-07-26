
from typing import Any, Dict
from django.db import models
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views import View
from django.http import Http404, HttpResponseRedirect
from dairyapp.models import *
from .forms import *
from django.views.generic import ListView
from django.views.generic.edit import UpdateView,DeleteView,CreateView
from django.shortcuts import get_object_or_404
# Create your views here.
from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

@method_decorator(login_required(login_url='account_login'),name="dispatch")
class HomeView(View):
    def get(self,request):
        auser = get_user_model()
        print("user model",auser)
        user = self.request.user
        print("inside home view")
        print(user)
        dairies = Dairy.objects.filter(user = user)
        print(dairies)
        if Dairy.objects.filter(user = user):
            fat_rates = FatRate.objects.filter(dairy__in = dairies)
            print(fat_rates)
            # dairy = Dairy.objects.get(name = self.request.GET.get('dairy'))
            # milk_records = MilkRecord.objects.filter(dairy=dairy,user=user)

            print("======")
            print("dairies",dairies)

            context = {
                'dairies':dairies,
                # "milk_records":milk_records,
                # 'fat_rates':fat_rates
            }
            return render(request,"dairyapp/index.html",context)

        else:
            # pass

            dairies_list = Dairy.objects.filter()
            return render(request,"dairyapp/index.html")

@method_decorator(login_required(login_url='account_login'),name="dispatch")
class FatListView(ListView):
    model = FatRate
    paginate_by = 100
    template_name = "fatrate_list"
    context_object_name = "fatrates"

    def get_queryset(self):
        qs = super().get_queryset().filter(dairy__user = self.request.user)
        print(qs)
        return qs
    
class EditFatView(UpdateView):
    pass

@method_decorator(login_required(login_url='account_login'),name="dispatch")
class CreateFatView(View):
    def get(self,request,*args,**kwargs):
        print(self.request.user)
        dairies = Dairy.verObs.filter(user=self.request.user)
        print(dairies)
        form = CreateFatForm(self.request,initial={'fat_rate':20})
        print(form.fields['dairy'])
        
        return render(request,"dairyapp/create_fat.html",{'form':form})

    def post(self,request,*args,**kwargs):
        form = CreateFatForm(self.request,request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("dairyapp:fat_list"))
        return render(request,"dairyapp/create_fat.html",{'form':form})


@method_decorator(login_required(login_url='account_login'),name="dispatch")
class UpdateFatView(View):
    def get(self,request,*args,**kwargs):

            fatrate =get_object_or_404(FatRate,id=self.kwargs['id'],dairy__user=self.request.user)
            # fatrate = FatRate.objects.get(id=self.kwargs['id'])
            # if fatrate and fatrate.dairy.user == request.user:
                # dairy = Dairy.objects.get()
            form = CreateFatForm(self.request,instance=fatrate)
            
            return render(request,'dairyapp/edit_fat.html',{'form':form})
            # else:
            #     # return HttpResponse("404")
        
        
    def post(self,request,*args,**kwargs):
            print("inside post")
            fatrate = get_object_or_404(FatRate,id=self.kwargs['id'],dairy__user=self.request.user)
            # FatRate.objects.get(id=self.kwargs['id'])
            # if fatrate and fatrate.dairy.user == request.user:
            print("inside if")
            # dairy = Dairy.objects.get()
            form = CreateFatForm(self.request,request.POST,instance=fatrate)
            if form.is_valid():
                print("inside valid data")
                form.save()
                return HttpResponseRedirect(reverse("dairyapp:fat_list"))
            print("inside else")
            return render(request,'dairyapp/edit_fat.html',{'form':form})
            # else:
            #     # return HttpResponse("404")
            #     raise Http404("Poll does not exist")
            
@method_decorator(login_required(login_url='account_login'),name="dispatch")
class DeleteFatRate(DeleteView):
    print("delete view called")
    model = FatRate
    success_url = reverse_lazy("dairyapp:fat_list")
    

    # def get_queryset(self):
    #     return super().get_queryset().filter(id=self.kwargs['pk'],dairy__user=self.request.user)
    
       
#Dairy views
@method_decorator(login_required(login_url='account_login'),name="dispatch")
class CreateDairyView(CreateView):
     model = Dairy
     form_class = CreateDairyForm
     template_name_suffix = '_create_form'

     def form_valid(self, form):
        """If the form is valid, save the associated model."""
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        return super().form_valid(form)

@method_decorator(login_required(login_url='account_login'),name="dispatch") 
class UpadteDairyView(UpdateView):
     model = Dairy
     form_class = CreateDairyForm
     template_name = 'dairyapp/dairy_edit_form.html'
    

     def get_queryset(self) -> QuerySet[Any]:
          return super().get_queryset().filter(user=self.request.user)
    

@method_decorator(login_required(login_url='account_login'),name="dispatch")
class ListMilkReports(ListView):
    model = MilkRecord
    context_object_name = "milkrecords"

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['dairy'] = self.kwargs['dairy']
        return context
    
    def get_queryset(self):
        
        # return super().get_queryset()
        dairy = get_object_or_404(Dairy,name=self.kwargs['dairy'])
        return MilkRecord.objects.filter(dairy=dairy,dairy__user=self.request.user)


@method_decorator(login_required(login_url='account_login'),name="dispatch")
class CreateMilkRercord(View):
    def get(self,request,*args,**kwargs):
            """
            user can add milk record if he is verified user
            """
            try:
                dairy = Dairy.verObs.get(name=kwargs['dairy'],user=self.request.user)
                # dairy =get_object_or_404(Dairy,name=kwargs['dairy'],user=self.request.user)
                print(dairy.members.all())
                form = CreateMilkRecordForm(dairy)
                
                return render(request,'dairyapp/milkrecord_create.html',{'form':form})
            except:
                 raise Http404("Dairy Not Found")
        
        
    def post(self,request,*args,**kwargs):
            print("inside mike record post methos")
            dairy =get_object_or_404(Dairy,name=kwargs['dairy'],user=self.request.user)
            form = CreateMilkRecordForm(dairy,request.POST)
            if form.is_valid():
                print(request.POST)
                print("inside valid data")
                miklrecord = form.save(commit=False)
                print("milkrec user",miklrecord.user)
                miklrecord.dairy = dairy
                miklrecord.save()
                return HttpResponseRedirect(reverse("dairyapp:milk_record",kwargs={'dairy':self.kwargs['dairy']}))
            return render(request,'dairyapp/milkrecord_create.html',{'form':form})

    
@method_decorator(login_required(login_url='account_login'),name="dispatch")
class UpdateMilkRercord(View):
    def get(self,request,*args,**kwargs):
            """
            user can add milk record if he is verified user
            """
            try:
                id = self.kwargs['id']
                print("id",id)
                dairy = Dairy.verObs.get(name=kwargs['dairy'],user=self.request.user)
                print("dairy",dairy)
                milkrecord = MilkRecord.objects.get(id=id)
                print("milkrec",milkrecord)
                # dairy =get_object_or_404(Dairy,name=kwargs['dairy'],user=self.request.user)
                print(dairy.members.all())
                form = CreateMilkRecordForm(dairy,instance=milkrecord)
                
                return render(request,'dairyapp/milkrecord_create.html',{'form':form})
            except:
                 raise Http404("Page Not Found")
        
        
    def post(self,request,*args,**kwargs):
            id = self.kwargs['id']
            print("inside mike record post methos")
            dairy =get_object_or_404(Dairy,name=kwargs['dairy'],user=self.request.user,is_verified=True)
            milkrecord = MilkRecord.objects.get(id=id)
            form = CreateMilkRecordForm(dairy,request.POST,instance = milkrecord)
            if form.is_valid():
                print(request.POST)
                print("inside valid data")
                miklrecord = form.save(commit=False)
                print("milkrec user",miklrecord.user)
                miklrecord.dairy = dairy
                miklrecord.save()
                return HttpResponseRedirect(reverse("dairyapp:milk_record",kwargs={'dairy':self.kwargs['dairy']}))
            return render(request,'dairyapp/milkrecord_edit.html',{'form':form})

    
