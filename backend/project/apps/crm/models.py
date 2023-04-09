from django.db.models import DO_NOTHING, ForeignKey, Model, CharField, DateTimeField, DateField, BooleanField

from ..authorization.models import User


class AllTime(Model):
    time = CharField(verbose_name='Рабочее время', max_length=20, db_index=True)

    def __str__(self):
        return self.time


class Clients(Model):
    PAID = 'paid'
    NOTPAID = 'notpaid'
    PAUSE = 'pause'
    FIRST = 'first'
    PART = 'part'
    ONE_PAID = 'one_paid'
    THIS_MONTH = 'this_month'
    NEW_CLIENT = 'new_client'
    PAID_STATUS = (
        (PAID, 'Оплачен'),
        (NOTPAID, 'Не оплачен'),
        (PAUSE, 'Пауза'),
        (FIRST, 'Первая тренировка'),
        (PART, 'Частичная оплата'),
        (ONE_PAID, 'Поразово'),
        (THIS_MONTH, 'Долг свыше месяца'),
        (NEW_CLIENT, 'Новый клиент')
    )

    NEW = 'new'
    RECORDED = 'recorded'
    REFUSAL = 'refusal'
    CLIENT_STATUS = (
        (NEW, 'Новый клиент'),
        (REFUSAL, 'Отказ'),
        (RECORDED, 'Записан'),
    )

    NOT_CHECK = 'not_check'
    CHECKED_UPLOAD = 'checked_upload'
    CHECKED_CLOSED = 'checked_closed'
    CRM_STATUS = (
        (NOT_CHECK, 'Не проверен'),
        (CHECKED_UPLOAD, 'Проверен, записан'),
        (CHECKED_CLOSED, 'Проверен, отказ'),
    )

    NOT_CHECKED = 'not_checked'
    RECORDED = 'recorded'
    NOT_RECORDED = 'not_recorded'
    COACH_STATUS = (
        (RECORDED, 'Записан'),
        (NOT_CHECKED, 'Не проверен'),
        (NOT_RECORDED, 'Отказ'),
    )

    status = CharField(verbose_name='Статус клиента', choices=CLIENT_STATUS, default=NEW, max_length=255)
    status_operator = CharField(verbose_name='Статус оператора', choices=CRM_STATUS, default=NOT_CHECK,
                                max_length=255)
    status_coach = CharField(verbose_name='Статус проверки тренера', choices=COACH_STATUS, default=NOT_CHECKED,
                             max_length=255)
    payed_status = CharField(choices=PAID_STATUS, default=NOTPAID, verbose_name='Статус оплаты', max_length=255)
    name = CharField(verbose_name='Имя', max_length=100, blank=True, null=True)
    lastname = CharField(verbose_name='Фамилия', max_length=100, blank=True, null=True)
    phone_number = CharField(verbose_name='Номер телефона', max_length=100, unique=True)
    date_added = DateTimeField(auto_now_add=True, verbose_name='Дата добавления клиента')
    date_update = DateTimeField(auto_now=True, verbose_name='Дата обновления данных')
    payed_date = DateField(verbose_name='Дата оплаты', blank=True, null=True)


class ClassAttendance(Model):
    visit = BooleanField(default=False)
    client = ForeignKey(Clients, on_delete=DO_NOTHING)
    date = DateField(auto_now_add=True)


class Location(Model):
    location = CharField(verbose_name='Место тренировки', max_length=255)
    key = CharField(verbose_name='Значение', max_length=255)


class Age(Model):
    age = CharField(verbose_name='Возрастная группа', max_length=255)
    key = CharField(verbose_name='Значение', max_length=255)


class Section(Model):
    section = CharField(verbose_name='Тип секции', max_length=255)
    key = CharField(verbose_name='Значение', max_length=255)


class GroupType(Model):
    class_type = CharField(verbose_name='Название группы', max_length=255)
    key = CharField(max_length=255)


class Days(Model):
    day = CharField(verbose_name='День', max_length=255)
    key = CharField(verbose_name='Значение', max_length=255)


class FormClient(Model):
    location = CharField(verbose_name='Локации которые были выбраны', max_length=1000, blank=True, null=True)
    visit_time = CharField(verbose_name='Время которое было выбрано', max_length=1000, blank=True, null=True)
    section = CharField(verbose_name='Секции которое были выбраны', max_length=1000, blank=True, null=True)
    client = ForeignKey(Clients, on_delete=DO_NOTHING)
    age = CharField(verbose_name='Возрастная категория', max_length=100)
    visit_day = CharField(verbose_name='Дни которое было выбрано', max_length=1000)
    class_type = CharField(verbose_name='Тип занятий', max_length=100)


class OtherData(Model):
    client = ForeignKey(Clients, on_delete=DO_NOTHING)
    location = CharField(verbose_name='Локации которые были выбраны', max_length=1000, blank=True, null=True)
    section = CharField(verbose_name='Секции которое были выбраны', max_length=1000, blank=True, null=True)


class CoachForClient(Model):
    coach = ForeignKey(User, verbose_name='Тренер', on_delete=DO_NOTHING)
    visit_time = CharField(verbose_name='Время посещения тренировки с тренером', max_length=255)
    group_type = CharField(verbose_name='Тип тренировки', max_length=255)
    client = ForeignKey(Clients, verbose_name='Клиент', on_delete=DO_NOTHING)


class NewClientCoach(Model):
    coach = ForeignKey(User, verbose_name='Тренер', on_delete=DO_NOTHING)
    client = ForeignKey(Clients, verbose_name='Клиент', on_delete=DO_NOTHING)
