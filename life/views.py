# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
import base64
import time; 
import re
import hashlib
import random
from django.contrib import auth
from django.contrib.auth.models import User
from .forms import RegisterForm
from django.core.mail import send_mail
from .models import Person, Room, Membership, Friendship
import json

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
lasttime = 1.0
myip = '192.168.43.238'

import smtplib  
from email.mime.text import MIMEText   
  
def sendmail(to_list,sub,content):  
    mail_host="smtp.126.com"  
    mail_user="sender7939"    
    mail_pass="shouquan1"   
    mail_postfix="126.com"
    me="hello"+"<"+mail_user+"@"+mail_postfix+">"  
    msg = MIMEText(content,_subtype='plain',_charset='UTF-8')  
    msg['Subject'] = sub  
    msg['From'] = me  
    msg['To'] = to_list
    try:  
        server = smtplib.SMTP()  
        server.connect(mail_host)  
        server.login(mail_user,mail_pass)  
        server.sendmail(me, to_list, msg.as_string())  
        server.close()  
        return True
    except Exception, e:  
        print str(e)  
        return False

def index(request):     
    response_data = {}   
    response_data['message'] = 'This is the homepage.'                 
    return HttpResponse(json.dumps(response_data), content_type="application/json") 

def source(request):     
    response_data = {}   
    response_data['message'] = 'upload'                 
    return HttpResponse(json.dumps(response_data), content_type="application/json") 

def person(request):
    response_data = {}
    if request.method=='GET' and 'name' in request.GET:
    	name = request.GET['name']
    	try:
            person = Person.objects.get(name=name)
        except Exception:
            response_data['message'] = 'wrong_key'
            return HttpResponse(json.dumps(response_data), content_type="application/json")  
        if person != None:
            response_data['message'] = 'ok'
            response_data['name'] = person.name
	    response_data['dscrp'] = person.dscrp
	    response_data['credit'] = str(person.credit)
	    response_data['gender'] = person.gender
	    response_data['talk'] = person.talk
	    
	    i = 0
	    if len(person.room_set.all()) != 0:
            	for room in person.room_set.all():
            	    if Membership.objects.filter(room_id=room.id).get(person_id=person.id).allowed == False :
            	    	continue
            	    i = i + 1
        	    response_data['room'+str(i)] = room.name
       	    response_data['roomnum'] = i
            return HttpResponse(json.dumps(response_data), content_type="application/json")
        #else: return HttpResponse('null')         
    
    elif request.method=='POST':    	
        name = request.POST.get('name','')
        newtalk = request.POST.get('talk','')
    	newname = request.POST.get('newname','')
    	filterResult=Person.objects.filter(name=newname)
        if len(filterResult)>0:
            response_data['message'] = 'exist'
            return HttpResponse(json.dumps(response_data), content_type="application/json")
        dscrp = request.POST.get('dscrp','')
        credit= float(request.POST.get('credit', 0))
        gender= request.POST.get('gender', '')
        if request.user.is_authenticated():
            me = request.user.person
        elif credit != 0:
            myname = request.POST.get('myname','')
            me = Person.objects.get(name=myname)
        try:
            obj = Person.objects.get(name=name)
        except Exception:
            response_data['message'] = 'not_exist'
            return HttpResponse(json.dumps(response_data), content_type="application/json")
        if len(newname) != 0: obj.name = newname
        if len(newtalk) != 0: obj.talk += newtalk + '\n'
        if len(dscrp) != 0: obj.dscrp = dscrp
        if credit != 0: 
            friend = Friendship.objects.filter(person1_id=me.id).get(person2_id=obj.id)
            if friend.rated > 0 :
                friend.rated -= 1
                friend.save()	
        	obj.credit = credit*1/(obj.rnum) + obj.credit*(obj.rnum-1)/(obj.rnum)
            else :
                response_data['message'] = 'repeated'
        	return HttpResponse(json.dumps(response_data), content_type="application/json")
        if credit < 5: obj.bad += 1
        elif obj.bad > 0 : obj.bad -= 1
        if len(gender) != 0: obj.gender = gender
        obj.save()
        
	response_data['name'] = obj.name
	response_data['dscrp'] = obj.dscrp
	response_data['credit'] = str(obj.credit)
	response_data['gender'] = obj.gender
	response_data['rnum'] = str(obj.rnum)
	response_data['message'] = 'ok'
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    else:
    	response_data['message'] = 'wrong_request'
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    	
def room(request):
    response_data = {}
    curtime = time.mktime(time.localtime()) 
    name = ''
    slug = ''
    if request.method=='GET' and ('name' in request.GET or 'slug' in request.GET) :
    	if 'name' in request.GET : name = request.GET['name']
    	if 'slug' in request.GET : slug = request.GET['slug']
        if name != '' : rooms = Room.objects.filter(name=name)
        else : rooms = Room.objects.filter(slug=slug)
        
        if len(rooms) == 0 :
            response_data['message'] = 'null'
            return HttpResponse(json.dumps(response_data), content_type="application/json")  
        else:
            i = 0
            for room in rooms:
            	i = i + 1
            	datetime = time.mktime(time.strptime(room.date,'%Y.%m.%d'))
            	if curtime > datetime : 
            	    room.closed = True 
            	    room.save()
            	response_data['id'+str(i)] = room.id
            	response_data['name'+str(i)] = room.name
            	response_data['slug'+str(i)] = room.slug
	    	response_data['dscrp'+str(i)] = room.dscrp
	    	response_data['address'+str(i)] = room.address
	    	response_data['date'+str(i)] = room.date
	    	response_data['closed'+str(i)] = room.closed
	    	response_data['talk'+str(i)] = room.talk
	    	response_data['creator'+str(i)] = room.creator.username
	    	j = 0
	    	if len(room.members.all()) != 0:
            	    for roomer in room.members.all():
            	    	if Membership.objects.filter(room_id=room.id).get(person=roomer).allowed == False:
            	    	    continue 
            	    	j = j + 1
        	        response_data['member'+str(i)+str(j)] = roomer.name
        	response_data['memnum'+str(i)] = j
            response_data['roomnum'] = i
            response_data['message'] = 'ok'
            return HttpResponse(json.dumps(response_data), content_type="application/json")
    if request.method=='GET' and 'id' in request.GET:
    	rid = request.GET['id']
        rooms = Room.objects.filter(id=rid)
        
        if len(rooms) == 0 :
            response_data['message'] = 'not_exist'
            return HttpResponse(json.dumps(response_data), content_type="application/json")  
        else:
            room = Room.objects.get(id=rid)
            datetime = time.mktime(time.strptime(room.date,'%Y.%m.%d'))
            if curtime > datetime : 
                room.closed = True 
                room.save()
            response_data['id'] = room.id
            response_data['name'] = room.name
            response_data['slug'] = room.slug
	    response_data['dscrp'] = room.dscrp
	    response_data['address'] = room.address
	    response_data['date'] = room.date	#2017.1.1
	    response_data['talk'] = room.talk
	    response_data['closed'] = room.closed
	    j = 0
	    m = 0
	    if len(room.members.all()) != 0:
	    	mems = Membership.objects.filter(room_id=room.id)
                for roomer in room.members.all():
                    try:
                    	mem = mems.get(person=roomer)
                    except Exception:
                	response_data['message'] = 'multi_value'
                	return HttpResponse(json.dumps(response_data), content_type="application/json")
               	    if mem.allowed == False :
               	    	j = j + 1
        	    	response_data['joiner'+str(j)] = roomer.name
        	    if mem.allowed == True :
               	    	m = m + 1
        	    	response_data['member'+str(m)] = roomer.name
        	response_data['memnum'] = m
        	response_data['joinnum'] = j
            response_data['creator'] = room.creator.username
            if request.user.is_authenticated() and room.creator.username == request.user.username : response_data['iscreator'] = str(1)
            else : response_data['iscreator'] = str(0)
            response_data['message'] = 'ok'
            return HttpResponse(json.dumps(response_data), content_type="application/json")
    elif request.method=='POST':    	
    	id = request.POST.get('id','')
    	name= request.POST.get('name','')
    	if request.user.is_authenticated():
            me = request.user
        else:
            myname = request.POST.get('myname','')
            if len(myname) == 0:
            	me = User.objects.get(username='linfuqi')
            else: me = User.objects.get(username=myname)
    	if me.person.bad > 3 :
            response_data['message'] = 'bad_credit'
            response_data['talk'] = Room.objects.get(id=id).talk
            return HttpResponse(json.dumps(response_data), content_type="application/json")
            
    	newname= request.POST.get('newname','')
    	#filterResult=Room.objects.filter(name=newname)
        #if len(filterResult)>0:
        #    response_data['message'] = 'exist'
        #    return HttpResponse(json.dumps(response_data), content_type="application/json")
        dscrp= request.POST.get('dscrp','')
        slug= request.POST.get('slug', '')
        address= request.POST.get('address', '')
        date = request.POST.get('date', '')
        create= request.POST.get('create', '')
        talk= request.POST.get('talk', '')
        
        obj = Room()
        try:
            obj = Room.objects.get(id=id)
        except Exception:
            if create != '': 
                obj = Room.objects.create(name=name, creator_id = me.id)
            else: 
                response_data['message'] = 'not_exist'
                return HttpResponse(json.dumps(response_data), content_type="application/json")
            
        if len(newname) != 0: obj.name = newname
        if len(dscrp) != 0: obj.dscrp = dscrp
        if len(slug) != 0: obj.slug = slug
        if len(address) != 0: obj.address = address
        if len(date) != 0: obj.date = date
        if len(talk) != 0: 
            obj.talk += me.person.name + ': ' + talk + '\r\n' 
        if len(create) != 0 : obj.creator = me
        obj.save()
        
        response_data['id'] = obj.id
	response_data['name'] = obj.name
	response_data['dscrp'] = obj.dscrp
	response_data['slug'] = obj.slug
	response_data['address'] = obj.address
	response_data['date'] = obj.date
	response_data['talk'] = obj.talk
	response_data['creator'] = obj.creator.username
	response_data['message'] = 'ok'
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    else:
    	response_data['message'] = 'wrong_request'
        return HttpResponse(json.dumps(response_data), content_type="application/json")
        
def mem(request):
    response_data = {}
    
    if request.method=='GET' and 'roomid' in request.GET:
    	roomid = request.GET['roomid']
    	try:    
    	    room = Room.objects.get(id=roomid)
    	except Exception:
    	    response_data['message'] = 'wrong_key'
            return HttpResponse(json.dumps(response_data), content_type="application/json")
        mems = Membership.objects.filter(room_id=roomid)
        if len(mems) == 0:
            response_data['message'] = 'null'
            return HttpResponse(json.dumps(response_data), content_type="application/json")
        else:
            i = 0
            for mem in mems:
            	i = i + 1
            	response_data['roomid'+str(i)] = mem.room.id
            	response_data['personname'+str(i)] = mem.person.name
	    	response_data['application'+str(i)] = mem.application
	    	response_data['allowed'+str(i)] = mem.allowed
	    	response_data['rate'+str(i)] = mem.rate
	    	response_data['evaluate'+str(i)] = mem.evaluate
	    	response_data['date_joined'+str(i)] = mem.date_joined
            return HttpResponse(json.dumps(response_data), content_type="application/json")
        
    if request.method=='POST':
    	if request.user.is_authenticated():
            me = request.user
        else:
            myname = request.POST.get('myname','')
            if len(myname) == 0:
            	me = User.objects.get(id=1)
            else: me = User.objects.get(username=myname)
        if me.person.bad > 3 :
            response_data['message'] = 'bad_credit'
            return HttpResponse(json.dumps(response_data), content_type="application/json")
        roomid = request.POST.get('roomid','')
    	name = request.POST.get('name','')
    	create = request.POST.get('create','')
    	verify = request.POST.get('verify','')
    	refuse = request.POST.get('refuse','')
    	application = request.POST.get('application','')
    	rate = request.POST.get('rate','')
    	evaluate = request.POST.get('evaluate','')
    	
    	try:
    	    room = Room.objects.get(id=roomid)
    	    person = Person.objects.get(name=name)
    	except Exception:
    	    response_data['message'] = 'wrong_key'
            return HttpResponse(json.dumps(response_data), content_type="application/json")
    	
    	if create != '':
            if len(Membership.objects.filter(room=room).filter(person=person)) != 0:  	    
    	        response_data['message'] = 'not_self'
                return HttpResponse(json.dumps(response_data), content_type="application/json")
            if person.name == room.creator.person.name:  
                if len(Friendship.objects.filter(person1_id=person.id).filter(person2_id=person.id)) == 0 :
            	    Friendship.objects.create(person1_id=person.id, person2_id=person.id, rated=0)
            	friend = Friendship.objects.filter(person1_id=person.id).get(person2_id=person.id)
            	friend.rated += 1
            	friend.save()
            	Membership.objects.create(person_id=person.id, room_id=room.id, application=application, allowed = True)
            	person.rnum += 1
            	person.save()
            else: 
            	Membership.objects.create(person_id=person.id, room_id=room.id, application=application, allowed = False)
            if person.slug1 == '':
            	person.slug1 = room.slug
            if person.slug2 == '':
            	person.slug2 = room.slug
            if (room.slug != person.slug1 and room.slug != person.slug2) :
            	person.slug2 = person.slug1
            	person.slug1 = room.slug
            person.save()
            response_data['message'] = 'create'
            return HttpResponse(json.dumps(response_data), content_type="application/json")
            
        if verify != '':   
            try:
                relation = Membership.objects.get(room_id=room.id, person_id=person.id)
            except Exception:
    	        response_data['message'] = 'wrong_relation'
                return HttpResponse(json.dumps(response_data), content_type="application/json")
            relation.allowed = True
            relation.save()
            person.rnum += 1
            person.save()
            if len(room.members.all()) != 0:
                for roomer in room.members.all():
            	    if len(Friendship.objects.filter(person1_id=roomer.id).filter(person2_id=person.id)) == 0 :
            	         Friendship.objects.create(person1_id=roomer.id, person2_id=person.id, rated=0)
            	    if len(Friendship.objects.filter(person1_id=person.id).filter(person2_id=roomer.id)) == 0 :
            	         Friendship.objects.create(person1_id=person.id, person2_id=roomer.id, rated=0)
            	for roomer in room.members.all() :
            	    friend = Friendship.objects.filter(person1_id=roomer.id).get(person2_id=person.id)
            	    friend.rated += 1
            	    friend.save()
            	    if person.id != roomer.id:
            	    	friend = Friendship.objects.filter(person1_id=person.id).get(person2_id=roomer.id)
            	    	friend.rated += 1
            	    	friend.save()
            	         
            response_data['message'] = 'verified'
            return HttpResponse(json.dumps(response_data), content_type="application/json")
            
        if refuse != '':          
            try:
                relation = Membership.objects.get(room_id=room.id, person_id=person.id)
            except Exception:
    	        response_data['message'] = 'wrong_relation'
                return HttpResponse(json.dumps(response_data), content_type="application/json")
            Membership.objects.filter(room_id=room.id, person_id=person.id).delete()
            response_data['message'] = 'deleted'
            return HttpResponse(json.dumps(response_data), content_type="application/json")
        
        else:
            try:
                relation = Membership.objects.get(room_id=room.id, person_id=person.id)
            except Exception:
    	        response_data['message'] = 'wrong_relation'
                return HttpResponse(json.dumps(response_data), content_type="application/json")
            rate = request.POST.get('rate','')
    	    evaluate = request.POST.get('evaluate','')
            relation.save()
            response_data['message'] = 'modified'
            return HttpResponse(json.dumps(response_data), content_type="application/json")
    else:
    	response_data['message'] = 'wrong_request'
    	return HttpResponse(json.dumps(response_data), content_type="application/json")
    	
def recommand(request):
    response_data = {}
    curtime = time.mktime(time.localtime()) 
    neartime = curtime + 10000000
    i = 0
    num = 0
    exist = 0
    if request.method=='GET' :
    	if 'name' in request.GET: name = request.GET['name']
    	else: name = request.user.person.name
    	try:    
    	    person = Person.objects.get(name=name)
    	except Exception:
    	    response_data['message'] = 'wrong_key'
            return HttpResponse(json.dumps(response_data), content_type="application/json")
        rooms = Room.objects.all()
        if len(rooms) == 0:
            response_data['message'] = 'null'
            return HttpResponse(json.dumps(response_data), content_type="application/json")
        
        for room in rooms:
            datetime = time.mktime(time.strptime(room.date,'%Y.%m.%d'))
            if datetime < neartime and datetime > curtime and len(Membership.objects.filter(room_id=room.id).filter(person_id=request.user.person.id)) == 0 :
            	    neartime = datetime
            if (room.slug == person.slug1 or room.slug == person.slug2) and curtime < datetime and Membership.objects.filter(room_id=room.id).filter(person_id=request.user.person.id) == '' :
                num += 1
        
        for room in rooms:
            if neartime == time.mktime(time.strptime(room.date,'%Y.%m.%d')) and len(Membership.objects.filter(room_id=room.id).filter(person_id=request.user.person.id)) == 0 :
                exist = room.id
        	i = i + 1
            	response_data['id'+str(i)] = room.id
            	response_data['name'+str(i)] = room.name
            	response_data['slug'+str(i)] = room.slug
	    	response_data['dscrp'+str(i)] = room.dscrp
	    	response_data['address'+str(i)] = room.address
	    	response_data['date'+str(i)] = room.date
	    	response_data['talk'+str(i)] = room.talk
	    	response_data['creator'+str(i)] = room.creator.username
	    	j = 0
	    	if len(room.members.all()) != 0:
            	    for roomer in room.members.all():
            	    	j = j + 1
        	        response_data['member'+str(i)+str(j)] = roomer.name
        	response_data['memnum'+str(i)] = j
        
        for room in rooms:    
            datetime = time.mktime(time.strptime(room.date,'%Y.%m.%d'))
            if (room.slug == person.slug1 or room.slug == person.slug2) and curtime < datetime and len(Membership.objects.filter(room_id=room.id).filter(person_id=request.user.person.id)) == 0 and room.id != exist :
            	i = i + 1
            	response_data['id'+str(i)] = room.id
            	response_data['name'+str(i)] = room.name
            	response_data['slug'+str(i)] = room.slug
	    	response_data['dscrp'+str(i)] = room.dscrp
	    	response_data['address'+str(i)] = room.address
	    	response_data['date'+str(i)] = room.date
	    	response_data['talk'+str(i)] = room.talk
	    	response_data['creator'+str(i)] = room.creator.username
	    	j = 0
	    	if len(room.members.all()) != 0:
            	    for roomer in room.members.all():
            	    	j = j + 1
        	        response_data['member'+str(i)+str(j)] = roomer.name
        	response_data['memnum'+str(i)] = j
            
        response_data['roomnum'] = i
        if i != 0 : response_data['message'] = 'ok'
        else : response_data['message'] = 'null'
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    else:
    	response_data['message'] = 'wrong_request'
    	return HttpResponse(json.dumps(response_data), content_type="application/json")    

def userLogin(request):
    response_data = {}
    global lasttime
    curtime = time.mktime(time.localtime()) 
    if curtime - lasttime > 10 :
        lasttime += 10
        people = Person.objects.all()
        for person in people :
            if person.bad > 3 :
                person.bad -= 1     
        for person in people :
            if person.credit < 5 :        
                person.credit *= 1.2 
        person.save()
    if request.method=='POST':
        username= request.POST.get('name','')
        password= request.POST.get('password','')
        user= auth.authenticate(username=username,password=password)
        if user and user.is_active:
            auth.login(request, user)
            response_data['message'] = 'login'
	    person = user.person
            if person == None:
            	response_data['message'] = 'bug'
            	return HttpResponse(json.dumps(response_data), content_type="application/json")  
            if person != None:
            	response_data['name'] = person.name
	    	response_data['dscrp'] = person.dscrp
	    	response_data['credit'] = str(person.credit)
	    	response_data['gender'] = person.gender	    
	    	i = 0
	    	if len(person.room_set.all()) != 0:
            	    for room in person.room_set.all():
            	        if Membership.objects.filter(room_id=room.id).get(person_id=person.id).allowed == False :
            	    	    continue
            	    	i = i + 1
        	    	response_data['room'+str(i)] = str(room.id)
        	response_data['roomnum'] = i    	
            return HttpResponse(json.dumps(response_data), content_type="application/json")
        elif user:
            response_data['message'] = 'not_active'
            return HttpResponse(json.dumps(response_data), content_type="application/json")
        else:
            response_data['message'] = 'wrong_password'
    	    return HttpResponse(json.dumps(response_data), content_type="application/json") 
    response_data['message'] = 'wrong_request'
    return HttpResponse(json.dumps(response_data), content_type="application/json") 
    
def userLogout(request):
    response_data = {}
    curtime=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime());
        
    user = request.user
    if request.method=='POST':
        username= request.POST.get('name','')
        if user and user.is_authenticated() and username == user.username :
            auth.logout(request)
            response_data['message'] = 'logout'    	
            return HttpResponse(json.dumps(response_data), content_type="application/json")
    response_data['message'] = 'not_logout'
    return HttpResponse(json.dumps(response_data), content_type="application/json")          

m = hashlib.md5()
secretkey = 'yangds'
def userRegister(request):
    response_data = {}
    curtime=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime());

    if request.method=='POST':
        username=request.POST.get('name','')	#username
        password1=request.POST.get('password1','')
        password2=request.POST.get('password2','')
        email=request.POST.get('email','')
        phone=request.POST.get('phone','')
        recall=request.POST.get('recall','')
        modify=request.POST.get('modify','')	#修改密码

	       
        if request.user.is_authenticated():     #已经登录
            if modify != '': 	#尝试修改密码
                if password1 == password2:
                    request.user.password = password1
                    request.user.save()
                    response_data['username'] = request.user.username
                    response_data['message'] = 'modified'
                    return HttpResponse(json.dumps(response_data), content_type="application/json")
                else:
                    response_data['message'] = 'not_consist'
                    return HttpResponse(json.dumps(response_data), content_type="application/json")
            '''
            else:    
                response_data['message'] = 'login'
                return HttpResponse(json.dumps(response_data), content_type="application/json")
            '''
        elif modify != '':	#修改密码失败
            response_data['message'] = 'not_login'
            return HttpResponse(json.dumps(response_data), content_type="application/json")
	elif recall == '':	#处理注册
            registerForm=RegisterForm({'name':username,'password1':password1,'password2':password2,'email':email})
            if not registerForm.is_valid():
                response_data['message'] = 'wrong_form'
                return HttpResponse(json.dumps(response_data), content_type="application/json")
                
            filterResult=User.objects.filter(username=username)	#用户名查重
            if len(filterResult)>0:
            	response_data['message'] = 'name_exist'
            	return HttpResponse(json.dumps(response_data), content_type="application/json")
            filterResult=User.objects.filter(email=email)	#邮箱查重
            if len(filterResult)>0:
            	response_data['message'] = 'email_exist'
            	return HttpResponse(json.dumps(response_data), content_type="application/json")
        
        if recall != '':	#尝试找回密码
            filterResult=User.objects.filter(email=email)
            if len(filterResult) == 0:	
            	response_data['message'] = 'not_exist'
            	return HttpResponse(json.dumps(response_data), content_type="application/json")
	
	#注册或找回密码从这里开始，设置信息并发邮件       
        if password1!=password2:
            response_data['message'] = 'not_consist'
            return HttpResponse(json.dumps(response_data), content_type="application/json")
        if re.search('.pku.edu.cn$', email, flags=0) == None:
            response_data['message'] = 'not_pku'
            return HttpResponse(json.dumps(response_data), content_type="application/json")
            
        if recall == '':
            user=User()
            user.username=username
            user.set_password(password1)
            user.email=email
        else:
            user = User.objects.get(email=email)
            user.set_password(password1)
        user.is_active = False
        user.save()
        
        if recall == '' :    
            person=Person()
            person.user_id=user.id  
            person.name=user.username  
            person.credit=8  
            person.save()
        else : person=user.person
            
        m.update(username.encode("ascii")+secretkey+str(random.randint(1,100000)))
        token = m.hexdigest()
        person.token = token
        person.save()
        message = '您好！欢迎使用北大人自己的线下活动应用pkulife，请点击下面的链接完成验证： '
        message = message + myip + ':8000/accounts/activate/?token='+str(token)+'&username='+user.username
        #attention here!
	if sendmail(email, 'pkulife注册验证', message ):
	    response_data['pid'] = person.user.id
	    response_data['uid'] = user.person.id
	    response_data['message'] = 'send'
            return HttpResponse(json.dumps(response_data), content_type="application/json")
	else: 
	    response_data['message'] = 'not_send'
            return HttpResponse(json.dumps(response_data), content_type="application/json")
    response_data['message'] = 'wrong_request'
    return HttpResponse(json.dumps(response_data), content_type="application/json")
    
def active_user(request):
    response_data = {}
    token = request.GET['token']
    username = request.GET['username']
    try:
	user = User.objects.get(username=username)
	truetoken = User.objects.get(username=username).person.token
    except User.DoesNotExist:
	response_data['message'] = 'not_exist'
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    if token != truetoken:
	response_data['message'] = 'wrong_token'
	response_data['token'] = token
	response_data['truetoken'] = truetoken
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    user.is_active = True
    user.save()
    response_data['亲爱的用户'] = '您已注册成功，欢迎使用PKULife'
    return HttpResponse(json.dumps(response_data), content_type="application/json")          
    
def display_meta(request):
    values = request.META.items()
    values.sort()
    html = []
    for k, v in values:
        html.append('<tr><td>%s</td><td>%s</td></tr>' % (k, v))
    return HttpResponse('<table>%s</table>' % '\n'.join(html))
