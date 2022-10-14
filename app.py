from flask import Flask, request
import sqlite3


app = Flask(__name__)

# Create Article
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
        article= [dict((cur.description[i][0], value) \
               for i, value in enumerate(row)) for row in cur.fetchall()]

        # Close connection
        connection.close()
        
        result = dict()
        if len(article) == 0:
            return "ERROR: Article posting failure"
        elif len(article) == 1:
            result["article"] = article[0]
        else:
            result["articles"] = article

        return result
if __name__ == '__main__':
    app.run(debug=True) # debug=True: I don't have to restart server.

