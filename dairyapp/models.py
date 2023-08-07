from django.db import models
from my_account.models import User
from django.utils.translation import gettext_lazy as _
from . custom_model_managers import *
from django.urls import reverse

class Dairy(models.Model):
    name = models.CharField(_("name"),max_length=200,unique=True)
    user = models.ForeignKey(User,on_delete=models.PROTECT,related_name="dairies",verbose_name=_("user"))
    location = models.CharField(_("location"),max_length=200)
    is_verified = models.BooleanField(_("verified"),default=False)
    created_at = models.DateTimeField(_("created at"),auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"),auto_now=True)
    members = models.ManyToManyField(User,verbose_name=_("dairy"),null=True,blank=True)

    objects = models.Manager()
    verObs = DairyModelManager()

    def __str__(self) -> str:
        return self.name
    
    class Meta:
        verbose_name = _("dairy")
        verbose_name_plural = _("dairies")

    def get_absolute_url(self):
        return reverse('dairyapp:homepage')
    

class FatRate(models.Model):
    fat_rate = models.FloatField(_("fat rate"),max_length=5)
    dairy = models.OneToOneField(Dairy,on_delete=models.CASCADE,verbose_name=_("dairy"))
    created_at = models.DateTimeField(_("created at"),auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"),auto_now=True)

    def __str__(self) -> str:
        return f"{self.dairy.name}-{self.fat_rate}"
    
class MilkRecord(models.Model):
    shift_choices = (
        (_("morning"),_("morning")),
        (_("night"),_("night"))
    )
    dairy = models.ForeignKey(Dairy,on_delete=models.CASCADE,verbose_name=_("dairy"))
    user = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name=_("user"))
    shift = models.CharField(_("shift"),max_length=10,choices=shift_choices)
    milk_weight = models.FloatField(_("milk weight"))
    milk_fat = models.FloatField(_("milk fat"),max_length=5)
    date = models.DateField(_("date"))
    created_at = models.DateTimeField(_("created at"),auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"),auto_now=True)

    class Meta:
        unique_together = ["dairy", "user","shift","date"]


