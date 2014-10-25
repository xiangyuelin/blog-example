# -*- coding: utf-8 -*-



"""
    def get_post(post_id):
        post = Post.query.filter_by(id=post_id).first()
        return post

    def delete_post(post_id):
        post = Post.query.filter_by(id=post_id).first()
        db.session.delete(post)
        db.session.commit()

    def add_post(title, author, content):
        post = Post(title=title, author=author, content=content)
        db.session.add(post)
        db.session.commit()

    def update_post(title, author, content, post_id):
        post = Post.query.filter_by(id=post_id).first()
        post['title'] = title
        post['author'] = author
        post['updated_at'] = datetime.utcnow
        db.session.commit()

    @classmethod
    def get_all_posts(cls):
        posts =  Post.query.all()
        return posts

    def get_posts_by_user(user_id):
        posts = Post.query.filter_by(user_id=user_id).all()
        return posts
"""

