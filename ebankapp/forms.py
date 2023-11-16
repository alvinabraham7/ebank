from django import forms
from .models import Registration, Branch, District


class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Registration
        fields = ['name', 'dob', 'age', 'gender', 'mail_id', 'mob_no', 'address', 'district', 'branch', 'account_type',
                  'credit_card', 'debit_card', 'check_book']
    account_type = forms.ChoiceField(choices=[('Select', 'Select'), ('savings', 'Savings Account'),
                                              ('current', 'Current Account')],
                                     label='Account Type')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['branch'].queryset = Branch.objects.none()

        if 'district' in self.data:
            try:
                district_id = int(self.data.get('district'))
                self.fields['branch'].queryset = Branch.objects.filter(district_id=district_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['branch'].queryset = self.instance.district.branch_set.order_by('name')
