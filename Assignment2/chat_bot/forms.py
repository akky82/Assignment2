from django import forms


class ChatBotForm(forms.Form):
    question = forms.CharField(label='You: ', max_length=100, required=True,
                               widget=forms.TextInput(attrs={
                                   'placeholder': '*Ask your question here',
                                   'size': 50
                               }))
