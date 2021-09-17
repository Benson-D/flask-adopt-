"""Forms for adopt app."""

from typing import Any
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField 
from wtforms.validators import InputRequired, Optional, URL, AnyOf

class AddPetForm(FlaskForm):
    """Form for adding pets."""

    name = StringField("Pet Name", validators=[InputRequired()])
    species = StringField("Species", validators=[InputRequired(), AnyOf(["dog", "cat", "porcupine"])])
    photo_url = StringField("Photo URL", validators=[Optional(), URL()])
    age = SelectField("Age", 
        choices=[
            ("baby", "Baby"),
            ("young", "Young"),
            ("adult", "Adult"),
            ("senior", "Senior")], validators=[InputRequired()])
    notes = TextAreaField("Notes", validators=[Optional()])
