from flask import render_template,request,redirect,url_for,abort
from . import main
from .forms import UpdateProfile,PitchForm
from ..models import User,Pitch
from flask_login import login_required
from .. import db,photos
from ..models import User,Pitch
from flask_login import login_required, current_user
import markdown2



# Views
@main.route('/')
def index():
    pitches = Pitch.query.all()
    business = Pitch.filter_by(catogory='bussiness').all()
    job = Pitch.filter_by(catogory='job').all()
    interview = Pitch.filter_by(catogory='interview').all()
    title = 'Welcome to to your one minute'
    return render_template('index.html',title = title,business = business, job = job, interview = interview)



@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user)


@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()
    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

    return render_template('profile/update.html',form =form)   


@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))


@main.route('/pitch',methods = ['GET', 'POST'])
@login_required
def new_pitch(id):
    form = PitchForm()
    if form.validate_on_submit():
        title = form.title.data
        category = form.category.data
        description = form.category.data
        new_pitch = Pitch(title=title,category= category,description= description)
        new_pitch.save_pitch()
        db.session.add(new_pitch)
        db.session.commit()
        return redirect(url_for('main.index',id = pitch_id))
        
    return render_template('new_pitch.html',form = form)


@main.route('/pitch/new')
def single_pitch(id):
    pitch = Pitch.query.get(id)
         

    return render_template('pitches.html')    