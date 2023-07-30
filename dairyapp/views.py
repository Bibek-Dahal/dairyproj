
from typing import Any, Dict
from django.db import models
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views import View
from django.http import Http404, HttpResponseRedirect,HttpResponseForbidden
from dairyapp.models import *
from .forms import *
from django.views.generic import ListView
from django.views.generic.edit import UpdateView,DeleteView,CreateView
from django.shortcuts import get_object_or_404
# Create your views here.
from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.db.models import Q
import datetime
from django.db.models import Avg,Sum
from .decorators import verified_dairy_user
from django.core.exceptions import PermissionDenied



@method_decorator(login_required(login_url='account_login'),name="dispatch")
@method_decorator(verified_dairy_user,name="dispatch")
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
@method_decorator(verified_dairy_user,name="dispatch")
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
@method_decorator(verified_dairy_user,name="dispatch")
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
@method_decorator(verified_dairy_user,name="dispatch")
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
@method_decorator(verified_dairy_user,name="dispatch")
class DeleteFatRate(DeleteView):
    print("delete view called")
    model = FatRate
    success_url = reverse_lazy("dairyapp:fat_list")
    

    # def get_queryset(self):
    #     return super().get_queryset().filter(id=self.kwargs['pk'],dairy__user=self.request.user)
    
       
#Dairy views
@method_decorator(login_required(login_url='account_login'),name="dispatch")
@method_decorator(verified_dairy_user,name="dispatch")
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
@method_decorator(verified_dairy_user,name="dispatch")
class ListMilkReports(ListView):
    model = MilkRecord
    context_object_name = "milkrecords"
    # paginate_by = 10

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['dairy'] = self.kwargs['dairy']
        dairy = get_object_or_404(Dairy,name=self.kwargs['dairy'],user=self.request.user)
        context['members'] = dairy.members.all()
        return context
    
    def get_queryset(self):
        
        # return super().get_queryset()
        dairy = get_object_or_404(Dairy,name=self.kwargs['dairy'])
        return MilkRecord.objects.filter(dairy=dairy,dairy__user=self.request.user)


@method_decorator(login_required(login_url='account_login'),name="dispatch")
@method_decorator(verified_dairy_user,name="dispatch")
class CreateMilkRercord(View):
    def get(self,request,*args,**kwargs):
            """
            user can add milk record if he is verified user
            """
            try:
                print(kwargs['dairy'])
                dairy = Dairy.objects.get(name=kwargs['dairy'],user=self.request.user)
                print("dairy",dairy)
                # dairy =get_object_or_404(Dairy,name=kwargs['dairy'],user=self.request.user)
                if dairy.is_verified:
                    print(dairy.members.all())
                    form = CreateMilkRecordForm(dairy)
                    
                    return render(request,'dairyapp/milkrecord_create.html',{'form':form})
                else:
                    print('inside else')
                    #  raise HttpResponseForbidden("Sorry,")
                    raise PermissionDenied()
            except Exception as e:
                 raise e
        
        
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
@method_decorator(verified_dairy_user,name="dispatch")
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

    
   
@method_decorator(login_required(login_url='account_login'),name="dispatch")
@method_decorator(verified_dairy_user,name="dispatch")
class ListMemberMilkRecord(ListView):
    model = MilkRecord
    context_object_name = "milkrecords"
    template_name = "dairyapp/member_milkrecord_list.html"

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['dairy'] = self.kwargs['dairy']
        context['id'] = self.kwargs['id']
        context['start_date'] = self.request.GET.get('start_date')
        context['end_date'] = self.request.GET.get('end_date')
        context['shift'] = self.request.GET.get('shift')
        context['date'] = self.request.GET.get('date')
        context['count'] = self.kwargs['count']
        context['total_milk_wieght'] = self.kwargs['total_milk_wieght']
        context['avg_fat'] = round(self.kwargs['avg_fat'],3)
        context['total_price'] = self.kwargs['total_price']
        dairy = get_object_or_404(Dairy,name=self.kwargs['dairy'],user=self.request.user)
        context['members'] = dairy.members.all()
        

        
        return context
    
        
    
    
    
    def get_queryset(self):
        request = self.request
        print("date",self.request.GET.get('date'))
        print("name",self.request.GET.get('name'))
        shift = request.GET.get('shift')
        date = request.GET.get('date')
        start_date = request.GET.get('start_date')
        print("start_date",start_date)
        end_date = request.GET.get('end_date')
        print("end_date",end_date)
        
        # return super().get_queryset()
        user = get_object_or_404(User,id=self.kwargs['id'])
        dairy = get_object_or_404(Dairy,name=self.kwargs['dairy'])
        queryset  = MilkRecord.objects.all()
        filters = Q(dairy=dairy,dairy__user=self.request.user,user=user)
        # return MilkRecord.objects.filter(dairy=dairy,dairy__user=self.request.user,user=user)
    
        if shift:
              print("inside shift--------------")
              print("shift",shift)
              filters &= Q(shift=shift)

        if date:
             filters &= Q(date=date)

        if start_date and end_date:
            queryset = queryset.filter(date__gte=start_date, date__lte=end_date)
        elif start_date:
            filters &= Q(date__gte=start_date)
        elif end_date:
            filters &= Q(date__lte=end_date)
            
             

        # if start_date and end_date:
        #      filters &= Q(date>=start_date and date<=end_date)
        


        def seedMilkRecord():
             print("inside milk record")
             import random
             i = 1
             for i in range(1,31):
                  date = f"2023-07-{i}"
                  if i<9:
                       date = f"2023-07-0{i}"
                  MilkRecord.objects.create(
                       dairy = dairy,
                       user = user,
                       shift = "night",
                       milk_weight = random.randint(1,20),
                       milk_fat = random.randint(1,6),
                       date = date
                  )
        # seedMilkRecord()
        qs = queryset.filter(filters)
        count = qs.count()
        print("count",count)
        self.kwargs['count'] = count
        self.kwargs['total_milk_wieght'] = 0
        self.kwargs['avg_fat'] = 0
        self.kwargs['total_price'] = 0

        if shift:
            
            milk_wg = qs.aggregate(Sum("milk_weight")).get('milk_weight__sum')
            avg_fat = qs.aggregate(Avg("milk_fat")).get('milk_fat__avg')
            self.kwargs['total_milk_wieght'] = milk_wg
            self.kwargs['avg_fat'] = avg_fat
            print("milk_weight",milk_wg)
            print("average_fat",avg_fat)
            fat_rate = FatRate.objects.filter(dairy__user=self.request.user,dairy=dairy)

            if fat_rate.exists():
                print("fat_fate",fat_rate[0].fat_rate)
                total_price = fat_rate[0].fat_rate*milk_wg*avg_fat
                self.kwargs['total_price'] = total_price
                # print("total price==",total_price)
                pass


             
        return queryset.filter(filters)
    

