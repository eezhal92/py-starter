import os
from flask import Flask, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename

import src.lib.db
from src.lib.db import (
    insert_new_book,
    seed_book,
    truncate_book,
    update_book,
    find_all_book,
    remove_book_by_id
)

# truncate_book()
# seed_book()

relative_path = '/static/upload/img'
upload_dir = os.path.abspath('.' + relative_path)

def create_app():
    app = Flask(
        __name__,
        static_folder='../../static',
        template_folder='../templates'
    )

    app.config['UPLOAD_FOLDER'] = upload_dir

    @app.route("/")
    def hello():
        result = find_all_book()
        print(result)
        return render_template("index.html", books=result)

    @app.route("/add-book", methods = ["GET"])
    def add_book():
        return render_template("add-book.html")

    @app.route("/create-book", methods = ["POST"])
    def create_book():
        print("-----")

        if  'file' not in request.files:
            return redirect('/')

        file = request.files['file']

        if file.filename == '':
            return redirect('/')

        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        file_relative_path = relative_path + '/' + filename

        data = {
            "title": request.form['title'],
            "author": request.form['author'],
            "img_path": file_relative_path
        }

        insert_new_book(data)

        return redirect('/')

    @app.route("/update-book/<id>", methods = ["POST"])
    def edit_book(id):
        print("-----")

        if  'file' not in request.files:
            return redirect('/')

        file = request.files['file']

        if file.filename == '':
            return redirect('/')

        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        file_relative_path = relative_path + '/' + filename

        data = {
            "id": id,
            "title": request.form['title'],
            "author": request.form['author'],
            "img_path": file_relative_path
        }

        update_book(data)

        return redirect('/')

    @app.route("/delete-book/<id>", methods=["POST"])
    def remove_book(id):
        remove_book_by_id(id)

        return redirect('/')

    @app.route("/ping")
    def ping():
        env = app.config['ENV']
        debug = app.config['DEBUG']

        return render_template("ping.html", env=env, debug=debug)

    return app
