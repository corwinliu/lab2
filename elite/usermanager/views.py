#-*- coding: UTF-8 -*-
from django.core.files import File
import datetime
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.views import login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from usermanager.forms import *
from django.forms.formsets import formset_factory
from django.forms.models import modelform_factory
import json
from django.http import HttpResponse
from core.face_ana import process
from PIL import Image


def setting(request):
	print "home"
	user =request.user
	ph=PHOTO.objects.create()
	if request.method == 'POST':
		print "post"
		
		print request.FILES
		if 'photo' in request.FILES:

			try:
				
				ph.photo = request.FILES['photo']
				ph.save()
				ph2 = PHOTO.objects.create()
				process(Image.open(ph.photo.path)).save('out.png')
				ph2.photo.save("qwe",File(open('out.png')))
			except Exception,e:
				print "erro",e

			return render_to_response('result.html',{'photo':ph2.photo} ,context_instance=RequestContext(request))
		else:
			pass

	return render_to_response('home.html',{
		} ,context_instance=RequestContext(request))			
	
	