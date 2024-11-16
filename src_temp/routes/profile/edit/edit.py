from flask import render_template, redirect

from src.routes import routes_bp
from src.data import session
from src.data.models import User
from src.forms import SearchForm, EditProfileForm
from src.data.models.validators import ModelNotFound, UserUnauthorized, \
    UserToUser

TITLE = 'Редактирование профиля пользователя {user_nickname}'


@routes_bp.route('/profile/<login>/edit', methods=['GET', 'POST'])
def edit(login):
    user = User.find(session, login)
    User.validate(UserUnauthorized(), ModelNotFound(user), UserToUser(user))

    form = EditProfileForm()
    # Значения, которые нужно игнорировать при проверке уникальным валидатором
    form.add_unique_except_values(nickname=[user.nickname], email=[user.email])

    if form.validate_on_submit():
        User.edit(session, form, user)

        # Сохранение фото профиля
        user.save_avatar_image(form.avatar_image.data)

        # Успешное окончание редактирования, пересылаем пользователя
        # на его профиль
        return redirect(f'/profile/{user.nickname}')

    return render_template(
        'profile/edit/edit.html', search_form=SearchForm(),
        title=TITLE.format(user_nickname=user.nickname),
        user=user, form=form)
