from django import forms

from .url_helper import get_all_views
from .models import Html


class HtmlForm(forms.ModelForm):
    view = forms.ChoiceField(widget=forms.Select, choices=(("", "--SELECT--")))

    def __init__(self, *args, **kwargs):
        super(HtmlForm, self).__init__(*args, **kwargs)
        choices = [('', "--SELECT--")] + get_all_views()
        self.fields['view'].choices = choices

    class Meta:
        model = Html
        exclude = []
