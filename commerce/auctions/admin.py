from django.contrib import admin

from .models import User, Listing, Watchitem, Bid, Comments

# Register your models here.

admin.site.register(User)
admin.site.register(Listing)
admin.site.register(Watchitem)
admin.site.register(Bid)
admin.site.register(Comments)