from flask import Blueprint, render_template, redirect, url_for, request, jsonify
from . import db
from .models import Photo
from .forms import PhotoCreateForm
from typing import List, Tuple, Any, Dict

photo_bp = Blueprint('photo_bp', __name__)

@photo_bp.route("/")
def index() -> str:
    photos: List[Tuple[Any]] = Photo.query.all()
    
    return render_template('index.html', photos=photos)

@photo_bp.route('/photos/new')
def new_photo_form() -> str:
    return render_template('photo_form.html')

@photo_bp.route('/photos', methods=['POST'])
def create_photo() -> str:
    data: Tuple[Any] = request.form
    
    try:
        PhotoCreateForm(title=data['title'], description=data['description'], image=str(data['image']))

    except ValueError as e:
        return jsonify({"error": e}), 400
    
    new_photo: Photo = Photo(title=data['title'], description=data['description'], image=str(data['image']))
    
    db.session.add(new_photo)
    db.session.commit()
    
    return render_template('photo_item.html', photo=new_photo)
    
@photo_bp.route('/photos<int:photo_id>/edit')
def edit_photo_form(photo_id: int) -> str:
    photo: Photo = Photo.query.get_or_404(photo_id)
    return render_template('photo_form.html', photo=photo)
    
@photo_bp.route('/photos/<int:photo_id>', methods=['DELETE'])
def delete_photo(photo_id: int) -> str:
    photo: Photo = Photo.query.get_or_404(photo_id)
        
    db.session.delete(photo)
    db.session.commit()
        
    photos: List[Tuple[Any]] = Photo.query.all()
        
    return redirect(url_for('photo_bp.index', photos=photos))
    
@photo_bp.route('/photos/<int:photo_id>', methods=['GET', 'POST'])
def update_photo(photo_id: int) -> str:
    photo: Photo = Photo.query.get_or_404(photo_id)
    
    if request.method == 'POST':
        data: Dict[str, str] = request.form

        
        try:
            photo_data: PhotoCreateForm = PhotoCreateForm(title=data['title'],description=data['description'], image=str(data['image']))

        except ValueError as e:
            return jsonify({"error": e}), 400
        
        photo.title = photo_data.title
        photo.description = photo_data.description
        photo.image = photo_data.image
        
        db.session.commit()
        
        return redirect(url_for('photo_bp.update_photo', photo_id=photo.id))
    
    return render_template('photo_item.html', photo=photo)   