from django.conf import settings
from django.urls import reverse
from django.db import models
from django.utils.text import slugify
# from accounts.models import User

import misaka

from django.contrib.auth import get_user_model
User = get_user_model()

# https://docs.djangoproject.com/en/1.11/howto/custom-template-tags/#inclusion-tags
# This is for the in_skill_likes check template tag
from django import template
register = template.Library()



class Skill(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(allow_unicode=True, unique=True)
    description = models.TextField(blank=True, default='')
    description_html = models.TextField(editable=False, default='', blank=True)
    likes = models.ManyToManyField(User,through="SkillLike")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        self.description_html = misaka.html(self.description)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("skills:single", kwargs={"slug": self.slug})


    class Meta:
        ordering = ["name"]


class SkillLike(models.Model):
    skill = models.ForeignKey(Skill, related_name="likeships",on_delete=models.CASCADE,)
    user = models.ForeignKey(User,related_name='user_skills',on_delete=models.CASCADE,)

    def __str__(self):
        return self.user.username

    class Meta:
        unique_together = ("skill", "user")
