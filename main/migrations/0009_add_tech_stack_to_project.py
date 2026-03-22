from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_remove_testimonial_quote_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='tech_stack',
            field=models.CharField(
                blank=True,
                default='',
                help_text='Comma-separated tags e.g. Python, Django, Docker',
                max_length=300,
            ),
        ),
    ]
