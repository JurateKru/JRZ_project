from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.contrib.auth import get_user_model
from tinymce.models import HTMLField
from datetime import date
from django.utils.timezone import now

User = get_user_model()

class Manager(models.Model):
    f_name = models.CharField(_("first name"), max_length=50)
    l_name = models.CharField(_("last name"), max_length=50)
    email = models.EmailField(_("email"), max_length=254)
    hire_date = models.DateField(_("hire date"), auto_now=False, auto_now_add=False, default=now)
    term_date = models.DateField(_("termination date"), auto_now=False, null=True, blank=True)

    STATUS_ACTIVITY = (
        (0, _('Active')),
        (1, _('Terminated'))
    )

    status = models.PositiveSmallIntegerField(
        _("status"), 
        choices=STATUS_ACTIVITY, 
        default=0,
        db_index=True
    )

    class Meta:
        verbose_name = _("manager")
        verbose_name_plural = _("managers")

    def __str__(self):
        return f"{self.f_name} {self.l_name} {self.email}"

    def get_absolute_url(self):
        return reverse("manager_detail", kwargs={"pk": self.pk})


class Department(models.Model):
    name = models.CharField(_("name"), max_length=250)
    manager = models.ForeignKey(
        Manager, 
        verbose_name=_("manager"), 
        on_delete=models.CASCADE,
        related_name='departments'
    )
    

    class Meta:
        verbose_name = _("department")
        verbose_name_plural = _("departments")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("department_detail", kwargs={"pk": self.pk})


class Employee(models.Model):
    f_name = models.CharField(_("first name"), max_length=50)
    l_name = models.CharField(_("last name"), max_length=50)
    email = models.EmailField(_("email"), max_length=254)
    hire_date = models.DateField(_("hire date"), auto_now=False, auto_now_add=False, default=now)
    term_date = models.DateField(_("termination date"), auto_now=False, null=True, blank=True)

    STATUS_ACTIVITY = (
        (0, _('Active')),
        (1, _('Terminated'))
    )

    status = models.PositiveSmallIntegerField(
        _("status"), 
        choices=STATUS_ACTIVITY, 
        default=0,
        db_index=True
    )
    department = models.ForeignKey(
        Department, 
        verbose_name=_("department"), 
        on_delete=models.CASCADE,
        related_name='employees',
        null=True, blank=True,
    )
    user = models.ForeignKey(
        User,
        verbose_name=("user_profile"),
        on_delete=models.CASCADE,
        related_name='users',
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = _("employee")
        verbose_name_plural = _("employees")

    def __str__(self):
        return f"{self.f_name} {self.l_name} "

    def get_absolute_url(self):
        return reverse("employee_detail", kwargs={"pk": self.pk})

class Application(models.Model):
    title = models.CharField(_("title"), max_length=50, db_index=True, blank=True, null=True)
    description = models.TextField(_("description"), max_length=5000, db_index=True, blank=True, null=True)
    class Meta:
        verbose_name = _("application")
        verbose_name_plural = _("applications")

    def __str__(self):
        return f"{self.title} "

    def get_absolute_url(self):
        return reverse("application_detail", kwargs={"pk": self.pk})
    

class ApplicationInstance(models.Model): 
    CHOICES_STATUS =(
        (0, _("New")),
        (1, _("Approved")),
        (2, _("Declined")),
        )
    
    status = models.PositiveSmallIntegerField(_("status"), choices=CHOICES_STATUS, db_index=True, null=True, blank=True, default=0)
    date_created = models.DateField(_("date_created"), default=now)
    content = models.TextField(_("content"), null=True, blank=True) 
    application = models.ForeignKey(
        Application, 
        verbose_name=_("application"), 
        on_delete=models.CASCADE,
        related_name='instances',
        )
    
    class Meta:
        verbose_name = _("application_instance")
        verbose_name_plural = _("application_instances")

    def __str__(self):
        status = dict(ApplicationInstance.CHOICES_STATUS)[self.status]
        return f"Application #{self.id}: {self.application}, {self.date_created}, {status}"

    def get_absolute_url(self):
        return reverse("application_instance_detail", kwargs={"pk": self.pk})
    
