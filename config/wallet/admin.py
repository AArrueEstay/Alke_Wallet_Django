from django.contrib import admin
from .models import Usuario, Transaccion

# Register your models here.
admin.site.register(Usuario)
admin.site.register(Transaccion)