from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0003_project_project_manager_and_more'),
        ('project_ethics', '0006_alter_ethic_options_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Ethic',
            new_name='Ethics',
        ),
        migrations.AlterModelOptions(
            name='ethics',
            options={'ordering': ('-project', 'ethics_committee__name'), 'verbose_name': 'Ethics', 'verbose_name_plural': 'Ethics'},
        ),
        migrations.AlterField(
            model_name='ethicfile',
            name='ethic',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='ethic_files', to='project_ethics.ethics', verbose_name='Ethics'),
        ),
    ]
