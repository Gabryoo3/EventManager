from django import forms
from .models import Event, Category


class EventForm(forms.ModelForm):

    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = Event
        fields = ['title', 'description','category','price', 'date','time','seats','image']
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }