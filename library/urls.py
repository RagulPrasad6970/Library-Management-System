from django.urls import path

from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("books/", views.book_list, name="book_list"),
    path("books/new/", views.book_create, name="book_create"),
    path("copies/new/", views.copy_create, name="copy_create"),
    path("members/", views.member_list, name="member_list"),
    path("members/new/", views.member_create, name="member_create"),
    path("circulation/issue/", views.issue_book, name="issue_book"),
    path("circulation/return/", views.return_book, name="return_book"),
    path("circulation/loans/", views.loan_list, name="loan_list"),
]
