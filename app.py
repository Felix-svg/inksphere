from flask import make_response, request
from config import bcrypt, api
from flask_restful import Resource
from flask_login import login_required, logout_user, login_user
from config import app, db, login_manager
from models import User, Blog, Comment


@app.route('/', methods=['GET'])
def home():
    return make_response({"message": "InkSphere API"})


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()

        if not data:
            return make_response({"error":"No input data provided"}, 400)

        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return make_response({"error":"Email and password are required"}, 400)

        user = User.query.filter(User.email == email).first()

        if user and user.check_password(password):
            login_user(user)
            return make_response({"message": "Logged in successfully"}, 200)
        else:
            return make_response({"error":"Invalid email or password"}, 401)

    except Exception as e:
        db.session.rollback()
        return make_response({"error":"Internal Server Error: " + str(e)}, 500)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return make_response({"message":"Logged out successfully"}, 200)


class Blogs(Resource):
        def get(self):
            try:
                blogs = []

                for blog in Blog.query.all():
                    blogs.append(blog.to_dict(rules=['-user', '-comments']))

                return make_response({"blogs": blogs}, 200)
            except Exception as e:
                return make_response({"error": str(e)}, 400)

        @login_required
        def post(self):
            try:
                data = request.get_json()
                if not data:
                    return make_response({"error": "No input data provided"}, 400)

                title = data.get('title')
                content = data.get('content')
                user_id = data.get('user_id')

                if not title or not content or not user_id:
                    return make_response({"error": "Title, content, and user_id are required"}, 400)

                new_blog = Blog(title=title, content=content, user_id=user_id)
                db.session.add(new_blog)
                db.session.commit()
                return make_response({"message": "Blog created successfully"}, 201)
            except Exception as e:
                db.session.rollback()
                return make_response({"error": str(e)}, 400)


api.add_resource(Blogs, "/blogs")

# @app.route('/blogs', methods=['GET', 'POST'])
# def blogs():
#     try:
#         if request.method == 'GET':
#             try:
#                 blogs = []
#
#                 for blog in Blog.query.all():
#                     blogs.append(blog.to_dict(rules=['-user', '-comments']))
#
#                 return make_response({"blogs": blogs}, 200)
#             except Exception as e:
#                 return make_response({"error":str(e)}, 400)
#         elif request.method == 'POST':
#             try:
#                 data = request.get_json()
#                 if not data:
#                     return make_response({"error":"No input data provided"}, 400)
#
#                 title = data.get('title')
#                 content = data.get('content')
#                 user_id = data.get('user_id')
#
#                 if not title or not content or not user_id:
#                     return make_response({"error":"Title, content, and user_id are required"}, 400)
#
#                 new_blog = Blog(title=title, content=content, user_id=user_id)
#                 db.session.add(new_blog)
#                 db.session.commit()
#                 return make_response({"message":"Blog created successfully"}, 201)
#             except Exception as e:
#                 db.session.rollback()
#                 return make_response({"error": str(e)},400)
#     except Exception as e:
#         return make_response({'error':'Internal Server Error: ' + str(e)}, 500)


@app.route('/blogs/<int:id>', methods=['GET', 'DELETE', 'PATCH'])
@login_required
def blog_by_id(id):
    try:
        blog = Blog.query.filter(Blog.id==id).first()
        if not blog:
            return make_response({"error":"Blog not found"}, 404)

        if request.method == 'GET':
            try:
                blog_dict = blog.to_dict(rules=['-user', '-comments'])
                return make_response({"blog":blog_dict}, 200)
            except Exception as e:
                return make_response({"error":str(e)}, 400)
        elif request.method == 'PATCH':
            try:
                data = request.get_json()
                if not data:
                    return make_response({"error":"No input data provided"}, 400)

                title = data.get('title')
                content = data.get('content')

                if title is not None:
                    blog.title = title
                if content is not None:
                    blog.content = content

                # for attr, value in data.items():
                #     if attr in ['title', 'content']:
                #         continue  # Skip attributes that should not be updated
                #     setattr(blog, attr, value)
                db.session.commit()
                return make_response({"message":"Blog updated successfully"}, 200)
            except Exception as e:
                db.session.rollback()
                return make_response({"error":"Failed to update blog: " + str(e)}, 400)
        elif request.method == 'DELETE':
            try:
                db.session.delete(blog)
                db.session.commit()
                return make_response({"message":"Blog deleted successfully"}, 200)
            except Exception as e:
                db.session.rollback()
                return make_response({"error":str(e)}, 400)

    except Exception as e:
        return make_response({"error": "Internal Server Error: " + str(e)}, 500)


@app.route('/users', methods=['GET', 'POST'])
@login_required
def users():
    try:
        if request.method == 'GET':
            try:
                users = []
                for user in User.query.all():
                    users.append(user.to_dict(rules=['-blogs', '-comments', '-password_hash']))
                return make_response({"users":users}, 200)
            except Exception as e:
                db.session.rollback()
                return make_response({"error":str(e)})
        elif request.method == 'POST':
            try:
                data = request.get_json()
                if not data:
                    return make_response({"error": "No input data provided"}, 400)

                username = data.get('username')
                email = data.get('email')
                password = data.get('password')

                if not username or not email or not password:
                    return make_response({"error": "Username, email, and password are required"}, 400)

                hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
                new_user = User(username=username, email=email, password_hash=hashed_password)
                db.session.add(new_user)
                db.session.commit()

                return make_response({"message":"User created successfully"}, 201)
            except Exception as e:
                db.session.rollback()
                return make_response({"error":str(e)})
    except Exception as e:
        return  make_response({"error":"Internal Server Error: " + str(e)}, 500)


@app.route('/users/<int:id>', methods=['GET', 'PATCH', 'DELETE'])
@login_required
def user_by_id(id):
    try:
        user = User.query.filter(User.id==id).first()
        if not user:
            return make_response({"error":"User not found"}, 404)

        if request.method == 'GET':
            try:
                user_dict = user.to_dict(rules=['-blogs', '-comments', '-password_hash'])
                return make_response({"user":user_dict}, 200)
            except Exception as e:
                return make_response({"error":str(e)}, 400)
        elif request.method == 'PATCH':
            try:
                data = request.get_json()
                if not data:
                    return make_response({"error":"No input data provided"}, 400)

                username = data.get('username')
                email = data.get('email')
                password = data.get('password')

                if username is not None:
                    user.username = username

                if email is not None:
                    user.email = email

                if password is not None:
                    user.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

                db.session.commit()
                return make_response({"message":"User updated successfully"}, 200)
            except Exception as e:
                db.session.rollback()
                return make_response({"error":"Failed to update user: " + str(e)}, 400)
        elif request.method == 'DELETE':
            try:
                db.session.delete(user)
                db.session.commit()
                return make_response({"message":"USer successfully deleted"}, 200)
            except Exception as e:
                db.session.rollback()
                return make_response({"error":"Failed to delete user: " + str(e)}, 400)
    except Exception as e:
        return make_response({"error":"Internal Server Error: " + str(e)}, 500)


@app.route('/comments', methods=['GET', 'POST'])
@login_required
def comments():
    try:
        if request.method == 'GET':
            try:
                comments = []

                for comment in Comment.query.all():
                    comments.append(comment.to_dict(rules=['user','blog']))
                return make_response({"comments":comments}, 200)
            except Exception as e:
                return make_response({"error":str(e)}, 400)
        elif request.method == 'POST':
            try:
                data = request.get_json()
                if not data:
                    return make_response({"error":"No data input provided"}, 400)

                content = data.get('content')
                user_id = data.get('user_id')
                blog_id = data.get('blog_id')

                if not content or not user_id or not blog_id:
                    return make_response({"error":"Content, user_id, and blog_id must be provided"}, 400)

                new_comment = Comment(content=content, user_id=user_id, blog_id=blog_id)
                db.session.add(new_comment)
                db.session.commit()
                return make_response({"message":"Comment posted successfuly"}, 201)

            except Exception as e:
                db.session.rollback()
                return make_response({"error":str(e)}, 400)
    except Exception as e:
        return make_response({"error":"Internal Server Error: " + str(e)}, 500)


@app.route('/comments/<int:id>', methods=['GET', 'PATCH', 'DELETE'])
@login_required
def comment_by_id(id):
    try:
        comment = Comment.query.filter(Comment.id==id).first()

        if not comment:
            return make_response({"error": "Comment not found"}, 404)

        if request.method == 'GET':
            try:
                comment_dict = comment.to_dict(rules=['user', 'blog'])
                return make_response({"comment":comment_dict}, 200)
            except Exception as e:
                return make_response({"error":str(e)}, 400)
        elif request.method == 'PATCH':
            try:
                data = request.get_json()

                if not data:
                    return make_response({"error":"No input data provided"}, 400)

                content = data.get('content')
                if content is not None:
                    comment.content = content

                db.session.commit()
                return make_response({"message": "Comment updated successfully"}, 200)
            except Exception as e:
                db.session.rollback()
                return make_response({"error": "Failed to update comment: " + str(e)}, 400)
        elif request.method == 'DELETE':
            try:
                db.session.delete(comment)
                db.session.commit()

                return make_response({"message":"Comment deleted succssfully"}, 200)
            except Exception as e:
                db.session.rollback()
                return make_response({"error":"Failed to delete comment: " + str(e)}, 400)

    except Exception as e:
        return make_response({"error":"Internal Server Error: " + str(e)}, 500)



if __name__ == '__main__':
    app.run(debug=True)
