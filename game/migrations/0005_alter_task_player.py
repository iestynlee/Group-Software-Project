# Generated by Django 4.0.2 on 2022-03-24 00:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0004_remove_player_playername'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='player',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='game.player'),
        ),
    ]
