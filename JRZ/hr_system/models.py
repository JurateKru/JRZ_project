from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from tinymce.models import HTMLField
from datetime import date
from django.utils.timezone import now



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
    )


    class Meta:
        verbose_name = _("employee")
        verbose_name_plural = _("employees")

    def __str__(self):
        return f"{self.f_name} "

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
    

class Vacation(models.Model):
    start_date = models.DateField(_("start_date"), auto_now=False, null=True, blank=True)
    end_date = models.DateField(_("end_date"), auto_now=False,null=True, blank=True)
    payout_before = models.BooleanField(_("payout_before"))
    application = models.ForeignKey(Application, verbose_name=_("application"), on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = _("vacation")
        verbose_name_plural = _("vacations")

    def __str__(self):
        return f"Start date: {self.start_date}, End date: {self.end_date}, Payout before vacation {self.payout_before}"

    def get_absolute_url(self):
        return reverse("vacation_detail", kwargs={"pk": self.pk})
    
    
class ParentDayOff(models.Model):
    start_date = models.DateField(_("start_date"), auto_now=False, null=True, blank=True)
    end_date = models.DateField(_("end_date"), auto_now=False,null=True, blank=True)    
    CHOICES =(
        (0, _("Raising 1 child under 12 years old")),
        (1, _("Raising 2 or more children under 12 years old")),
        (2, _("Raising 3 or more children under 12 years old")),
        (3, _("Raising 1 child with disabilities")),
        (4, _("Raising 2 or more children with disabilities"))
        )    
    parental_status = models.PositiveSmallIntegerField(_("parental_status"), choices=CHOICES, db_index=True, null=True, blank=True, default=0)
    application = models.ForeignKey(Application, verbose_name=_("application"), on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("parent day-off")
        verbose_name_plural = _("parent day-offs")

    def __str__(self):
        return f"Start date: {self.start_date}, End date: {self.end_date}, Parental status: {self.parental_status}"

    def get_absolute_url(self):
        return reverse("parent_day_off_detail", kwargs={"pk": self.pk})
    

class Termination(models.Model):
    terminate_date = models.DateField(_("terminate_date"), auto_now=False, null=True, blank=True)
    application = models.ForeignKey(Application, verbose_name=_("application"), on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("termination")
        verbose_name_plural = _("terminations")

    def __str__(self):
        return self.terminate_date

    def get_absolute_url(self):
        return reverse("termination_detail", kwargs={"pk": self.pk})


class Taxes(models.Model):
    npd = models.BooleanField(_("npd"))
    start_date = models.DateField(_("start_date"), auto_now=False, null=True, blank=True)
    application = models.ForeignKey(Application, verbose_name=_("application"), on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("taxes")
        verbose_name_plural = _("taxes")

    def __str__(self):
        return f"Start date{self.start_date}, Aplly NPD{self.npd}"

    def get_absolute_url(self):
        return reverse("taxes_detail", kwargs={"pk": self.pk})







