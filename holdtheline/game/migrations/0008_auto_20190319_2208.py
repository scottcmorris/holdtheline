# Generated by Django 2.1.7 on 2019-03-19 22:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0007_auto_20190319_2017'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hand',
            name='card_fk',
        ),
        migrations.RemoveField(
            model_name='hand',
            name='game_fk',
        ),
        migrations.RemoveField(
            model_name='hand',
            name='player_fk',
        ),
        migrations.RemoveField(
            model_name='game',
            name='hand1',
        ),
        migrations.RemoveField(
            model_name='game',
            name='hand2',
        ),
        migrations.RemoveField(
            model_name='game',
            name='hand3',
        ),
        migrations.RemoveField(
            model_name='game',
            name='hand4',
        ),
        migrations.AddField(
            model_name='deck',
            name='player_fk',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='game.Player'),
        ),
        migrations.DeleteModel(
            name='Hand',
        ),
    ]