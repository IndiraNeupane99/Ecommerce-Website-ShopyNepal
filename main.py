# from website import create_app
# from website.models import *

# app = create_app()

# with app.app_context():
#     db.create_all()   # 🔥 THIS CREATES ALL TABLES
    

# if __name__ == '__main__':
#     app.run(debug=True, port=5001)


# from website import create_app


# app = create_app()


# if __name__ == '__main__':
#     app.run(debug=True, port=5001)



from website import create_app, db

app = create_app()

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True, port=5001)
    