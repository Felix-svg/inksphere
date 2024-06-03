from config import db, app
from faker import Faker
from models import User
from models import Blog
from models import Comment

with app.app_context():
    db.create_all()

    print("Deleting all records")
    User.query.delete()
    Blog.query.delete()
    Comment.query.delete()

    fake = Faker()

    print("Creating users")
    user1 = User(username=fake.user_name(), email=fake.company_email())
    user1.set_password("1234")
    user2 = User(username=fake.user_name(), email=fake.company_email())
    user2.set_password("2345")
    user3 = User(username=fake.user_name(), email=fake.company_email())
    user3.set_password("3456")

    db.session.add_all([user1, user2, user3])
    db.session.commit()

    print("Creating blogs")
    blog1 = Blog(
        title="Getting Started with Python",
        content="Python is a versatile and powerful programming language that is easy to learn and fun to use. In this article, we will cover the basics of Python, including installation, syntax, and basic programming concepts.",
        user=user2,
    )
    blog2 = Blog(
        title="Mastering SQL: Tips and Tricks",
        content="SQL is the language of databases. Whether you're using MySQL, PostgreSQL, or SQLite, mastering SQL is essential for any developer working with data. In this article, we will explore some advanced SQL techniques that can help you become a SQL expert.",
        user=user1,
    )
    blog3 = Blog(
        title="JavaScript for Beginners: A Comprehensive Guide",
        content="JavaScript is the language of the web. From simple animations to complex web applications, JavaScript is a crucial skill for any web developer. This guide will take you through the fundamentals of JavaScript, including variables, functions, and event handling.",
        user=user3,
    )
    blog4 = Blog(
        title="Building RESTful APIs with Flask",
        content="Flask is a lightweight and flexible web framework for Python. In this tutorial, we will show you how to build a RESTful API with Flask, covering everything from setting up your development environment to deploying your API to production.",
        user=user1,
    )
    blog5 = Blog(
        title="Advanced Python Techniques",
        content="Python is known for its simplicity, but it also has a rich set of features for advanced programming. This article will delve into some advanced Python techniques, such as decorators, context managers, and metaclasses, to help you write more efficient and elegant code.",
        user=user2,
    )

    db.session.add_all([blog1, blog2, blog3, blog4, blog5])
    db.session.commit()

    print("Creating comments")
    comment1 = Comment(
        content="Great introduction to Python! I especially liked the section on basic programming concepts. Looking forward to more articles like this.",
        blog=blog1,
        user=user2,
    )
    comment2 = Comment(
        content="The tips on optimizing SQL queries were really helpful. I've already noticed a performance improvement in my database operations. Thanks for sharing!",
        blog=blog2,
        user=user1,
    )
    comment3 = Comment(
        content="This guide is perfect for beginners! The examples were easy to follow, and I learned a lot about JavaScript. Can't wait to try out more advanced topics.",
        blog=blog3,
        user=user3,
    )
    comment4 = Comment(
        content="I've been looking for a good tutorial on Flask APIs, and this one nailed it. Clear and concise, with practical examples. Keep up the great work!",
        blog=blog4,
        user=user2,
    )
    comment5 = Comment(
        content="This article really opened my eyes to the advanced features of Python. The section on decorators was particularly enlightening. Thanks for the detailed explanations!",
        blog=blog5,
        user=user1,
    )

    db.session.add_all([comment1, comment2, comment3, comment4, comment5])
    db.session.commit()

    print("Seeding complete")
