# Generated by Django 3.2.5 on 2021-07-28 01:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('banner', models.URLField()),
                ('featured', models.BooleanField(default=False)),
                ('description', models.TextField(blank=True, null=True)),
                ('difficulty', models.IntegerField(choices=[(0, 'Easy'), (1, 'Moderate'), (2, 'Difficult'), (3, 'Expert')], default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('duration', models.DurationField()),
                ('points', models.IntegerField()),
                ('content', models.TextField()),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lessons', to='courses.course')),
            ],
        ),
    ]
