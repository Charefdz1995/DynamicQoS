from django import forms
from .models import *


class AddApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ('business_type', 'business_app', 'app_priority', 'drop_prob')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["business_app"].queryset = BusinessApp.objects.none()

        if 'BusinessType' in self.data:
            try:
                business_type_id = int(self.data.get('BusinessType'))
                self.fields['business_app'].queryset = BusinessApp.objects.filter(
                    business_type_id=business_type_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['business_app'].queryset = self.instance.BusinessType.BusinessApp_set.order_by('name')


class AddInputPolicyForm(forms.ModelForm):
    class Meta:
        model = PolicyIn
        fields = '__all__'
