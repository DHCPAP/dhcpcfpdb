from django.contrib import admin
from django.utils.html import format_html

from dhcpfpdb.models import DhcpVendor, UserAgent
from dhcpfpdb.models import DhcpFingerprint
from dhcpfpdb.models import Dhcp6Fingerprint
from dhcpfpdb.models import Dhcp6Enterprise, MacVendor
from dhcpfpdb.models import Device, Combination


class CombinationInline(admin.TabularInline):
    model = Combination


@admin.register(DhcpFingerprint)
class DhcpFingerprintAdmin(admin.ModelAdmin):
    list_display = ('value', 'created_at', 'updated_at', 'ignored')
    list_filter = (# 'value',
                   'ignored', 
                   # ('combination', admin.RelatedOnlyFieldListFilter),
                  )
    inlines = [
        CombinationInline,
    ]


@admin.register(Combination)
class CombinationAdmin(admin.ModelAdmin):
    list_display = ('device', 'score', 
                    'dhcp_fingerprint',
                    # 'user_agent',
                    'version',
                    'dhcp_vendor', 'mac_vendor',
                    'submitter_id', 'dhcp6_fingerprint',
                    'dhcp6_enterprise', 'fixed')
 
    list_filter = ('fixed', 'dhcp_fingerprint', 'dhcp_vendor')

    def user_agent_column_size(self):
        return format_html(
            '<th scope="col" class="sortable column-user_agent" widht="15px">'
            # self.user_agent,
        )


admin.site.register(DhcpVendor)
admin.site.register(UserAgent)
# admin.site.register(DhcpFingerprint)
admin.site.register(Dhcp6Fingerprint)
admin.site.register(Dhcp6Enterprise)
admin.site.register(MacVendor)
admin.site.register(Device)
# admin.site.register(Combination)
