import os
from flask import Flask, render_template, request, redirect, url_for, jsonify
from models import db, User, Scheme, Like, Comment
from sqlalchemy import func

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "social_schemes.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    print("Index page accessed")
    categories = db.session.query(Scheme.schemeCategory).distinct().all()
    return render_template('categories.html', categories=[c[0] for c in categories])


@app.route('/category/<category>')
def category_view(category):
    schemes = Scheme.query.filter_by(schemeCategory=category).all()
    # Optional: get sub-category grouping by tags or level if needed
    return render_template('category_view.html', category=category, schemes=schemes)

@app.route('/like/<int:scheme_id>', methods=['POST'])
def like_scheme(scheme_id):
    user_id = 1  # Replace with actual user session system
    existing_like = Like.query.filter_by(user_id=user_id, scheme_id=scheme_id).first()
    if not existing_like:
        like = Like(user_id=user_id, scheme_id=scheme_id)
        db.session.add(like)
        db.session.commit()
    like_count = Like.query.filter_by(scheme_id=scheme_id).count()
    return jsonify({'success': True, 'likes': like_count})

@app.route('/comment/<int:scheme_id>', methods=['POST'])
def comment_scheme(scheme_id):
    content = request.json.get('content', '')
    if content.strip():
        comment = Comment(content=content, user_id=1, scheme_id=scheme_id)
        db.session.add(comment)
        db.session.commit()
    comments = Comment.query.filter_by(scheme_id=scheme_id).order_by(Comment.timestamp.desc()).all()
    comments_list = [{'content': c.content, 'timestamp': c.timestamp.strftime('%Y-%m-%d %H:%M:%S')} for c in comments]
    return jsonify(comments_list)

@app.route('/comments/<int:scheme_id>', methods=['GET'])
def get_comments(scheme_id):
    comments = Comment.query.filter_by(scheme_id=scheme_id).order_by(Comment.timestamp.desc()).all()
    comments_list = [{'content': c.content, 'timestamp': c.timestamp.strftime('%Y-%m-%d %H:%M:%S')} for c in comments]
    return jsonify(comments_list)

if __name__ == '__main__':
    app.run(debug=True)
