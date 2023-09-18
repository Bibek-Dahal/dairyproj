from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404, render
from django.views.generic import View,ListView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from dairyapp.models import Dairy, FatRate, MilkRecord
from dairyapp.views import ParentListMemberMilkRecord
from django.db.models import Q
from django.db.models import Avg,Sum
from django.core.paginator import Paginator


# Create your views here.

@method_decorator(login_required(login_url='account_login'),name="dispatch")
class HomeView(ListView):
    model = Dairy
    template_name = 'user/index.html'
    context_object_name = 'dairies'

    def get_queryset(self):
        qs = super().get_queryset().filter(members__in=[self.request.user])
        print('qs',qs)
        return qs
    # def get(self,request):
    #     dairies = Dairy.objects.filter(members__in=[request.user])
    #     print('dairies',dairies)

    #     return render(request,'user/index.html')


class MemberMilkRecord(ListView):
    context_object_name = "milkrecords"
    template_name = "user/member_milkrecord_list.html"

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['dairy'] = self.kwargs['dairy']
        context['start_date'] = self.request.GET.get('start_date')
        context['end_date'] = self.request.GET.get('end_date')
        context['shift'] = self.request.GET.get('shift')
        context['date'] = self.request.GET.get('date')
        context['count'] = self.kwargs['count']
        context['total_milk_wieght'] = self.kwargs['total_milk_wieght']
        context['avg_fat'] = round(self.kwargs['avg_fat'],3)
        context['total_price'] = self.kwargs['total_price']
        dairy = get_object_or_404(Dairy,name=self.kwargs['dairy'])
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
        user = self.request.user
        dairy = get_object_or_404(Dairy,name=self.kwargs['dairy'])
        print("after dairy=========")
        print('')
        queryset  = MilkRecord.objects.all()
        filters = Q(dairy=dairy,user=user)
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
                fat_rate = FatRate.objects.filter(dairy=dairy)
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