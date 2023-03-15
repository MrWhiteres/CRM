# Generated by Django 4.1.7 on 2023-03-26 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0003_alter_clients_payed_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clients',
            name='payed_date',
            field=models.DateField(choices=[('paid', 'Оплачен'), ('notpaid', 'Не оплачен'), ('pause', 'Пауза')], default='notpaid', verbose_name='Дата оплаты'),
        ),
    ]