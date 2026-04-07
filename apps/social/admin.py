from django.contrib import admin
from .models import FriendRequest, Friendship, Block, Report

admin.site.register(FriendRequest)
admin.site.register(Friendship)
admin.site.register(Block)
admin.site.register(Report)
