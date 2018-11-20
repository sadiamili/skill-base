from django import forms

from posts import models


class PostForm(forms.ModelForm):
    class Meta:
        fields = ("message", "course")
        model = models.Post

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields["course"].queryset = (
                models.Course.objects.filter(
                    pk__in=user.courses.values_list("course__pk")
                )
            )