from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('project_ethics', '0004_alter_ethicfile_filetype'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='EthicBoard',
            new_name='EthicsCommittee',
        ),
        migrations.AlterModelOptions(
            name='ethicscommittee',
            options={'ordering': ('name',), 'verbose_name': 'Ethics committee', 'verbose_name_plural': 'Ethics committees'},
        ),
        migrations.AlterField(
            model_name='ethic',
            name='ethic_board',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='project_ethics.ethicscommittee', verbose_name='Ethics committee'),
        ),
    ]
