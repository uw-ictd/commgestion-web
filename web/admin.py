from django.contrib import admin

# Register your models here.
from django.utils.html import format_html

from .models import Application, Subscriber, UserDefinedHost, HostMapping, Usage

admin.site.site_header = 'Community Cellular Admin'  # Updates the written text
admin.site.index_title = 'Community Cellular'  # Tab Title content
admin.site.site_title = 'Application Administration Panel'  # Tab title | sub_title


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('host', 'throughput', 'timestamp')


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('user', 'phonenumber', 'display_name', 'imsi', 'guti', 'is_local', 'role', 'connectivity_status',
                    'last_time_online', 'rate_limit_kbps')


@admin.register(UserDefinedHost)
class UserDefinedHostAdmin(admin.ModelAdmin):
    list_display = ('name', 'view_user_defined_host')

    @staticmethod
    def view_user_defined_host(self):
        return format_html('<a class="button" target="_blank" href="https://{}">View</a>'.format(self.name))


admin.site.register(HostMapping)
admin.site.register(Usage)
