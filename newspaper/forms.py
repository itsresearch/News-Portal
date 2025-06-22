from .models import Comment
from django import forms

class CommentForm(forms.ModelForm):
    
    class Meta:
        model = Comment
        fields = ["post", "content"]


# class ContactForm(forms.ModelForm):

#     class Meta:
#         model = Contact
#         fields = "__all__"


# class NewsletterForm(forms.ModelForm):

#     class Meta:
#         model = Newsletter
#         fields = "__all__"
