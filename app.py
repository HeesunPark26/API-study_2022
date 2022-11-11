from flask import Flask, request, jsonify
import sqlite3


app = Flask(__name__)

# Create Article
@app.route('/articles', methods=['GET', 'POST'])
def add_article():
    if request.method == 'POST':

        params = request.get_json()["article"]
        title = params["title"]
        description = params["description"]
        body = params["body"]

        if "tagList" in params.keys(): 
            tagList = ",".join(params["tagList"])
        else:
            tagList = None

        # make slug with title
        from slugify import slugify
        slug = slugify(title)
        
        # tmp
        author_id = 1

        # Create Cursor
        connection = sqlite3.connect('database.db')
        cur = connection.cursor()

        # Execute
        try:
            if tagList is not None:
                cur.execute((
                    "INSERT INTO post "
                    "(slug, title, description, body, tagList, favorited, favoritesCount, author_id) "
                    f"VALUES ('{slug}', '{title}', '{description}', '{body}', '{tagList}', 'False', 0, {author_id})"))
            else:
                cur.execute((
                    "INSERT INTO post "
                    "(slug, title, description, body, favorited, favoritesCount, author_id) "
                    f"VALUES ('{slug}', '{title}', '{description}', '{body}', 'False', 0, {author_id})"))
        except:
            return "Title already exists. Try different title"    

        # Commit to DB
        connection.commit()

        # give response
        cur.execute(f"SELECT * FROM post WHERE slug is '{slug}'")

        article = [dict((cur.description[i][0], value) \
                    for i, value in enumerate(row)) for row in cur.fetchall()]
        
        # Close connection
        connection.close()

        if len(article) == 0:
            return "ERROR: Article posting failure"

        elif len(article) == 1:
            article = article[0]
            if article["tagList"] is not None:
                article["tagList"] = article["tagList"].split(",")
            return jsonify(article = article)
    elif request.method == 'GET':
        param_dict = request.args.to_dict()
        # no parameter -> default
        if len(param_dict) == 0:
            connection = sqlite3.connect('database.db')
            cur = connection.cursor()

            cur.execute(("SELECT * FROM post ORDER BY createdAT DESC LIMIT 20"))
            articles = [dict((cur.description[i][0], value) \
                    for i, value in enumerate(row)) for row in cur.fetchall()]
            connection.close()
            return jsonify(articles = articles)
        else:            
            connection = sqlite3.connect('database.db')
            cur = connection.cursor()

            query_tag = None
            query_author = None
            query_limit = ''

            if param_dict["tag"] is not None:
                tag = param_dict["tag"]
                query_tag = f"tagList LIKE '%{tag}%'"
            if param_dict["author"] is not None:
                author = param_dict["author"]
                query_author = (
                    f"author_id IN (SELECT id from user WHERE username is '{author}')")
            if param_dict["limit"] is not None:
                limit = param_dict["limit"]
                query_limit = f"LIMIT {limit}"

            if query_author is not None:
                if query_tag is not None:
                    query_where = f"WHERE ({query_tag}) AND ({query_author})"
                else:
                    query_where = f"WHERE ({query_author})"
            else:
                if query_tag is not None:
                    query_where = f"WHERE ({query_tag})"
                else:
                    query_where = ''
            
            cur.execute(f"SELECT * FROM post {query_where} ORDER BY createdAT DESC {query_limit};")
            articles = [dict((cur.description[i][0], value) \
                    for i, value in enumerate(row)) for row in cur.fetchall()]
            connection.close()

            return jsonify(articles = articles)
@app.route('/articles/feed', methods = ['GET'])
def feed_article():
    param_dict = request.args.to_dict()
    if len(param_dict) == 0:
        connection = sqlite3.connect('database.db')
        cur = connection.cursor()

        cur.execute(("SELECT * FROM post ORDER BY createdAT DESC LIMIT 20"))
        articles = [dict((cur.description[i][0], value) \
            for i, value in enumerate(row)) for row in cur.fetchall()]
        connection.close()
        return articles
    else:
        limit = param_dict["limit"]
        connection = sqlite3.connect('database.db')
        cur = connection.cursor()

        cur.execute((f"SELECT * FROM post ORDER BY createdAT DESC LIMIT {limit}"))
        articles = [dict((cur.description[i][0], value) \
            for i, value in enumerate(row)) for row in cur.fetchall()]
        connection.close()
        return jsonify(articles = articles)


@app.route('/articles/<string:slug>', methods = ['GET', 'PUT', 'DELETE'])
def article(slug):
    if request.method == 'GET':
        if slug != 'feed':
            # Create Cursor
            connection = sqlite3.connect('database.db')
            cur = connection.cursor()

            # execute 
            cur.execute(f"SELECT * FROM post WHERE slug is '{slug}'")

            # get article
            article = [dict((cur.description[i][0], value) \
                            for i, value in enumerate(row)) for row in cur.fetchall()]
            
            # close connection
            connection.close()

            if len(article) == 0:
                return "No article"
            elif len(article) == 1:
                article = article[0]
                if article["tagList"] is not None:
                    article["tagList"] = article["tagList"].split(",")
                return jsonify(article = article)

    elif request.method == 'PUT':
        params = request.get_json()["article"]
        if "tagList" in params.keys(): 
            params["tagList"] = ", ".join(params["tagList"])

        # to make query including to-be-updated parameters
        query_set_l = [f"{p} = '{params[p]}'" for p in params.keys()]
        # e.g., query_set_l is ["title = 'how to train dog'"]

        # change slug if title is changed
        if params["title"] is not None:
            from slugify import slugify
            new_slug = slugify(params["title"])
            query_set_l.append(f"slug = '{new_slug}'")
        
        query_set = ", ".join(query_set_l)

        # Create Cursor
        connection = sqlite3.connect('database.db')
        cur = connection.cursor()

        # execute 
        cur.execute((
            "UPDATE post "
            f"SET {query_set} "
            f"WHERE slug is '{slug}'"))
        
        # Commit to DB
        connection.commit()

        # give response
        cur.execute(f"SELECT * FROM post WHERE slug is '{new_slug}'")

        # get article
        article = [dict((cur.description[i][0], value) \
                        for i, value in enumerate(row)) for row in cur.fetchall()]
        # close connection
        connection.close()

        article = article[0]
        if article["tagList"] is not None:
            article["tagList"] = article["tagList"].split(",")

        return jsonify(article = article)

    elif request.method == 'DELETE':
        # Create Cursor
        connection = sqlite3.connect('database.db')
        cur = connection.cursor()

        # execute 
        cur.execute(f"DELETE FROM post WHERE slug = '{slug}'")

        # Commit to DB
        connection.commit()

        # close connection
        connection.close()

        return "ARTICLE DELETED"

@app.route('/articles/<string:slug>/comments', methods = ['POST', 'GET'])
def comments(slug):
    if request.method == 'POST':
        params = request.get_json()["comment"]
        body = params['body']

        author_id = 1

        connection = sqlite3.connect('database.db')
        cur = connection.cursor()
        cur.execute((
            "INSERT INTO comment "
            "(article_id, body, author_id) "
            f"VALUES ('{slug}', '{body}', {author_id})"))

        comment_id = cur.lastrowid
        connection.commit()

        cur.execute(f"SELECT * FROM comment WHERE id is '{comment_id}'")
        comment = [dict((cur.description[i][0], value) \
            for i, value in enumerate(row)) for row in cur.fetchall()]
        connection.close()

        return jsonify(comment = comment)

    elif request.method == 'GET':
        connection = sqlite3.connect('database.db')
        cur = connection.cursor()
        cur.execute(f"SELECT * FROM comment WHERE article_id is '{slug}'")

        # get article
        comment = [dict((cur.description[i][0], value) \
                        for i, value in enumerate(row)) for row in cur.fetchall()]
        connection.close()

        if len(comment) == 0:
            return "NO COMMENT"
        elif len(comment) == 1:
            return jsonify(comment = comment)
        else: 
            return jsonify(comments = comment)

@app.route('/articles/<string:slug>/comments/<int:id>', methods = ['DELETE'])
def delete_comment(slug, id):
    # Create Cursor
    connection = sqlite3.connect('database.db')
    cur = connection.cursor()

    # execute 
    cur.execute(f"DELETE FROM comment WHERE article_id = '{slug}' AND id = {id}")
    connection.commit()
    connection.close()

    return "COMMENT DELETED"

@app.route('/articles/<string:slug>/favorite', methods = ['POST', 'DELETE'])
def favorite(slug):
    if request.method == 'POST':
        connection = sqlite3.connect('database.db')
        cur = connection.cursor()

        # execute 
        cur.execute((
            "UPDATE post "
            f"SET favoritesCount = favoritesCount + 1, "
            "favorited = CASE WHEN favorited = 'False' THEN 'True' ELSE 'True' END "
            f"WHERE slug is '{slug}'"))
        connection.commit()
        cur.execute(f"SELECT * FROM post WHERE slug is '{slug}'")
        article = [dict((cur.description[i][0], value) \
                        for i, value in enumerate(row)) for row in cur.fetchall()]
        connection.close()

        
        article = article[0]
        if article["tagList"] is not None:
            article["tagList"] = article["tagList"].split(",")

        return jsonify(article = article)

    if request.method == 'DELETE':
        connection = sqlite3.connect('database.db')
        cur = connection.cursor()

        # execute 
        cur.execute((
            "UPDATE post "
            f"SET favoritesCount = CASE WHEN favoritesCount = 0 THEN 0 ELSE favoritesCount -1 END "
            f"WHERE slug is '{slug}'"))
        connection.commit()

        cur.execute((
            "UPDATE post "
            "SET favorited = CASE WHEN favoritesCount = 0 THEN 'False' ELSE 'True' END "
            f"WHERE slug is '{slug}'"))
        connection.commit()

        cur.execute(f"SELECT * FROM post WHERE slug is '{slug}'")
        article = [dict((cur.description[i][0], value) \
                        for i, value in enumerate(row)) for row in cur.fetchall()]
        connection.close()

        
        article = article[0]
        if article["tagList"] is not None:
            article["tagList"] = article["tagList"].split(",")

        return jsonify(article = article)

@app.route('/tags', methods = ['GET'])
def tags():
    connection = sqlite3.connect('database.db')
    cur = connection.cursor()

    # execute 
    cur.execute(
        "SELECT tagList FROM post") 
    connection.commit()

    tags = cur.fetchall()
    tags_all = []
    for t in tags:
        tags_all += t[0].split(',')
    tags_all = list(set(tags_all))

    return jsonify(tags = tags_all)

if __name__ == '__main__':
    app.run(debug=True) # debug=True: I don't have to restart server.

