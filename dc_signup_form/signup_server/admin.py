from django.contrib import admin
from .models import Token

class TokenAdmin(admin.ModelAdmin):
    readonly_fields = ('token',)

admin.site.register(Token, TokenAdmin)
