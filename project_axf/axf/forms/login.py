#coding:utf-8
from django import forms

class LoginForms(forms.Form):
    username=forms.CharField(max_length=12,min_length=1,required=True,error_messages={
        'required':'用户账户不能为空','invalid':'格式错误'},widget=forms.TextInput(attrs={'class':'c'}))

    passwd=forms.CharField(max_length=16,min_length=1,widget=forms.PasswordInput)