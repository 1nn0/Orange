from flask.ext.wtf import Form
from wtforms import StringField, TextAreaField, SelectField
from wtforms.validators import DataRequired


class SearchForm(Form):
    search = StringField('search', validators=[DataRequired()])


# category = SelectField(u'Фильтр', choices=[('name', 'Фамилия'), ('fname', 'Имя'), ('dolzh', 'Должность')])

class CreateForm(Form):
    client = StringField('Клиент', validators=[DataRequired()])
    origin = StringField('Откуда', validators=[DataRequired()])
    destination = StringField('Куда', validators=[DataRequired()])
    capacity = StringField('Грузоподъемность', validators=[DataRequired()])
    type = SelectField('Тип ТС',
                       choices=[('Борт', 'Борт'), ('Тент', 'Тент'), ('Конт.', 'Контейнер'), ('Фургон', 'Фургон'),
                                ('Ц-М-Т.', 'Цельнометалл.'), ('Реф.', 'Рефрижератор'), ('Площ.', 'Площадка'),
                                ('Шал.', 'Шаланда'), ('Трал', 'Трал'),
                                ('Автовышка', 'Автовышка'), ('К.площ.', 'Контейнерная площадка'), ('Кран', 'Кран'),
                                ('Лесовоз', 'Лесовоз'),
                                ('Трубовоз', 'Трубовоз'), ('Манипулятор', 'Манипулятор'), ('Мега', 'Мега'),
                                ('Погрузчик', 'Погрузчик'),
                                ('Такелаж', 'Такелаж')])
    comments = TextAreaField('Примечания', validators=[DataRequired()])


class EditForm(CreateForm):
    rate = StringField('Ставка')
    terms = TextAreaField('Код АТИ и т.д.', validators=[DataRequired()])
    manager = StringField('Логист', validators=[DataRequired()])
    comments = TextAreaField('Примечания', validators=[DataRequired()])
