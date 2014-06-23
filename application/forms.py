import wtforms as forms
from wtforms import validators


class MessageForm(forms.Form):
    message_id = forms.IntegerField(label="message id",
                                    validators=[validators.required()])
    message_data = forms.StringField(label="content",
                                     validators=[validators.required()])