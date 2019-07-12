from django.contrib import admin
from investment_bot.models import user_database,Section_Details,Amount_Restrictions,Section_Deduction

admin.site.register(user_database)
admin.site.register(Amount_Restrictions)
admin.site.register(Section_Details)
admin.site.register(Section_Deduction)
# Register your models here.
