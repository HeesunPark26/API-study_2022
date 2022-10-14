from flask import Flask, render_template, request, redirect, url_for, flash
from data import Articles
import sqlite3
from wtforms import Form, StringField, TextAreaField, PasswordField, validators


app = Flask(__name__)

# Articles = Articles()

@app.route("/")
def index():
    return render_template('home.html')

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/articles")
def articles():
    # Create cursor
    connection = sqlite3.connect('database.db')
    cur = connection.cursor()

    # Get articles
    cur.execute("SELECT * FROM post")

    articles = cur.fetchall()

    if len(articles) > 0:
        return render_template('articles.html', articles=articles)
    else:
        msg = 'No Articles Found'
        return render_template('articles.html', msg=msg)
    
    # Close connection
    connection.close()

@app.route("/article/<string:slug>/")
def article(slug):
    return render_template('article.html', slug=slug)

# Article Form Class
class ArticleForm(Form):
    title = StringField('Title', [validators.Length(min=1, max=200)])
    description = TextAreaField('Description', [validators.Length(min=1)])
    body = TextAreaField('Body', [validators.Length(min=30)])
    tagList = TextAreaField('Tags', [validators.Length(min=1)])

# Add Article
@app.route('/add_article', methods=['GET','POST'])
def add_article():
    form = ArticleForm(request.form)
    if request.method == 'POST' and form.validate():
        title = form.title.data
        description = form.description.data
        body = form.body.data
        tagList = form.tagList.data

        from slugify import slugify
        slug = slugify(title)
        #tmp
        author_id = 0


        # Create Curser
        connection = sqlite3.connect('database.db')
        cur = connection.cursor()

        # Execute
        cur.execute((
            "INSERT INTO post "
            "(slug, title, description, body, tagList, favorited, favoritesCount, author_id) "
            f"VALUES ('{slug}', '{title}', '{description}', '{body}', '{tagList}', 'False', 0, 0)"))
        
        # Commit to DB
        connection.commit()

        # Close connection
        connection.close()

        # flash('Article Created', 'success')

        return redirect(url_for('articles'))
    return render_template('add_article.html', form=form)


# Add Article
@app.route('/article_', methods=['GET','POST'])
def add_article_():
    if request.method == 'POST':
        # https://www.digitalocean.com/community/tutorials/processing-incoming-request-data-in-flask
        title = request.form.get('title')
        description = request.form.get('description')
        body = request.form.get('body')
        if request.form.get('tagList') is not None:
            tagList = request.form.get('tagList')
        else:
            tagList = " "

        from slugify import slugify
        slug = slugify(title)
        #tmp
        author_id = 1


        # Create Curser
        connection = sqlite3.connect('database.db')
        cur = connection.cursor()

        # Execute
        cur.execute((
            "INSERT INTO post "
            "(slug, title, description, body, tagList, favorited, favoritesCount, author_id) "
            f"VALUES ('{slug}', '{title}', '{description}', '{body}', '{tagList}', 'False', 0, {author_id})"))
        
        # Commit to DB
        connection.commit()

        # give response
        cur.execute(f"SELECT * FROM post WHERE title is '{title}'")

        # get output with json format
        articles = [dict((cur.description[i][0], value) \
               for i, value in enumerate(row)) for row in cur.fetchall()]
    
        # Close connection
        connection.close()
        
        return articles

if __name__ == '__main__':
    app.run(debug=True) # debug=True: I don't have to restart server.

