#-*- coding: UTF-8 -*-
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import ugettext, ugettext_lazy as _
from django.contrib.auth.models import User
from django.forms import ModelForm, Textarea,TextInput
from usermanager.models import *
from django.forms.formsets import formset_factory
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit,HTML,Row,Field
from crispy_forms.bootstrap import InlineField
from django.forms.extras.widgets import SelectDateWidget
from datetime import *

MAX_CHAR_LENGTH = 200



class PhotoForm(forms.Form):
	photo = forms.ImageField(required=True)

