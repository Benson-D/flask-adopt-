"""Flask app for adopt app."""

from flask import Flask, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension


from models import db, connect_db, Pet
from forms import AddPetForm, EditPetForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///adopt"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.config['SECRET_KEY'] = "secret"
# In development keep ON 
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)

# Don't forget to db.drop_all() incase of errors 
db.create_all()

# Having the Debug Toolbar show redirects explicitly is often useful;
# however, if you want to turn it off, you can uncomment this line:
#
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)

@app.get('/') 
def render_pet_list(): 
    """Render pet_list"""

    pets = Pet.query.all()

    return render_template('pet-list.html', pets=pets)

@app.route("/add", methods=["GET", "POST"])
def add_pet():
    """Pet add form; handle adding."""

    form = AddPetForm()

    if form.validate_on_submit():
        name = form.name.data
        species = form.species.data
        photo_url = form.photo_url.data
        age = form.age.data
        notes = form.notes.data
        
        pet = Pet(name=name, 
            species=species, 
            photo_url=photo_url, 
            age=age, 
            notes=notes)
        # breakpoint()
        db.session.add(pet)
        db.session.commit()

        flash(f"Added {name} the {species}")
        return redirect("/")

    else:
        return render_template(
            "add-pet-form.html", form=form)

# ASK about validation rendering display through form route 
@app.route("/<int:pet_id>", methods=["GET", "POST"])
def edit_form(pet_id):
    # SHORT and sweet to the point 
    """Pet display profile edit form handling."""
    pet = Pet.query.get_or_404(pet_id)

    form = EditPetForm(obj=pet)
    # REMEMBER OBJ 

    if form.validate_on_submit():
        pet.photo_url = form.photo_url.data
        pet.notes = form.notes.data
        pet.available = form.available.data
        
        # breakpoint()
        db.session.commit()

        flash(f"Edited {pet.name}!")
        return redirect(f"/{pet_id}")

    else:
      
        return render_template(
            "pet-display-edit.html", form=form, pet=pet)
