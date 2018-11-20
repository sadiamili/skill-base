from django.contrib import messages
from django.contrib.auth.mixins import(
    LoginRequiredMixin,
    PermissionRequiredMixin
)

from django.urls import reverse
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django.views import generic
from skills.models import Skill,SkillLike
from . import models

class CreateSkill(LoginRequiredMixin, generic.CreateView):
    fields = ("name", "description")
    model = Skill

class SingleSkill(generic.DetailView):
    model = Skill

class ListSkills(generic.ListView):
    model = Skill


class LikeSkill(LoginRequiredMixin, generic.RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse("skills:single",kwargs={"slug": self.kwargs.get("slug")})

    def get(self, request, *args, **kwargs):
        skill = get_object_or_404(Skill,slug=self.kwargs.get("slug"))

        try:
            SkillLike.objects.create(user=self.request.user,skill=skill)

        except IntegrityError:
            messages.warning(self.request,("Warning, already liked {}".format(skill.name)))

        else:
            messages.success(self.request,"You now like {} skill.".format(skill.name))

        return super().get(request, *args, **kwargs)


class LeaveSkill(LoginRequiredMixin, generic.RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse("skills:single",kwargs={"slug": self.kwargs.get("slug")})

    def get(self, request, *args, **kwargs):

        try:

            likeship = models.SkillLike.objects.filter(
                user=self.request.user,
                skill__slug=self.kwargs.get("slug")
            ).get()

        except models.SkillLike.DoesNotExist:
            messages.warning(
                self.request,
                "You can't unlike a skill you haven't liked."
            )
        else:
            likeship.delete()
            messages.success(
                self.request,
                "You have unliked the skill."
            )
        return super().get(request, *args, **kwargs)
