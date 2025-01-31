# Generated by Django 5.1.1 on 2024-09-13 12:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leave_management', '0002_leaverequest_calendar_event_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='calendarevent',
            name='leave_request',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='calendar_events', to='leave_management.leaverequest'),
        ),
        migrations.AddField(
            model_name='leavesummary',
            name='leave_request',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='leave_summaries', to='leave_management.leaverequest'),
        ),
    ]
