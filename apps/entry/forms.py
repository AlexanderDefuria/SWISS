from django import forms


class TestForm(forms.Form):
    template_name = 'entry/components/forms/form_snippet.html'
    your_name = forms.CharField(label='Your name', max_length=100)
