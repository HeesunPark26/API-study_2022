from flask import Flask, request, jsonify
import sqlite3


app = Flask(__name__)

# Create Article
@app.route('/article_', methods=['GET','POST'])
def add_article_():
    if request.method == 'POST':
        ### get request body
        ## way 1. x-www-form-urlencoded
        # title = request.form.get('title')
        # description = request.form.get('description')
        # body = request.form.get('body')

        # if request.form.get('tagList') is not None:
        #     tagList = request.form.get('tagList')
        # else:
        #     tagList = " " # tmp

        ## way 2. raw (JSON)
        params = request.get_json()
        title = params["title"]
        description = params["description"]
        body = params["body"]

        if params["tagList"] is not None:
            tagList = params["tagList"]
        else:
            tagList = " "

        # make slug with title
        from slugify import slugify
        slug = slugify(params["title"])
        
        # tmp
        author_id = 1

        # Create Cursor
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

        ### convert output to json format
        ## way 1. use dictionary
        # article= [dict((cur.description[i][0], value) \
        #        for i, value in enumerate(row)) for row in cur.fetchall()]
        # result = dict()
        # if len(article) == 0:
        #     return "ERROR: Article posting failure"
        # elif len(article) == 1:
        #     result["article"] = article[0]
        # else:
        #     result["articles"] = article


        # way 2. use jsonify
        article = cur.fetchall()
        if len(article) == 0:
            return "ERROR: Article posting failure"

        elif len(article) == 1:
            result = jsonify(
                slug = article[0][0],
                title = article[0][1],
                description = article[0][2],
                body = article[0][3],
                tagList = article[0][4],
                createdAt = article[0][5],
                updatedAt = article[0][6],
                favorited = article[0][7],
                favoritesCount = article[0][8],
                author_id = article[0][9]
            )
        
        # Close connection
        connection.close()
        
     
        return result
        
if __name__ == '__main__':
    app.run(debug=True) # debug=True: I don't have to restart server.

