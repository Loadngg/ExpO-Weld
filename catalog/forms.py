from django import forms


class SearchForm(forms.Form):
    """Форма поиска"""

    search_field = forms.CharField(max_length=150)
