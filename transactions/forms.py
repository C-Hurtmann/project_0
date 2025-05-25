from django import forms
from .models import Transfer


class TransferForm(forms.ModelForm):
    class Meta:
        model = Transfer
        fields = ['income', 'outcome']

    def clean(self):
        cleaned_data = super().clean()
        income = cleaned_data.get('income')
        outcome = cleaned_data.get('outcome')

        if income and income.amount <= 0:
            self.add_error(
                'income', 'Selected income transaction is not positive.'
            )
        if outcome and outcome.amount >= 0:
            self.add_error(
                'outcome', 'Selected outcome transaction is not negative.'
            )
