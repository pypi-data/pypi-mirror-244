from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('project_ethics', '0009_rename_ethicfile_ethicsfile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ethicsfile',
            name='ethics',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='ethics_files', to='project_ethics.ethics', verbose_name='Ethics'),
        ),
    ]
