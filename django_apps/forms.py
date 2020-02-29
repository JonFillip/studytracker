from django import forms
from .models import Topic, Entry


class TopicForm(forms.ModelForm):
    """A class that defines the form in which a user can enter in a topic."""

    class Meta:
        """This class tells django which model to base the form on and the
        fields to include in the form."""
        model = Topic
        fields = ['text']
        labels = {'text': ''}


class EntryForm(forms.ModelForm):
    """A class that defines the form in which a user can fill in an entry to
    a topic."""

    class Meta:
        """This meta class tells django which model to base the form for
        entries on and the fields to include in the form."""
        model = Entry
        fields = ['text']
        labels = {'text': 'Entry:'}
        widgets = {'text': forms.Textarea(attrs={'cols': 80})}
