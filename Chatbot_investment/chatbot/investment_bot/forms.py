from django import forms

class login_form(forms.Form):
    employee_code=forms.CharField(widget=forms.TextInput(attrs={'class':'form-group'}))

class register_form(forms.Form):
    employee_code=forms.CharField(max_length=264)
    name=forms.CharField(max_length=264)
    Father_or_Husband_name=forms.CharField(max_length=264)
    Company_name=forms.CharField(max_length=264)
    dob=forms.DateField()
    Gender=forms.CharField(max_length=264)
    location=forms.CharField(max_length=264)
    PAN=forms.CharField(max_length=264)
    Contact_Number=forms.CharField(max_length=264)
    Date_of_Join=forms.DateField()
