from django.contrib import admin 
from .models import User , UserProfile , Election , Candidate , VoteBlocks

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Election)
admin.site.register(Candidate)
admin.site.register(VoteBlocks)