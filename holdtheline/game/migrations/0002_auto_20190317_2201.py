# Generated by Django 2.1.7 on 2019-03-17 22:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='hand',
            name='game',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='game.Game'),
        ),
        migrations.AlterField(
            model_name='deck',
            name='game',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='game.Game'),
        ),
    ]
