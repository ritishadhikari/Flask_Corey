import secrets
import os
from PIL import Image
from flask_mail import Message
from flask import url_for, current_app
from flask_blog import mail

def save_picture(form_picture):
    random_hex=secrets.token_hex(8)
    f_name,f_ext=os.path.splitext(form_picture.filename)
    picture_fn=random_hex+f_ext
    picture_path=os.path.join(current_app.root_path,'static','profile_pics',picture_fn)
    #reducing the image size and standardizing it
    output_size=(128,128)
    image=Image.open(form_picture)
    image.thumbnail(output_size)
    image.save(picture_path)
    return picture_fn

#pip install flask-mail
def send_reset_email(user):
    token=user.get_reset_token()
    msg=Message(subject='Password Reset Request',
                sender='noreply@demo.com', recipients=[user.email])
    msg.body=f'''To Reset your password visit the following link
{url_for('users.reset_token',token=token,_external=True)}

If you did not make this request, then ignore.
No changes will be made.

    '''
    mail.send(message=msg)
