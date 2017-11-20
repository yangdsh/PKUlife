from django.test import TestCase
from django.test.client import Client
import time

class ViewTest(TestCase):
    def test1(self):
    	c = Client()
        response1 = c.post('/accounts/register/', {'name':'linfuqi', 'password1':'999999', 'password2':'999999', 'email':'yangds@pku.edu.cn', 'phone':'1'})
        self.assertEqual(response1.status_code, 200)
        print response1.content
    	   
        response2 = c.post('/person/', {'name':'linfuqi', 'newname':'lin', 'credit':0.5, })
        self.assertEqual(response2.status_code, 200)
        print response2.content
        
        d = Client()
        response3 = d.get('/accounts/activate/', {'token':'3f57857cf5a809da2148a03df681d233', 'username':'linfuqi', })
        self.assertEqual(response3.status_code, 200)
        print response3.content
        
        response4 = d.post('/accounts/login/', {'name':'linfuqi', 'password':'999999', })
        self.assertEqual(response4.status_code, 200)
        print response4.content
        
        responsep = d.post('/accounts/register/', {'name':'linfuqi', 'password1':'000000', 'password2':'000000', 'modify':'1'})
        self.assertEqual(responsep.status_code, 200)
        print responsep.content
        
        response5 = d.post('/room/', {'name':'shixi', 'slug':'work', 'create':'1', })
        self.assertEqual(response5.status_code, 200)
        print response5.content
        
        response6 = d.post('/person/', {'name':'linfuqi', 'newname':'lin', })
        self.assertEqual(response6.status_code, 200)
        print response6.content
        
        response7 = d.post('/room/', {'newname':'wangluoshixi', 'slug':'work', 'id':'1', })
        self.assertEqual(response7.status_code, 200)
        print response7.content
        
        response8 = d.post('/room/', {'name':'wangluoshixi', 'slug':'play', 'create':'1', })
        self.assertEqual(response8.status_code, 200)
        print response8.content
        
        response9 = d.get('/room/', {'name':'wangluoshixi', })
        self.assertEqual(response9.status_code, 200)
        print response9.content
        
        responsem = d.post('/membership/', {'name':'lin', 'roomid':'1', 'create':'1', 'application':'hello', })
        self.assertEqual(responsem.status_code, 200)
        print responsem.content
        
        responsem = d.post('/membership/', {'name':'lin', 'roomid':'1', 'varify':'1', 'application':'hello', })
        self.assertEqual(responsem.status_code, 200)
        print responsem.content
        
        responsem = d.get('/membership/', {'name':'lin', 'roomid':'1', })
        self.assertEqual(responsem.status_code, 200)
        print responsem.content
