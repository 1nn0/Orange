from flask_wtf import Form
from wtforms import StringField, TextAreaField, SelectField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, Length


class SearchForm(Form):
    search = StringField('search', validators=[DataRequired()])


# category = SelectField(u'Фильтр', choices=[('name', 'Фамилия'), ('fname', 'Имя'), ('dolzh', 'Должность')])

class CreateForm(Form):
    client = StringField('Клиент', validators=[DataRequired()])
    origin = StringField('Откуда', validators=[DataRequired()])
    destination = StringField('Куда', validators=[DataRequired()])
    capacity = StringField('Грузоподъемность', validators=[DataRequired()])
    type = SelectField('Тип ТС',
                       choices=[('БОРТ', 'Борт'), ('ТЕНТ', 'Тент'), ('КОНТ', 'Контейнер'), ('ФУРГ', 'Фургон'),
                                ('ЦЕЛН', 'Цельнометалл.'), ('РЕФР', 'Рефрижератор'), ('ПЛЩД', 'Площадка'),
                                ('ШАЛА', 'Шаланда'), ('ТРАЛ', 'Трал'),
                                ('ВЫШК', 'Автовышка'), ('КПЛЩ', 'Контейнерная площадка'), ('КРАН', 'Кран'),
                                ('ЛЕСВ', 'Лесовоз'), ('ВЗДХ', 'Вездеход'),
                                ('ТРУБ', 'Трубовоз'), ('МАНП', 'Манипулятор'), ('МЕГА', 'Мега'),
                                ('ПОГР', 'Погрузчик'),
                                ('ТАКЛ', 'Такелаж')])
    comments = TextAreaField('Примечания', validators=[DataRequired()])


class EditForm(CreateForm):
    rate = StringField('Ставка')
    terms = TextAreaField('Код АТИ и т.д.', validators=[DataRequired()])
    manager = StringField('Логист', validators=[DataRequired()])
    comments = TextAreaField('Примечания', validators=[DataRequired()])


class CreateUserForm(Form):
    first_name = StringField('Имя')
    last_name = StringField('Фамилия')
    email = StringField('Логин (email)', validators=[DataRequired(), Email(message='Некорректный E-mail')])
    password = PasswordField('Пароль', validators=[DataRequired(), Length(8, 20, 'От 8 до 20 символов')])
    role = SelectField('Роль')


class EditUserForm(CreateUserForm):
    active = BooleanField('Активен?')
    password = PasswordField('Пароль')
