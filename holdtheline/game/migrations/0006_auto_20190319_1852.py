# Generated by Django 2.1.7 on 2019-03-19 18:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0005_auto_20190319_1849'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='deck',
            name='card',
        ),
        migrations.AddField(
            model_name='deck',
            name='card_fk',
            field=models.ForeignKey(default=-1, on_delete=django.db.models.deletion.CASCADE, related_name='card_fk', to='game.Card'),
        ),
        migrations.AlterField(
            model_name='deck',
            name='game_fk',
            field=models.ForeignKey(default=-1, on_delete=django.db.models.deletion.CASCADE, related_name='game_fk', to='game.Game'),
        ),
    ]