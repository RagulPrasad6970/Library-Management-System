from decimal import Decimal

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class TimeStampedModel(models.Model):
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		abstract = True


class Category(TimeStampedModel):
	name = models.CharField(max_length=120, unique=True)
	description = models.TextField(blank=True)

	class Meta:
		ordering = ["name"]

	def __str__(self):
		return self.name


class Author(TimeStampedModel):
	full_name = models.CharField(max_length=150, unique=True)

	class Meta:
		ordering = ["full_name"]

	def __str__(self):
		return self.full_name


class Publisher(TimeStampedModel):
	name = models.CharField(max_length=150, unique=True)

	class Meta:
		ordering = ["name"]

	def __str__(self):
		return self.name


class Book(TimeStampedModel):
	isbn = models.CharField(max_length=20, unique=True)
	title = models.CharField(max_length=255)
	subtitle = models.CharField(max_length=255, blank=True)
	description = models.TextField(blank=True)
	category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="books")
	publisher = models.ForeignKey(Publisher, on_delete=models.SET_NULL, null=True, related_name="books")
	published_year = models.PositiveIntegerField(null=True, blank=True)
	language = models.CharField(max_length=64, default="English")
	pages = models.PositiveIntegerField(default=0)
	authors = models.ManyToManyField(Author, blank=True, related_name="books")

	class Meta:
		ordering = ["title"]

	def __str__(self):
		return f"{self.title} ({self.isbn})"


class BookCopy(TimeStampedModel):
	class Status(models.TextChoices):
		AVAILABLE = "AVAILABLE", "Available"
		ISSUED = "ISSUED", "Issued"
		RESERVED = "RESERVED", "Reserved"
		LOST = "LOST", "Lost"

	book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="copies")
	accession_no = models.CharField(max_length=30, unique=True)
	shelf_location = models.CharField(max_length=100)
	condition_notes = models.CharField(max_length=255, blank=True)
	status = models.CharField(max_length=20, choices=Status.choices, default=Status.AVAILABLE)

	class Meta:
		ordering = ["accession_no"]

	def __str__(self):
		return f"{self.book.title} - {self.accession_no}"


class Member(TimeStampedModel):
	class Status(models.TextChoices):
		ACTIVE = "ACTIVE", "Active"
		INACTIVE = "INACTIVE", "Inactive"

	member_id = models.CharField(max_length=30, unique=True)
	full_name = models.CharField(max_length=150)
	email = models.EmailField(unique=True)
	phone = models.CharField(max_length=20, blank=True)
	address = models.CharField(max_length=255, blank=True)
	status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE)

	class Meta:
		ordering = ["full_name"]

	def __str__(self):
		return f"{self.full_name} ({self.member_id})"


class StaffProfile(TimeStampedModel):
	class Role(models.TextChoices):
		ADMIN = "ADMIN", "Administrator"
		LIBRARIAN = "LIBRARIAN", "Librarian"
		ASSISTANT = "ASSISTANT", "Assistant"
		VIEWER = "VIEWER", "Viewer"

	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="staff_profile")
	role = models.CharField(max_length=20, choices=Role.choices, default=Role.VIEWER)

	class Meta:
		ordering = ["user__username"]

	def __str__(self):
		return f"{self.user.username} - {self.get_role_display()}"


class Loan(TimeStampedModel):
	copy = models.ForeignKey(BookCopy, on_delete=models.PROTECT, related_name="loans")
	member = models.ForeignKey(Member, on_delete=models.PROTECT, related_name="loans")
	issued_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
	issued_on = models.DateField(default=timezone.localdate)
	due_on = models.DateField()
	returned_on = models.DateField(null=True, blank=True)
	fine_per_day = models.DecimalField(max_digits=7, decimal_places=2, default=Decimal("10.00"))

	class Meta:
		ordering = ["-issued_on"]

	def __str__(self):
		return f"{self.copy.accession_no} -> {self.member.member_id}"

	@property
	def is_overdue(self):
		reference_date = self.returned_on or timezone.localdate()
		return reference_date > self.due_on

	@property
	def overdue_days(self):
		reference_date = self.returned_on or timezone.localdate()
		if reference_date <= self.due_on:
			return 0
		return (reference_date - self.due_on).days

	@property
	def fine_amount(self):
		return Decimal(self.overdue_days) * self.fine_per_day


class Reservation(TimeStampedModel):
	class Status(models.TextChoices):
		ACTIVE = "ACTIVE", "Active"
		FULFILLED = "FULFILLED", "Fulfilled"
		CANCELLED = "CANCELLED", "Cancelled"

	member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="reservations")
	book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="reservations")
	status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE)
	requested_on = models.DateTimeField(auto_now_add=True)
	fulfilled_on = models.DateTimeField(null=True, blank=True)

	class Meta:
		ordering = ["-requested_on"]

	def __str__(self):
		return f"Reservation {self.book.title} - {self.member.member_id}"
