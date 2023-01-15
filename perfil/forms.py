from django import forms

class SemesterForm(forms.Form):
    semester = forms.IntegerField(max_value = 32767, min_value = 1, label = False)