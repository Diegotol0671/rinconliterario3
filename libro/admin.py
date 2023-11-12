from django.contrib import admin
from .models import libro
from .models import comentario

class comentariolibro(admin.ModelAdmin):
    readonly_fields = ("completado", )

# Register your models here.
admin.site.register(libro)
admin.site.register(comentario, comentariolibro)