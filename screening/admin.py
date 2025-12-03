from django.contrib import admin
from .models import UserProfile, ScreeningSubmission


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
	list_display = ("user", "full_name", "created_at")
	search_fields = ("user__username", "full_name")


@admin.register(ScreeningSubmission)
class ScreeningSubmissionAdmin(admin.ModelAdmin):
	list_display = (
		"id",
		"patient_name",
		"user",
		"created_at",
		"result",
		"confidence",
	)
	search_fields = ("patient_name", "user__username", "result")
	list_filter = ("result", "created_at")
	readonly_fields = ("created_at",)

