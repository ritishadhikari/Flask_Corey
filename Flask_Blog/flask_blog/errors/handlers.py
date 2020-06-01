from flask import Blueprint, render_template

errors=Blueprint(name='errors', import_name=__name__)

@errors.app_errorhandler(404)
def error_404(error):

    #the default is 200 route, but since it is a error
    # we implicitly mention it as 404
    return render_template('errors/404.html'),404

@errors.app_errorhandler(403)
def error_403(error):

    #the default is 200 route, but since it is a error
    # we implicitly mention it as 403
    return render_template('errors/403.html'),403

@errors.app_errorhandler(500)
def error_500(error):

    #the default is 200 route, but since it is a error
    # we implicitly mention it as 404
    return render_template('errors/500.html'),500
