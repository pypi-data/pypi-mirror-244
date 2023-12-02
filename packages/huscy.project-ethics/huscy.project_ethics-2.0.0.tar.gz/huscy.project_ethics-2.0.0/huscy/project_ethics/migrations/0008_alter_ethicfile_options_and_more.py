from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project_ethics', '0007_rename_ethic_ethics_alter_ethics_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ethicfile',
            options={'ordering': ('-ethics__project', '-ethics', 'filename'), 'verbose_name': 'Ethic file', 'verbose_name_plural': 'Ethic files'},
        ),
        migrations.RenameField(
            model_name='ethicfile',
            old_name='ethic',
            new_name='ethics',
        ),
    ]
