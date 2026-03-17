from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Count, Q
from django.shortcuts import redirect, render
from django.utils import timezone

from .forms import BookCopyForm, BookForm, IssueBookForm, MemberForm, ReturnBookForm
from .models import Book, BookCopy, Loan, Member
from .rbac import capability_required


@login_required
def dashboard(request):
	active_loans = Loan.objects.filter(returned_on__isnull=True)
	context = {
		"book_count": Book.objects.count(),
		"copy_available": BookCopy.objects.filter(status=BookCopy.Status.AVAILABLE).count(),
		"member_count": Member.objects.filter(status=Member.Status.ACTIVE).count(),
		"active_loans": active_loans.count(),
		"overdue_count": active_loans.filter(due_on__lt=timezone.localdate()).count(),
		"recent_loans": Loan.objects.select_related("copy", "copy__book", "member")[:10],
		"top_books": Book.objects.annotate(total_issued=Count("copies__loans")).order_by("-total_issued")[:5],
	}
	return render(request, "library/dashboard.html", context)


@login_required
def book_list(request):
	query = request.GET.get("q", "").strip()
	books = Book.objects.select_related("category", "publisher").prefetch_related("authors")
	if query:
		books = books.filter(Q(title__icontains=query) | Q(isbn__icontains=query))
	return render(request, "library/books/list.html", {"books": books, "query": query})


@login_required
@capability_required("manage_catalog")
def book_create(request):
	form = BookForm(request.POST or None)
	if request.method == "POST" and form.is_valid():
		form.save()
		messages.success(request, "Book added successfully.")
		return redirect("book_list")
	return render(request, "library/books/form.html", {"form": form, "title": "Add New Book"})


@login_required
@capability_required("manage_catalog")
def copy_create(request):
	form = BookCopyForm(request.POST or None)
	if request.method == "POST" and form.is_valid():
		form.save()
		messages.success(request, "Book copy added successfully.")
		return redirect("book_list")
	return render(request, "library/books/form.html", {"form": form, "title": "Add Book Copy"})


@login_required
def member_list(request):
	query = request.GET.get("q", "").strip()
	members = Member.objects.all()
	if query:
		members = members.filter(
			Q(member_id__icontains=query) | Q(full_name__icontains=query) | Q(email__icontains=query)
		)
	return render(request, "library/members/list.html", {"members": members, "query": query})


@login_required
@capability_required("manage_members")
def member_create(request):
	form = MemberForm(request.POST or None)
	if request.method == "POST" and form.is_valid():
		form.save()
		messages.success(request, "Member registered successfully.")
		return redirect("member_list")
	return render(request, "library/members/form.html", {"form": form})


@login_required
@capability_required("manage_circulation")
def issue_book(request):
	form = IssueBookForm(request.POST or None)
	if request.method == "POST" and form.is_valid():
		with transaction.atomic():
			copy = form.cleaned_data["copy"]
			loan = Loan.objects.create(
				copy=copy,
				member=form.cleaned_data["member"],
				due_on=form.cleaned_data["due_on"],
				issued_by=request.user,
			)
			copy.status = BookCopy.Status.ISSUED
			copy.save(update_fields=["status", "updated_at"])
		messages.success(request, f"Book issued successfully. Loan #{loan.id} created.")
		return redirect("loan_list")
	return render(request, "library/circulation/issue.html", {"form": form})


@login_required
@capability_required("manage_circulation")
def return_book(request):
	form = ReturnBookForm(request.POST or None)
	if request.method == "POST" and form.is_valid():
		with transaction.atomic():
			loan = form.cleaned_data["loan"]
			loan.returned_on = timezone.localdate()
			loan.save(update_fields=["returned_on", "updated_at"])
			copy = loan.copy
			copy.status = BookCopy.Status.AVAILABLE
			copy.save(update_fields=["status", "updated_at"])
		messages.success(request, f"Book returned. Fine amount: Rs. {loan.fine_amount}")
		return redirect("loan_list")
	return render(request, "library/circulation/return.html", {"form": form})


@login_required
def loan_list(request):
	loans = Loan.objects.select_related("copy", "copy__book", "member")
	return render(
		request,
		"library/circulation/loans.html",
		{
			"active_loans": loans.filter(returned_on__isnull=True),
			"completed_loans": loans.filter(returned_on__isnull=False)[:25],
		},
	)
