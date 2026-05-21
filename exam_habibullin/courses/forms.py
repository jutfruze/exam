from django import forms

from .models import User, Application, Review


class RegisterForm(forms.ModelForm):
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['surname', 'name', 'patronymic', 'login', 'password', 'phone', 'email']

    def clean_login(self):
        login = self.cleaned_data['login']
        if User.objects.filter(login=login).exists():
            raise forms.ValidationError('Такой логин уже занят')
        return login

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})


class LoginForm(forms.Form):
    login = forms.CharField(label='Логин')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

class ApplicationForm(forms.ModelForm):
    preferred_date = forms.DateField(
        label='Дата обучения'
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    
    class Meta:
        model = Application
        fields = ['course_type', 'payment_type', 'preffered_date']

    def __init__(self,*args, **kwards):
        super().__init__(*args, **kwards)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-select'})
        self.fields['preffered_date'].widget.attrs.update({'class': 'form-control'})

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'rows':4}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['text'].widget.attrs.update({'class':'form-control'})