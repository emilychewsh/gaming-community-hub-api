from flask_restful import Resource
from config import db 
from models import User, Game, Review, ReviewLike
from flask import make_response, session, request

class ReviewLikeController(Resource):
    def post(self):
        user_id = session.get('user_id')
        review_id = request.json.get('review_id')
        is_like = bool(request.json.get('is_like'))

        if not user_id:
            return make_response({"error": "User not logged in. Please sign in."}, 401)
        
        if not review_id or is_like is None:
            return make_response({"error": "Review ID and like status are required"}, 400)
        
        user = User.query.get(user_id)
        if not user:
            return make_response({"error": "User not found"}, 404)
        
        review = Review.query.get(review_id)
        if not review:
            return make_response({"error": "Review not found"}, 404)
        
        #Check if like/dislike already exists 
        existing_like = ReviewLike.query.filter_by(user_id=user_id, review_id=review_id).first()

        if existing_like:
            existing_like.is_like = is_like
            db.session.commit()
            return make_response({"message": "You have already updated this review"}, 200)
        else:
            new_like = ReviewLike(
                user_id=user_id, 
                review_id=review_id, 
                is_like=is_like)
            db.session.add(new_like)
            db.session.commit()
            return make_response({"message": "Like status updated successfully"}, 201)
        
    def delete(self, review_id):
        user_id = session.get('user_id')

        if not user_id:
            return make_response({"error": "User not logged in. Please sign in."}, 401)
        
        # Find the like/dislike entry to delete
        existing_like = ReviewLike.query.filter_by(user_id=user_id, review_id=review_id).first()

        if not existing_like:
            return make_response({"error": "Like/dislike entry not found"}, 404)
        
        db.session.delete(existing_like)
        db.session.commit()
        return make_response({"message": "Like/dislike removed"}, 200)