from django.contrib import admin

from . import models


class CourseLikeInline(admin.TabularInline):
    model = models.CourseLike



admin.site.register(models.Course)
