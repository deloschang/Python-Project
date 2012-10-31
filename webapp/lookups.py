from django.db.models import Q
from django.utils.html import escape
#from webapp.models import *
from django.contrib.auth.models import User
from ajax_select import LookupChannel


# User autocomplete for invitation system
class UserLookup(LookupChannel):
    model = User

    #def get_query(self,q,request):
        #return Meme.objects.filter(Q(title__icontains=q) | Q(creator__istartswith=q)).order_by('title')
    #def get_query(self,q,request):
        #return User.objects.filter(username__icontains=q).order_by('username')
    def get_query(self,q,request):
        return User.objects.filter(Q(username__icontains=q) | Q(email__istartswith=q)).order_by('username')
    
    def get_result(self,obj):
        u""" result is the simple text that is the completion of what the person typed """
        return obj.username

    def format_match(self,obj):
        """ (HTML) formatted item for display in the dropdown """
        return self.format_item_display(obj)

    def format_item_display(self,obj):
        """ (HTML) formatted item for displaying item in the selected deck area """
        #return u"%s<div><i>%s</i></div>" % (escape(obj.username),escape(obj.email))
        return u"%s<div><i>%s</i></div>" % (escape(obj.username),escape(obj.get_profile().url_username))

    # ensure nobody can get json by just knowing URL
    def check_auth(self, request):
        if request.user:
            return True
