from django import forms

from .models import Book, BookCopy, Loan, Member


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = [
            "isbn",
            "title",
            "subtitle",
            "description",
            "category",
            "publisher",
            "published_year",
            "language",
            "pages",
        ]


class BookCopyForm(forms.ModelForm):
    class Meta:
        model = BookCopy
        fields = ["book", "accession_no", "shelf_location", "condition_notes", "status"]


class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ["member_id", "full_name", "email", "phone", "address", "status"]


class IssueBookForm(forms.Form):
    copy = forms.ModelChoiceField(queryset=BookCopy.objects.none(), label="Book Copy")
    member = forms.ModelChoiceField(queryset=Member.objects.none())
    due_on = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["copy"].queryset = BookCopy.objects.filter(status=BookCopy.Status.AVAILABLE)
        self.fields["member"].queryset = Member.objects.filter(status=Member.Status.ACTIVE)


class ReturnBookForm(forms.Form):
    loan = forms.ModelChoiceField(queryset=Loan.objects.none(), label="Active Loan")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["loan"].queryset = Loan.objects.filter(returned_on__isnull=True).select_related(
            "copy", "member", "copy__book"
        )
