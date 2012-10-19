from django import forms

class Change(forms.Form):
    username=forms.CharField(required=True)
    password=forms.CharField(widget=forms.PasswordInput, required=True)
    first_name=forms.CharField(required=False)
    last_name=forms.CharField(required=False)
    email=forms.CharField(required=False)
    is_supeuser=forms.CharField(widget=forms.CheckboxInput, required=False)
    core_num=forms.IntegerField(required=False)
    mem_limit=forms.IntegerField(required=False)
    user=""

