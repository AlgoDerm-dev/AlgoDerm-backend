from models import *
from api import oauth
from flask import Flask, request, jsonify, send_from_directory, Blueprint,abort

app_routes = Blueprint('app_routes', __name__)

@app_routes.route('/diseases', methods=['GET', 'POST'])
@oauth.require_oauth()
def allDiseases():
    if request.method == 'GET':
        query_params = request.args.to_dict()
        diseases = Disease.query.filter_by(**query_params).all() if query_params else Disease.query.all()
        if diseases:
            disease_response = list_model_to_dict(diseases, Disease)
            return jsonify({"result": disease_response})
        else:
            return 404 #add some response message for error
    else:
        disease = Disease(**request.json)
        if disease:
            db.session.add(disease)
            db.session.commit()
            disease_response = model_to_dict(disease, Disease)
            return jsonify({"result": disease_response})
        else:
            return 400 #add validation as to why 
#get one disease
@app_routes.route('/diseases/<disease_id>', methods=['GET',])
@oauth.require_oauth()
def uniqueDisease(disease_id):
    disease = Disease.query.filter_by(id = disease_id).first()
    if disease:
        disease_response = model_to_dict(disease, Disease)
        return jsonify({"result": disease_response})
    else:
        return 404


#all images under a disease id and post image of disease's url
@app_routes.route('/diseases/<disease_id>/images', methods=['GET', 'POST'])
@oauth.require_oauth()
def uniqueDiseaseImages(disease_id):
    if request.method == 'GET':
        disease_images = DiseaseImage.query.filter_by(disease_id = disease_id).all()
        if diseaseImage:
            disease_image_response = list_model_to_dict(disease_images, DiseaseImage)
            return jsonify({"result": disease_image_response})
        else:
            return 404
    else:
        disease_image = DiseaseImage(**request.json)
        if disease_image:
            db.session.add(disease_image)
            db.session.commit()
            disease_image_response = model_to_dict(disease_images, DiseaseImage)
            return jsonify({"result": disease_image_response})
        else:
            return 400 #give the exact reason why the post failed

@app_routes.route('/me/images', methods=['GET', 'POST'])
@oauth.require_oauth()
def userImages():
    if request.method == 'POST':
        
        
    else:
        user_images = UserImages.query.filter_by(id = request.oauth.user.id).all()
        if user_images:
            user_images_response = list_model_to_dict(user_images, UserImages)
            return jsonify({"result": disease_image_response})
        else:
            return 404 #provide reason 
