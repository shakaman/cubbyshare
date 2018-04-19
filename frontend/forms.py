from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField, SubmitField
from wtforms.validators import DataRequired, ValidationError


class DataForm(FlaskForm):
    secrets = TextAreaField(u'Your data', validators=[DataRequired()])
    submit = SubmitField("Create")

    def validate_secrets(self, field):
        if field.data == '':
            raise ValidationError("No secrets found")
