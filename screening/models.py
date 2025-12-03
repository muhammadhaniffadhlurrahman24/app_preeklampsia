from django.db import models
from django.conf import settings


class UserProfile(models.Model):
	"""Optional user profile extending Django User for additional info."""
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	full_name = models.CharField(max_length=200, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.full_name or self.user.username


class ScreeningSubmission(models.Model):
	"""Stores one screening form submission (32 fields from the form)."""
	user = models.ForeignKey(
		settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL
	)
	created_at = models.DateTimeField(auto_now_add=True)

	# Informasi dasar pasien
	patient_name = models.CharField(max_length=255)
	district_city = models.CharField(max_length=100, blank=True)
	patient_age = models.PositiveSmallIntegerField(null=True, blank=True)
	education_level = models.CharField(max_length=50, blank=True)
	current_occupation = models.CharField(max_length=100, blank=True)
	marital_status = models.CharField(max_length=50, blank=True)
	marriage_order = models.PositiveSmallIntegerField(null=True, blank=True)
	parity = models.CharField(max_length=50, blank=True)

	# Riwayat kehamilan & perencanaan
	new_partner_pregnancy = models.BooleanField(null=True)
	child_spacing_over_10_years = models.BooleanField(null=True)
	ivf_pregnancy = models.BooleanField(null=True)
	multiple_pregnancy = models.BooleanField(null=True)
	smoker = models.BooleanField(null=True)
	planned_pregnancy = models.BooleanField(null=True)

	# Riwayat pribadi & penyakit ibu
	family_history_pe = models.BooleanField(null=True)
	personal_history_pe = models.BooleanField(null=True)
	chronic_hypertension = models.BooleanField(null=True)
	diabetes_mellitus = models.BooleanField(null=True)
	kidney_disease = models.BooleanField(null=True)
	autoimmune_disease = models.BooleanField(null=True)
	aps_history = models.BooleanField(null=True)

	# Antropometri & pemeriksaan
	pre_pregnancy_weight = models.FloatField(null=True, blank=True)
	height_cm = models.FloatField(null=True, blank=True)
	bmi = models.FloatField(null=True, blank=True)
	lila_cm = models.FloatField(null=True, blank=True)
	systolic_bp = models.IntegerField(null=True, blank=True)
	diastolic_bp = models.IntegerField(null=True, blank=True)
	map_mmhg = models.FloatField(null=True, blank=True)
	hemoglobin = models.FloatField(null=True, blank=True)

	# Riwayat penyakit keluarga
	family_history_hypertension = models.BooleanField(null=True)
	family_history_kidney = models.BooleanField(null=True)
	family_history_heart = models.BooleanField(null=True)

	# Prediction result (optional)
	result = models.CharField(max_length=50, blank=True)
	confidence = models.CharField(max_length=20, blank=True)

	def __str__(self):
		return f"{self.patient_name} - {self.created_at:%Y-%m-%d %H:%M}"

