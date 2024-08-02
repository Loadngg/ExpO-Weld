from django import forms
from .models import Callback


class CallbackForm(forms.ModelForm):
    """Форма обратной связи"""

    class Meta:
        model = Callback
        fields = ["full_name", "phone_number", "message", "article"]
