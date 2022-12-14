from django import forms
import datetime


def GetChoiceList(courses,day,hour,user):


     CHOICE_LIST = []
     
     sec = GetUserSections(day,hour,user)
     if sec != None :
          CHOICE_LIST.append(sec)
     CHOICE_LIST.append(("1", "----"))
     
     for course in courses:      
         for section_time in course.schedule.all():
               if section_time.day == day and section_time.time == hour:
                    CHOICE_LIST.append((course, course))
    
     return CHOICE_LIST

def GetUserSections(day,hour,user):
     for course in user:      
          for section_time in course.schedule.all():
              
               if section_time.day == day and section_time.time == hour:
                    return ("0", course)
     return None

def GetFormLabel(courses,day,hour,user):
 fieldClass = forms.Select(attrs={"class":"form-select box-header-card col-10"})
 return forms.ChoiceField(choices=GetChoiceList(courses,day,hour,user),widget=fieldClass)


class AgendaForm(forms.Form):
     #overwrite __init__
     #required_css_class = 'form-select box-header-card col-10 '
     def __init__(self,courses,day,user_sec,*args,**kwargs):
          # call standard __init__
          super().__init__(*args,**kwargs)
          #extend __init__ 
    
          self.fields['8:00'] = GetFormLabel(courses,day,datetime.time(8,0,0),user_sec)
          self.fields['10:00'] = GetFormLabel(courses,day,datetime.time(10,0,0),user_sec)
          self.fields['13:30'] = GetFormLabel(courses,day,datetime.time(13,30,0),user_sec)
          self.fields['15:30'] = GetFormLabel(courses,day,datetime.time(15,30,0),user_sec)
          self.fields['19:00'] = GetFormLabel(courses,day,datetime.time(19,0,0),user_sec)
          self.fields['21:00'] = GetFormLabel(courses,day,datetime.time(21,0,0),user_sec)
          self.fields['8:00'].required = False
          self.fields['10:00'].required = False
          self.fields['13:30'].required = False
          self.fields['15:30'].required = False
          self.fields['19:00'].required = False
          self.fields['21:00'].required = False


