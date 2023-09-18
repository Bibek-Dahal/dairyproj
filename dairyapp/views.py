import io
from django.db.models.query import QuerySet
from django.shortcuts import render,redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.http import Http404, HttpResponse, HttpResponseRedirect,HttpResponseForbidden,HttpResponseNotFound
from dairyapp.mixins import PaginationMixin
from dairyapp.models import *
from .forms import *
from django.views.generic import ListView,DetailView
from django.views.generic.edit import UpdateView,DeleteView,CreateView
from django.shortcuts import get_object_or_404
from django.contrib import messages
# Create your views here.
from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db.models import Avg,Sum
from .decorators import verified_dairy_user
import uuid
import requests as req
from django.views.generic import View
from django.utils.translation import gettext_lazy as _
from django.template.loader import render_to_string
from weasyprint import HTML
from utils.dairyapp.commonutils import sendMial
from django.conf import settings
from django.forms import formset_factory


@method_decorator(login_required(login_url='account_login'),name="dispatch")
# @method_decorator(verified_dairy_user,name="dispatch")
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
        dairies = Dairy.objects.filter(user=self.request.user)
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
# @method_decorator(verified_dairy_user,name="dispatch")
class CreateDairyView(CreateView):
     model = Dairy
     form_class = CreateDairyForm
     template_name_suffix = '_create_form'

     def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        uid = uuid.uuid4()
        context['uid'] = uid
        print("uid",uid)
        return context

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
    

     def get_queryset(self):
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
    
    CreateMilkRecordFormSet = formset_factory(CreateMilkRecordForm,max_num=10)
    def get(self,request,*args,**kwargs):
            """
            user can add milk record if he is verified user
            """
            try:
                print(kwargs['dairy'])
                dairy = Dairy.objects.get(name=kwargs['dairy'],user=self.request.user)
                user = User.objects.get(id=kwargs['id'])
                print("dairy===============",dairy)
                
                formset = self.CreateMilkRecordFormSet(form_kwargs={'dairy':dairy,'user':user,})

                # formset = self.CreateMilkRecordFormSet(initial=[
                #     {
                #         'user':user,
                #         'dairy':dairy
                #     }
                # ])
                    
                return render(request,'dairyapp/milkrecord_create.html',{'formset':formset,'user':user})
                # else:
                #     print('inside else')
                #     #  raise HttpResponseForbidden("Sorry,")
                #     raise PermissionDenied()
            except Dairy.DoesNotExist:
                raise Http404
                 
            except User.DoesNotExist:
                raise Http404
        
        
    def post(self,request,*args,**kwargs):
            print("inside mike record post methos")
            dairy =get_object_or_404(Dairy,name=kwargs['dairy'],user=self.request.user)
            user = get_object_or_404(User,id=kwargs['id'])
            formset = self.CreateMilkRecordFormSet(request.POST,form_kwargs={'dairy':dairy,'user':user})
            if formset.is_valid():
                print(request.POST)
                print("inside valid data")
                # milk_records  = formset.save(commit=False)

                # bulk_data = []
                for milk_record in formset.forms:
                #     print("inside milkrecord formset for loop")
                #     shift = milk_record.cleaned_data['shift']
                #     user = milk_record.cleaned_data['user']
                #     milk_weight = milk_record.cleaned_data['milk_weight']
                #     date = milk_record.cleaned_data['date']
                #     milk_fat = milk_record.cleaned_data['milk_fat']
                #     dairy = dairy
                #     obj = MilkRecord(
                #          shift=shift,
                #          user=user,
                #          milk_weight=milk_weight,
                #          milk_fat=milk_fat,
                #          date=date,
                #          dairy=dairy
                #     )
                #     bulk_data.append(obj)
                    new_record = milk_record.save(commit=False)
                    new_record.dairy = dairy
                    new_record.save()
                # print("bulk data=====",bulk_data)
                # MilkRecord.objects.bulk_create(bulk_data)
                # print("milkrec user",miklrecord.user)
                # miklrecord.dairy = dairy
                # miklrecord.save()
                messages.success(request, _("Record added successfully"))
                return HttpResponseRedirect(reverse("dairyapp:member_milk_record",kwargs={'dairy':self.kwargs['dairy'],'id':self.kwargs['id']}))
            print("invalid form data++++++")
            print(formset)
            return render(request,'dairyapp/milkrecord_create.html',{'formset':formset})

    
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
                dairy = Dairy.objects.get(name=kwargs['dairy'],user=self.request.user)
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
            dairy =get_object_or_404(Dairy,name=kwargs['dairy'],user=self.request.user)
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





class ParentListMemberMilkRecord(ListView):
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
             for i in range(10,30):
                  date = f"2023-09-{i}"
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
            if qs:
                """
                perform qs operation if only qs is not empty
                """
            
                milk_wg = qs.aggregate(Sum("milk_weight")).get('milk_weight__sum')
                avg_fat = qs.aggregate(Avg("milk_fat")).get('milk_fat__avg')
                self.kwargs['total_milk_wieght'] = milk_wg
                self.kwargs['avg_fat'] = avg_fat
                print("milk_weight",milk_wg)
                print("average_fat",avg_fat)
                fat_rate = FatRate.objects.filter(dairy__user=self.request.user,dairy=dairy)
                print("fat rate===",fat_rate[0].get_fat_rate)
                if fat_rate.exists():
                    print("inside fat_rate exists function")
                    print("fat_fate",fat_rate[0].fat_rate)
                    try:
                        total_price = fat_rate[0].get_fat_rate*milk_wg*avg_fat
                    except Exception as e:
                        total_price = 0
                    self.kwargs['total_price'] = total_price
                    # print("total price==",total_price)
                    pass


             
        return queryset.filter(filters)
   
@method_decorator(login_required(login_url='account_login'),name="dispatch")
@method_decorator(verified_dairy_user,name="dispatch")
class ListMemberMilkRecord(PaginationMixin,ParentListMemberMilkRecord):
    paginate_by = 16
    
    
    

class VerifyEsewa(View):
     def get(self,request):
        url ="https://uat.esewa.com.np/epay/transrec"
        q = request.GET.get('q')
        print(request.GET)
        

        d = {
            'amt':request.GET.get('amt'),
            'scd': 'EPAYTEST',
            'rid':  request.GET.get('refId'),
            'pid':request.GET.get('oid'),
        }
        resp = req.post(url, d)
        print("status code=====",resp.status_code)
        if resp.status_code == 200:
            user = self.request.user
            user.has_verified_dairy = True
            user.save()
        # print(resp.text)
            return HttpResponseRedirect(reverse('dairyapp:create_dairy'))
        else:
            raise Http404()

@method_decorator(login_required(login_url='account_login'),name="dispatch")
@method_decorator(verified_dairy_user,name="dispatch")
class ListDairyMembers(ListView):
     model = Dairy
     template_name = 'dairyapp/list_dairy_members.html'
     context_object_name = 'members'
     def get_queryset(self):
          print("hello =========")
          qs = super().get_queryset().filter(user=self.request.user)
          print(qs[0].members.all)
          if len(qs) == 1:
               return qs[0].members.all
          return []
     
     def get_context_data(self, **kwargs):
          context =  super().get_context_data(**kwargs)
          print("context===",context)
          
          context['dairy'] = self.kwargs['dairy']
          return context


@method_decorator(login_required(login_url='account_login'),name="dispatch")
@method_decorator(verified_dairy_user,name="dispatch")
class SendMilkReportEmialView(View):
    def get(self,request,*args,**kwargs):
        dairy_name = request.GET.get('dairy')
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        shift = request.GET.get('shift')
        user_id = request.GET.get('id')

        
        

             
        global user
        global dairy
        global fat_rate

        if not start_date and not end_date:
            messages.error(request,_("Please select start date and end date"))
            return redirect('dairyapp:member_milk_record',dairy=dairy_name,id=user_id)

        try:
            try:
                dairy = Dairy.objects.get(name=dairy_name,user=request.user)
            except Dairy.DoesNotExist:
                messages.error(request, _("Sorry,dairy with username doesnot exists."))
                return redirect("dairyapp:member_milk_record",id=user_id,dairy=dairy_name)
            
            try:
                #get dairy based on dairy nama and dairy owner
                fat_rate = FatRate.objects.get(dairy=dairy,dairy__user=request.user).get_fat_rate
            except FatRate.DoesNotExist:
                messages.error(request, _("Sorry,Please insert fatrate."))
                return redirect("dairyapp:member_milk_record",id=user_id,dairy=dairy_name)
                
                
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                messages.error(request, _("Sorry,invalid userid"))
                return redirect("dairyapp:member_milk_record",id=user_id,dairy=dairy_name)
            
            morning_milk_records = MilkRecord.objects.filter(dairy__user=self.request.user,dairy=dairy,shift="morning",user=user,date__gte=start_date, date__lte=end_date)
            night_milk_records = MilkRecord.objects.filter(dairy__user=self.request.user,date__gte=start_date, date__lte=end_date,shift="night",user=user)
            if not morning_milk_records or not night_milk_records:
                messages.error(request, _("Please select valid information before genarating milk report"))
                return redirect("dairyapp:member_milk_record",id=user_id,dairy=dairy_name)
            
            print(morning_milk_records)
            milk_wg = morning_milk_records.aggregate(Sum("milk_weight")).get('milk_weight__sum')
            avg_fat = morning_milk_records.aggregate(Avg("milk_fat")).get('milk_fat__avg')
            fat_rate = fat_rate
            total_price = fat_rate*milk_wg*avg_fat

            nmilk_wg = night_milk_records.aggregate(Sum("milk_weight")).get('milk_weight__sum')
            navg_fat = night_milk_records.aggregate(Avg("milk_fat")).get('milk_fat__avg')
            nfat_rate = fat_rate

            ntotal_price = fat_rate*nmilk_wg*navg_fat


            context = {
                'total_milk_wieght':milk_wg,
                'avg_fat': round(avg_fat,3),
                'fat_rate':round(fat_rate,3),
                'total_price':round(total_price,3),

                'ntotal_milk_wieght':nmilk_wg,
                'navg_fat': round(navg_fat,3),
                'nfat_rate':round(nfat_rate,3),
                'ntotal_price':round(ntotal_price,3),


                'user':user,
                'shift':'morning',
                'morning_milk_records':morning_milk_records,
                'night_milk_records': night_milk_records
            }
            print("context===========",context)
            rendered_mail_template = render_to_string("dairyapp/email/report.html",context)
            html = HTML(string=rendered_mail_template)
            buffer = io.BytesIO()
            html.write_pdf(target=buffer)
            pdf = buffer.getvalue()

            filename = 'test.pdf'
            mimetype_pdf = 'application/pdf'
            # print(rendered_mail_template)

            try:
                 
                sendMial(
                    subject="Milk Report",
                    from_email=settings.EMAIL_HOST_USER,
                    to=user.email,
                    message="hello",
                    filename=filename,
                    pdf=pdf)
            except Exception as e:
                 print(e)

            return HttpResponse(rendered_mail_template)
            messages.success(request,_("milk report email sent"))
            return redirect("dairyapp:member_milk_record",id=user_id,dairy=dairy_name)
                
        except Exception as e:
            print("e----------",e)
            raise Http404
            # return HttpResponseNotFound
            

            
            
