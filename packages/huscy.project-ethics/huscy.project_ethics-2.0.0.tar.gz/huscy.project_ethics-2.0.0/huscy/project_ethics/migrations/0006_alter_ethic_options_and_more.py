from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0003_project_project_manager_and_more'),
        ('project_ethics', '0005_rename_ethicboard_ethicscommittee_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ethic',
            options={'ordering': ('-project', 'ethics_committee__name'), 'verbose_name': 'Ethic', 'verbose_name_plural': 'Ethics'},
        ),
        migrations.RenameField(
            model_name='ethic',
            old_name='ethic_board',
            new_name='ethics_committee',
        ),
        migrations.AlterUniqueTogether(
            name='ethic',
            unique_together={('project', 'ethics_committee')},
        ),
    ]
