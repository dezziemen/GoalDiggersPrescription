import django.forms as forms
from accounts.models import CustomUser


class EditCustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ["user_type", "email", "full_name", "phone_number", "address", ]

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        matching_emails = CustomUser.objects.exclude(pk=self.instance.pk).filter(email=email)
        if matching_emails.exists():
            raise forms.ValidationError(f"Email {email} is already in use. ")
        else:
            return email

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        matching_phone_number = CustomUser.objects.exclude(pk=self.instance.pk).filter(phone_number=phone_number)
        if matching_phone_number.exists():
            raise forms.ValidationError(f"Phone number {phone_number} is already in use.")
        else:
            return phone_number

    def save(self, commit=True):
        account = super(EditCustomUserForm, self).save(commit=False)
        account.email = self.cleaned_data['email']
        account.phone_number = self.cleaned_data['phone_number']
        account.full_name = self.cleaned_data['full_name']
        account.address = self.cleaned_data['address']
        account.user_type = self.cleaned_data['user_type']
        if commit:
            account.save()
        return account
