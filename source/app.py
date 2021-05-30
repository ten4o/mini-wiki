from gevent import monkey; monkey.patch_all()

from bottle import get, route, run, static_file, template
import os

WWW_ROOT = os.getenv('WWW_ROOT') or os.path.dirname(__file__)

# Static Routes
@get('/static/css/<filepath:re:.*\.css>')
def css(filepath):
    return static_file(filepath, root=f'{WWW_ROOT}/css')

@get('/static/font/<filepath:re:.*\.(eot|otf|svg|ttf|woff|woff2?)>')
def font(filepath):
    return static_file(filepath, root=f'{WWW_ROOT}/font')

@get('/static/img/<filepath:re:.*\.(jpg|png|gif|ico|svg)>')
def img(filepath):
    return static_file(filepath, root=f'{WWW_ROOT}/img')

@get('/static/js/<filepath:re:.*\.js>')
def js(filepath):
    return static_file(filepath, root=f'{WWW_ROOT}/js')

@get("/")
@get("/index")
@get("/index.htm")
@get("/index.html")
def index():
    return static_file('index.html', root=WWW_ROOT)

if __name__ == '__main__':
    print(WWW_ROOT)
    run(host='0.0.0.0', port=8081)
