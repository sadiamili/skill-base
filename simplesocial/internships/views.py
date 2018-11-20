from django.contrib import messages
from django.contrib.auth.mixins import(
    LoginRequiredMixin,
    PermissionRequiredMixin
)

from django.urls import reverse
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django.views import generic
from internships.models import Internship,InternshipLike
from . import models

class CreateInternship(LoginRequiredMixin, generic.CreateView):
    fields = ("name", "description")
    model = Internship

class SingleInternship(generic.DetailView):
    model = Internship

class ListInternships(generic.ListView):
    model = Internship


class LikeInternship(LoginRequiredMixin, generic.RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse("internships:single",kwargs={"slug": self.kwargs.get("slug")})

    def get(self, request, *args, **kwargs):
        internship = get_object_or_404(Internship,slug=self.kwargs.get("slug"))

        try:
            InternshipLike.objects.create(user=self.request.user,internship=internship)

        except IntegrityError:
            messages.warning(self.request,("Warning, already liked {}".format(internship.name)))

        else:
            messages.success(self.request,"You liked the {} internship.".format(internship.name))

        return super().get(request, *args, **kwargs)


class UnlikeInternship(LoginRequiredMixin, generic.RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse("internships:single",kwargs={"slug": self.kwargs.get("slug")})

    def get(self, request, *args, **kwargs):

        try:

            likeship = models.InternshipLike.objects.filter(
                user=self.request.user,
                internship__slug=self.kwargs.get("slug")
            ).get()

        except models.InternshipLike.DoesNotExist:
            messages.warning(
                self.request,
                "You can't unlike this internship because you haven't liked it yet."
            )
        else:
            likeship.delete()
            messages.success(
                self.request,
                "You have unliked."
            )
        return super().get(request, *args, **kwargs)
