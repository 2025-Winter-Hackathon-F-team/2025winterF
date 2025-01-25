# 管理画面で表示したいモデルをimportし、記述する。
from django.contrib import admin
from .models import Users, YearGoals, MonthGoals, Todos, MessageMST

admin.site.register(Users)
admin.site.register(YearGoals)
admin.site.register(MonthGoals)
admin.site.register(Todos)
admin.site.register(MessageMST)