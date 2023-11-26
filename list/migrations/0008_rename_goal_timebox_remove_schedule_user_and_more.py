# Generated by Django 4.0.4 on 2023-08-12 23:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('list', '0007_alter_itemgoal_text_alter_itempriority_text_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Goal',
            new_name='Timebox',
        ),
        migrations.RemoveField(
            model_name='schedule',
            name='user',
        ),
        migrations.AddField(
            model_name='itemgoal',
            name='timebox',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='list.timebox'),
        ),
        migrations.AddField(
            model_name='itempriority',
            name='timebox',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='list.timebox'),
        ),
        migrations.AddField(
            model_name='itemschedule',
            name='timebox',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='list.timebox'),
        ),
        migrations.AlterField(
            model_name='itemgoal',
            name='text',
            field=models.CharField(max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='itempriority',
            name='text',
            field=models.CharField(max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='itemschedule',
            name='text',
            field=models.CharField(max_length=300, null=True),
        ),
        migrations.DeleteModel(
            name='Priority',
        ),
        migrations.DeleteModel(
            name='Schedule',
        ),
    ]