from django.contrib import admin

# Register your models here.
from .models import Application, Subscriber, UserDefinedHost, HostMapping, Usage

admin.site.site_header = 'Community Cellular Admin'  # Updates the written text
admin.site.index_title = 'Community Cellular'  # Tab Title content
admin.site.site_title = 'Application Administration Panel'  # Tab title | sub_title


class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('host', 'throughput', 'timestamp')


admin.site.register(Application, ApplicationAdmin)
admin.site.register(Subscriber)
admin.site.register(UserDefinedHost)
admin.site.register(HostMapping)
admin.site.register(Usage)
