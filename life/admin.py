from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
 
from .models import Person, Room, Membership, Friendship
 
class PersonAdmin(admin.ModelAdmin):
    list_display = ('name', 'credit',)
 
class RoomAdmin(admin.ModelAdmin):
    list_display = ('name',)
    
class MembershipAdmin(admin.ModelAdmin):
    list_display = ('person', 'room', )
    
class FriendshipAdmin(admin.ModelAdmin):
    list_display = ('person1', 'person2', 'rated')
    
class UserProfileInline(admin.StackedInline):  
    model=Person  
    fk_name='user'  
    max_num=1  
      
class UserProfileAdmin(UserAdmin):  
    inlines = [UserProfileInline, ]  

admin.site.register(Person, PersonAdmin)
admin.site.register(Room, RoomAdmin)
admin.site.register(Membership, MembershipAdmin)
admin.site.register(Friendship, FriendshipAdmin)
admin.site.unregister(User)  
admin.site.register(User,UserProfileAdmin) 
