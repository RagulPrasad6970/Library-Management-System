from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import Author, Book, BookCopy, Category, Loan, Member, Publisher, Reservation, StaffProfile


class StaffProfileInline(admin.StackedInline):
	model = StaffProfile
	extra = 0
	can_delete = False


class UserAdmin(BaseUserAdmin):
	inlines = (StaffProfileInline,)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
	list_display = ("name", "created_at")
	search_fields = ("name",)


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
	list_display = ("full_name", "created_at")
	search_fields = ("full_name",)


@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
	list_display = ("name", "created_at")
	search_fields = ("name",)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
	list_display = ("title", "isbn", "category", "publisher")
	search_fields = ("title", "isbn")
	list_filter = ("category", "publisher")


@admin.register(BookCopy)
class BookCopyAdmin(admin.ModelAdmin):
	list_display = ("accession_no", "book", "status", "shelf_location")
	search_fields = ("accession_no", "book__title", "book__isbn")
	list_filter = ("status",)


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
	list_display = ("member_id", "full_name", "email", "status")
	search_fields = ("member_id", "full_name", "email")
	list_filter = ("status",)


@admin.register(StaffProfile)
class StaffProfileAdmin(admin.ModelAdmin):
	list_display = ("user", "role", "created_at")
	search_fields = ("user__username", "user__email")
	list_filter = ("role",)


@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
	list_display = ("copy", "member", "issued_on", "due_on", "returned_on")
	search_fields = ("copy__accession_no", "member__member_id", "member__full_name")
	list_filter = ("issued_on", "due_on", "returned_on")


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
	list_display = ("book", "member", "status", "requested_on", "fulfilled_on")
	search_fields = ("book__title", "member__member_id", "member__full_name")
	list_filter = ("status",)

# Register your models here.
