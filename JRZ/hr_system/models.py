from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse


class Manager(models.Model):
    f_name = models.CharField(_("first name"), max_length=50)
    l_name = models.CharField(_("last name"), max_length=50)
    email = models.EmailField(_("email"), max_length=254)

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

    department = models.ForeignKey(
        Department, 
        verbose_name=_("employee"), 
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

class AplicationForms(models.Model):

    

    class Meta:
        verbose_name = _("aplicationforms")
        verbose_name_plural = _("aplicationforms")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("aplicationforms_detail", kwargs={"pk": self.pk})



class Application(models.Model):
    date_created = models.DateField(_("date_created"), auto_now=False, auto_now_add=False)
    # department = models.ForeignKey( 
    #     verbose_name=_("employee"), 
    #     on_delete=models.CASCADE,
    #     related_name='employees',
    #     choices=
    # )

    class Meta:
        verbose_name = _("application")
        verbose_name_plural = _("applications")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("application_detail", kwargs={"pk": self.pk})







