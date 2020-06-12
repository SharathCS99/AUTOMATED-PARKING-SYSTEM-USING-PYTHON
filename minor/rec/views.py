from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.urls import path,include
from firebase import firebase
from django.contrib import messages
import numpy as np
import cv2
import imutils
import pytesseract
import time
reg_id=0
timo=''
strin=''
import datetime
from datetime import timedelta
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
a=['id','pass','pass2','slot','slotp']
x=0
reg_id=0
id=0
loga=['id1','pass1']
firebase=firebase.FirebaseApplication('fill the firebase link')
def startup(request):
	return render(request,'stata.html')
def home(request):
	global a
	global reg_id
	d={'id':a[0],'pass':a[1],'pass2':a[2],'slot':a[3],'slotp':a[4]}
	return render(request,'home.html',d)
def login(request):
	global reg_id
	global loga
	return render(request,'LOG.html',{'id1':loga[0],'pass1':loga[1]})
def actuallo(request):
	global reg_id
	print("is the login id",request.GET['id1'])
	global x
	global id
	if(firebase.get('/'+str(request.GET['id1']),'id')!=None):
		if(firebase.get('/'+str(request.GET['id1']),'pass')==request.GET['pass1']):
			reg_id=request.GET['id1']
			print("reg_id in login is",reg_id)
			return render(request,'optionsoftwo.html')
		else:
			messages.error(request,"the paswords or username do not match or no such user")
			return redirect('login')
	else:
		messages.error(request,"the paswords or username do not match or no such user")
		return redirect('login')
def entry1(request):
	global timo
	global id
	global strin
	image=cv2.imread('C:/python3/working/i20.jpeg')
	image=imutils.resize(image, width=500)
	cv2.imshow("Original Image", image)
	print(image)
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	cv2.imshow("1 - Grayscale Conversion", gray)
	gray = cv2.bilateralFilter(gray, 11,17,17)
	cv2.imshow("2 - Bilateral Filter", gray)
	edged = cv2.Canny(gray, 170, 200)
	cv2.imshow("4 - Canny Edges", edged)
	(new, cnts, _) = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
	cnts=sorted(cnts, key = cv2.contourArea, reverse = True)[:30]
	NumberplateCnt = None
	count=0
	idx=7
	for c in cnts:
		print("hello")
		peri=cv2.arcLength(c,True)
		approx=cv2.approxPolyDP(c,0.02*peri,True)
		NumberplateCnt=approx
		x,y,w,h=cv2.boundingRect(c)
		new_img=image[y:y+h,x:x+w]
		cv2.imwrite('C:/python3/cropped image-test'+str(idx)+'.png',new_img)
		cv2.imshow("hey bro",new_img)
		idx+=1
		break
	loc='C:/python3/cropped image-test7.png'
	cv2.drawContours(image,[NumberplateCnt], -1,(0,255,0),3)
	cv2.imshow("Final Image With Number Plate Detected", image)
	strin=pytesseract.image_to_string(loc,lang='eng')
	strin=str(strin)
	strin.replace(" ","")
	print(strin)
	print(id)
	datetimeFormat = '%Y-%m-%d %H:%M:%S.%f'
	date1 = str(datetime.datetime.now())
	#date2 = str(datetime.datetime.now())
	#diff = datetime.datetime.strptime(date1, datetimeFormat)- datetime.datetime.strptime(date2, datetimeFormat)
	timo=date1
	#print("Difference:", diff)
	#print("Days:", diff.days)
	#print("Microseconds:", diff.microseconds)
	#print("Seconds:", diff.seconds)
	d1='entry1'+str(strin)
	#g=firebase.patch('/'+str(id)+'/'+'entry',{d1:strin})
	return render(request,'rep.html',{'var':strin,'time':str(timo)})
def cloudop(request):
	global id
	global timo
	global reg_id
	print("reg_id",reg_id)
	timo=str(timo)
	global strin
	d='/'+str(reg_id)+'/entry'
	print(d)
	dsim='entry1'+str(strin)
	g=firebase.patch(d,{dsim:strin})
	d1='/'+str(reg_id)+'/timeentry'
	print("is the time",timo,d1)
	dsim='timeentry'+str(strin)
	print(dsim)
	g1=firebase.patch(d1,{dsim:timo})
	return render(request,'optionsoftwo.html')
#def exit(request):
def entry(request):
	global a
	global reg_id
	reg_id=request.GET[a[0]]
	d=firebase.get('/'+str(reg_id),'id')
	if(d!=None):
		print("hey")
		messages.error(request,"This user already present please login")
		return redirect('startup')
	if(request.GET[a[1]]!=request.GET[a[2]]):
		messages.error(request,"the paswords do not match")
		return redirect('home')
	if((request.GET[a[3]]=='') or(request.GET[a[4]]=='')):
		messages.error(request,"the slot field must not be empty")
		return redirect('home')
	for i in a:
		s='/'+str(request.GET[a[0]])
		id=s
		firebase.patch(s,{i:request.GET[i]})
	messages.error(request,"REGISTRATION SUCESSFUL")
	return redirect('home')
def exit(request):
	global timo
	global reg_id
	global id
	global strin
	image=cv2.imread('C:/python3/working/i20.jpeg')
	image=imutils.resize(image, width=500)
	cv2.imshow("Original Image", image)
	print(image)
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	cv2.imshow("1 - Grayscale Conversion", gray)
	gray = cv2.bilateralFilter(gray, 11,17,17)
	cv2.imshow("2 - Bilateral Filter", gray)
	edged = cv2.Canny(gray, 170, 200)
	cv2.imshow("4 - Canny Edges", edged)
	(new, cnts, _) = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
	cnts=sorted(cnts, key = cv2.contourArea, reverse = True)[:30]
	NumberplateCnt = None
	count=0
	idx=7
	for c in cnts:
		print("hello")
		peri=cv2.arcLength(c,True)
		approx=cv2.approxPolyDP(c,0.02*peri,True)
		NumberplateCnt=approx
		x,y,w,h=cv2.boundingRect(c)
		new_img=image[y:y+h,x:x+w]
		cv2.imwrite('C:/python3/cropped image-test'+str(idx)+'.png',new_img)
		cv2.imshow("hey bro",new_img)
		idx+=1
		break
	loc='C:/python3/cropped image-test7.png'
	cv2.drawContours(image,[NumberplateCnt], -1,(0,255,0),3)
	cv2.imshow("Final Image With Number Plate Detected", image)
	strin=pytesseract.image_to_string(loc,lang='eng')
	strin=str(strin)
	strin.replace(" ","")
	print(strin)
	g=firebase.get('/'+str(reg_id)+'/timeentry','timeentry'+str(strin))
	print(g)
	if(g==None):
		messages.error(request,"NO USER AS SUCH ENTERED")
		return render(request,'ack.html')
	date2=g
	#date2 = datetime.datetime.strptime(g,'%Y-%m-%d %H:%M:%S.%f')
	datetimeFormat = '%Y-%m-%d %H:%M:%S.%f'
	date1 = str(datetime.datetime.now())
	diff = datetime.datetime.strptime(date1, datetimeFormat)- datetime.datetime.strptime(date2, datetimeFormat)
	print("op",reg_id)
	print("Difference:", diff)
	print("Days:", diff.days)
	print("Microseconds:", diff.microseconds)
	print("Seconds:", diff.seconds)
	#d1='entry1'+str(strin)
	#g=firebase.patch('/'+str(id)+'/'+'entry',{d1:strin})tetime.now())
	#date2 = str(datetime.dtetime.now())
	baseprice=firebase.get('/'+str(reg_id),'slot')
	baseprice=int(baseprice)
	print(baseprice)
	diff=str(diff.seconds)
	print(type(diff))
	diff=int(int(diff)/60)
	paseprice=(diff)*baseprice
	print(paseprice)
	messages.error(request,"THE USER WITH"+str(strin)+" "+"MUST PAY"+" "+str(paseprice))
	return render(request,'ack.html')
