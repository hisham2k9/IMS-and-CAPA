from django import forms

class NameForm(forms.Form):
    subject = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class' : 'form-control', 'placeholder':'Search'}))
    message = forms.CharField(widget=forms.Textarea)
    sender = forms.EmailField()
    cc_myself = forms.BooleanField(required=False)