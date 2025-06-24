from django.contrib import admin
from .models import CustomUser, Testimonial, Service, WhyChooseUs, ServiceStep, ServicePageContent, Company, ActivityPageContent, WastePickupRequest, Reward, Transaction, Hero, FeatureCard, UpgradeRequest
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

admin.site.register(CustomUser)
admin.site.register(Company)
admin.site.register(WastePickupRequest)
admin.site.register(Reward)
admin.site.register(Transaction)
admin.site.register(Hero)
admin.site.register(FeatureCard)
admin.site.register(Service)
admin.site.register(WhyChooseUs)
admin.site.register(ServiceStep)
admin.site.register(ServicePageContent)
admin.site.register(ActivityPageContent)



@admin.register(UpgradeRequest)
class UpgradeRequestAdmin(admin.ModelAdmin):
    list_display = ['user', 'company_name', 'approved', 'declined', 'created_at']
    list_filter = ['approved', 'declined']
    actions = ['approve_requests', 'decline_requests']

    def save_model(self, request, obj, form, change):
        if change:
            old_obj = UpgradeRequest.objects.get(pk=obj.pk)
            if not old_obj.approved and obj.approved:
                # Send approval email
                subject = "Your Upgrade Request Has Been Approved"
                html_message = render_to_string('upgrade/email_approved.html', {'user': obj.user})
                email = EmailMessage(subject, html_message, to=[obj.user.email])
                email.content_subtype = "html"
                email.send()
            elif not old_obj.declined and obj.declined:
                # Send rejection email
                subject = "Your Upgrade Request Was Rejected"
                html_message = render_to_string('upgrade/email_rejected.html', {'user': obj.user})
                email = EmailMessage(subject, html_message, to=[obj.user.email])
                email.content_subtype = "html"
                email.send()
        super().save_model(request, obj, form, change)


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('user', 'text', 'approved', 'created_at')
    list_filter = ('approved',)
    search_fields = ('user__username', 'text')        