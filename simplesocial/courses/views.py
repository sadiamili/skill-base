from django.contrib import messages
from django.contrib.auth.mixins import(
    LoginRequiredMixin,
    PermissionRequiredMixin
)

from django.urls import reverse
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django.views import generic
from courses.models import Course,CourseLike
from . import models

class CreateCourse(LoginRequiredMixin, generic.CreateView):
    fields = ("name", "description")
    model = Course

class SingleCourse(generic.DetailView):
    model = Course

class ListCourses(generic.ListView):
    model = Course


class LikeCourse(LoginRequiredMixin, generic.RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse("courses:single",kwargs={"slug": self.kwargs.get("slug")})

    def get(self, request, *args, **kwargs):
        course = get_object_or_404(Course,slug=self.kwargs.get("slug"))

        try:
            CourseLike.objects.create(user=self.request.user,course=course)

        except IntegrityError:
            messages.warning(self.request,("Warning, already liked {}".format(course.name)))

        else:
            messages.success(self.request,"You now like the {} course.".format(course.name))

        return super().get(request, *args, **kwargs)


class LeaveCourse(LoginRequiredMixin, generic.RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse("courses:single",kwargs={"slug": self.kwargs.get("slug")})

    def get(self, request, *args, **kwargs):

        try:

            likeship = models.CourseLike.objects.filter(
                user=self.request.user,
                course__slug=self.kwargs.get("slug")
            ).get()

        except models.CourseLike.DoesNotExist:
            messages.warning(
                self.request,
                "You can't unlike a course you haven't liked."
            )
        else:
            likeship.delete()
            messages.success(
                self.request,
                "You have successfully unliked it."
            )
        return super().get(request, *args, **kwargs)
