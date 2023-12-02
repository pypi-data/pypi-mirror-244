from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project_ethics', '0008_alter_ethicfile_options_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='EthicFile',
            new_name='EthicsFile',
        ),
    ]
