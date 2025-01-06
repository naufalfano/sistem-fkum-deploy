from django import forms 
from django.core.validators import FileExtensionValidator

class HasilUKMPPDForm(forms.Form):
    file = forms.FileField(validators=[FileExtensionValidator(['csv'])])
    
    def clean_file(self):
        file = self.cleaned_data['file']
        if not file.name.endswith('.csv'):
            raise forms.ValidationError('File harus dalam format csv.')
        return file