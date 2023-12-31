
from django.urls import path,include
from . import views
app_name = "dairyapp"

urlpatterns = [
    path("",views.HomeView.as_view(),name="homepage"),

    #fat urls
    path("fat-rates",views.FatListView.as_view(),name="fat_list"),
    path("create-fat-rates/",views.CreateFatView.as_view(),name="create-fat"),
    path("edit-fat-rates/<int:id>",views.UpdateFatView.as_view(),name="edit_fat"),
    path("delete-fat-rates/<int:pk>",views.DeleteFatRate.as_view(),name="delete_fat"),

    #dairy urls
    path("create-dairy",views.CreateDairyView.as_view(),name="create_dairy"),
    path("edit-dairy/<int:pk>",views.UpadteDairyView.as_view(),name="update_dairy"),
    path("list-milk-records/<str:dairy>",views.ListMilkReports.as_view(),name="milk_record"),
    path("create-milk-records/<str:dairy>",views.CreateMilkRercord.as_view(),name="create_milk_record"),
    path("update-milk-record/<int:id>/<str:dairy>",views.UpdateMilkRercord.as_view(),name="update_milk_record")
]