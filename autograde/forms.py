from django import forms
import datetime

def GetFormLabel():
 fieldClass = forms.CheckboxInput(attrs={"class":"form-check-input"})
 
 return forms.BooleanField(widget=fieldClass,required=False)

class HorariosForm(forms.Form):
     #overwrite __init__
     def __init__(self,*args,**kwargs):
          # call standard __init__
          super().__init__(*args,**kwargs)
          #extend __init__ 
          
    
          self.fields['mon0800'] = GetFormLabel();
          self.fields['mon1000'] = GetFormLabel();
          self.fields['mon1330'] = GetFormLabel();
          self.fields['mon1530'] = GetFormLabel();
          self.fields['mon1900'] = GetFormLabel();
          self.fields['mon2100'] = GetFormLabel();

          self.fields['tue0800'] = GetFormLabel();
          self.fields['tue1000'] = GetFormLabel();
          self.fields['tue1330'] = GetFormLabel();
          self.fields['tue1530'] = GetFormLabel();
          self.fields['tue1900'] = GetFormLabel();
          self.fields['tue2100'] = GetFormLabel();

          self.fields['wed0800'] = GetFormLabel();
          self.fields['wed1000'] = GetFormLabel();
          self.fields['wed1330'] = GetFormLabel();
          self.fields['wed1530'] = GetFormLabel();
          self.fields['wed1900'] = GetFormLabel();
          self.fields['wed2100'] = GetFormLabel();

          self.fields['thu0800'] = GetFormLabel();
          self.fields['thu1000'] = GetFormLabel();
          self.fields['thu1330'] = GetFormLabel();
          self.fields['thu1530'] = GetFormLabel();
          self.fields['thu1900'] = GetFormLabel();
          self.fields['thu2100'] = GetFormLabel();

          self.fields['fri0800'] = GetFormLabel();
          self.fields['fri1000'] = GetFormLabel();
          self.fields['fri1330'] = GetFormLabel();
          self.fields['fri1530'] = GetFormLabel();
          self.fields['fri1900'] = GetFormLabel();
          self.fields['fri2100'] = GetFormLabel();

          self.fields['sat0800'] = GetFormLabel();
          self.fields['sat1000'] = GetFormLabel();
          self.fields['sat1330'] = GetFormLabel();
          self.fields['sat1530'] = GetFormLabel();
          self.fields['sat1900'] = GetFormLabel();
          self.fields['sat2100'] = GetFormLabel();
