from django import forms
import cluster_iq.settings


class CSVUploadForm(forms.Form):
    csv_file = forms.FileField(
        label="Upload CSV File",
        widget=forms.ClearableFileInput(attrs={
            'class': 'upload-file',
            'id': 'upload_csv',
            'accept': '.csv',
        }),
        help_text="Only .csv files are supported.",
    )

    def clean_csv_file(self):
        file = self.cleaned_data.get('csv_file')

        if file:
            if not file.name.endswith('.csv'):
                raise forms.ValidationError("This is not a valid CSV file.")

            if file.size > cluster_iq.settings.CSV_FILE_SIZE:
                raise forms.ValidationError(f"The file is too large. Please upload a file smaller than {cluster_iq.settings.CSV_FILE_SIZE} MB.")

        return file
