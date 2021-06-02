from gevent import monkey; monkey.patch_all()

import markdown
import os
import re
import db
from bottle import get, post, request, run, static_file, template, TEMPLATE_PATH

WWW_ROOT = os.getenv('WWW_ROOT') or os.path.dirname(__file__)

# make sure the template engine can find our views
TEMPLATE_PATH.append(f'{WWW_ROOT}/views')

# list of tag delimiters: | , ; - or white space
TAG_DELIMITER_RE = re.compile(r'[|,;\-\s]')

g_db = db.DB()

#
# Static Routes
#
@get('/static/<filepath:re:.*\.(htm|html)>')
def html(filepath):
    return static_file(filepath, root=f'{WWW_ROOT}/static')


@get('/static/css/<filepath:re:.*\.css>')
def css(filepath):
    return static_file(filepath, root=f'{WWW_ROOT}/static/css')


@get('/static/font/<filepath:re:.*\.(eot|otf|svg|ttf|woff|woff2?)>')
def font(filepath):
    return static_file(filepath, root=f'{WWW_ROOT}/static/font')


@get('/static/img/<filepath:re:.*\.(jpg|png|gif|ico|svg)>')
def img(filepath):
    return static_file(filepath, root=f'{WWW_ROOT}/static/img')


@get('/static/js/<filepath:re:.*\.js>')
def js(filepath):
    return static_file(filepath, root=f'{WWW_ROOT}/static/js')


@get('/')
@get('/index')
@get('/index.htm')
@get('/index.html')
def index():
    return static_file('index.html', root=WWW_ROOT)


@get('/new')
def get_new_article_page():
    return template('new_article', err_msg=None, body='')


@post('/new')
def insert_article():
    title = request.POST.get('title', '').strip()
    body = request.POST.get('body', '').strip()
    tag_str = request.POST.get('tag_list', '').strip()
    err_msg = None

    if tag_str:
        tag_list = [tag.lower() for tag in TAG_DELIMITER_RE.split(tag_str) if tag]
    else:
        tag_list = []

    if title and body:
        try:
            # TODO sanitize body to prevent XSS
            html_body = markdown.markdown(body)
            article_id = g_db.insert_article(title, html_body, tag_list)
        except ValueError as ve:
            err_msg = ve.args[0]
        except db.DuplicateTitleException:
            err_msg = 'Article with the same title already exists'
    else:
        if not title:
            err_msg = 'title cannot be empty'
        else:
            err_msg = 'body cannot be empty'

    if err_msg:
        return template('new_article', err_msg=err_msg, body=body, tag_list=tag_list)
    return template('inserted_article', title=title, article_id=article_id)


@get('/view/<article_id:int>')
def view_article(article_id):
    article = g_db.get_article_by_id(article_id)
    if article is None:
        title = f'Article with id {article_id} was not found.'
        body = ''
        tag_list = []
    else:
        title = article.title
        body = article.body
        tag_list = sorted([tag.name for tag in article.tags])
    return template('view_article', title=title, body=body, tag_list=tag_list)


@get('/search')
def search_articles():
    title = request.GET.get('title', '').strip()
    body = request.GET.get('body', '').strip()
    tag_list_str = request.GET.get('tags', '').strip()
    if tag_list_str:
        tag_list = [tag.lower() for tag in TAG_DELIMITER_RE.split(tag_list_str) if tag]
    else:
        tag_list = []
    article_list = g_db.get_article_list(title, body, tag_list)
    return template('article_list', article_list=article_list)


if __name__ == '__main__':
    print(WWW_ROOT)
    run(host='0.0.0.0', port=8081)
