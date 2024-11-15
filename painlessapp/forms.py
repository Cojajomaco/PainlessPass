# Upon this rock, I will build my church.
from django import forms
from django.contrib.auth.models import User
from .models import UserPass, Folder


# Form for registering users. It is largely copied from the Django UserCreationForm example.
# The reason for using the actual code is for better customization and possible tie-in to the
# extended user model of the PainlessPass app.
class RegistrationForm(forms.ModelForm):
    error_messages = {
        'password_mismatch': "The two password fields didn't match.",
    }
    password1 = forms.CharField(label="Password",
                                widget=forms.PasswordInput)
    password2 = forms.CharField(label="Password confirmation",
                                widget=forms.PasswordInput,
                                help_text="Enter the same password as above, for verification.")

    class Meta:
        model = User
        fields = ("username",)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


# Form for creating new password items.
class NewPasswordForm(forms.ModelForm):
    class Meta:
        model = UserPass
        fields = ["name", "username", "password", "uri", "folder", "note", ]

    # Restrict the "folder" field to folders only available to the user.
    def __init__(self, *args, **kwargs):
        user_id = kwargs.pop("user_id")
        super().__init__(*args, **kwargs)
        self.fields["folder"].queryset = Folder.objects.filter(user_id=user_id.pk).order_by("name")
        # Try to get the default "No Folder" object as initial value.
        try:
            self.fields["folder"].initial = Folder.objects.get(user_id=user_id.pk, name="No Folder")
        except Exception:
            pass


# Form for creating new folder items.
class NewFolderForm(forms.ModelForm):
    class Meta:
        model = Folder
        fields = ["name", ]

    # Restrict the "folder" field to folders only available to the user.
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
