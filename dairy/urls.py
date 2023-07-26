
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('account/',include('my_account.urls',namespace='account')),
    path('accounts/', include('allauth.urls')),
    path('',include("dairyapp.urls",namespace="dairyapp")),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
