# Generated by Django 3.2.16 on 2022-11-29 16:53

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import formation_metier.models.seance


class Migration(migrations.Migration):

    replaces = [('formation_metier', '0001_initial'), ('formation_metier', '0002_alter_register_register_date'), ('formation_metier', '0003_alter_register_register_date'), ('formation_metier', '0004_alter_register_register_date'), ('formation_metier', '0005_auto_20221026_1351'), ('formation_metier', '0006_alter_register_register_date'), ('formation_metier', '0007_rename_formation_code_session_formation'), ('formation_metier', '0008_person'), ('formation_metier', '0009_alter_register_participant'), ('formation_metier', '0010_register_unique_register'), ('formation_metier', '0011_formation_unique_formation_code_name'), ('formation_metier', '0012_formation_unique_formation_code'), ('formation_metier', '0013_remove_formation_unique_formation_code_name'), ('formation_metier', '0014_session_public_cible'), ('formation_metier', '0015_alter_session_public_cible'), ('formation_metier', '0016_auto_20221110_0925'), ('formation_metier', '0017_alter_roleosis_name'), ('formation_metier', '0018_auto_20221116_1115'), ('formation_metier', '0019_alter_formation_code'), ('formation_metier', '0020_alter_formation_code'), ('formation_metier', '0021_auto_20221117_1529'), ('formation_metier', '0022_alter_person_role_formation_metier'), ('formation_metier', '0023_person_unique_person'), ('formation_metier', '0024_auto_20221121_1358'), ('formation_metier', '0025_rename_formateur_session_formateur_id'), ('formation_metier', '0026_rename_formateur_id_session_formateur'), ('formation_metier', '0027_session_unique_session'), ('formation_metier', '0028_alter_register_participant'), ('formation_metier', '0029_person_user'), ('formation_metier', '0030_auto_20221122_1538'), ('formation_metier', '0031_alter_person_user'), ('formation_metier', '0032_alter_person_role_formation_metier'), ('formation_metier', '0033_alter_person_options'), ('formation_metier', '0034_auto_20221125_1344'), ('formation_metier', '0035_auto_20221125_1505'), ('formation_metier', '0036_auto_20221128_0905'), ('formation_metier', '0037_alter_seance_formateur'), ('formation_metier', '0038_alter_seance_participant_max_number'), ('formation_metier', '0039_auto_20221129_1212'), ('formation_metier', '0040_auto_20221129_1341')]

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Formation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=9)),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('local', models.CharField(max_length=50)),
                ('formateur', models.CharField(max_length=50)),
                ('formation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='formation_metier.formation')),
                ('participant_max_number', models.IntegerField(default=0)),
                ('session_date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('numberFGS', models.CharField(max_length=8)),
                ('role', models.CharField(choices=[('admin', 'admin'), ('formateur', 'formateur'), ('participant', 'participant')], max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Register',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('participant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='formation_metier.person')),
                ('register_date', models.DateTimeField(auto_now_add=True)),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='formation_metier.session')),
            ],
        ),
        migrations.AddConstraint(
            model_name='register',
            constraint=models.UniqueConstraint(fields=('session', 'participant'), name='unique_register'),
        ),
        migrations.AddConstraint(
            model_name='formation',
            constraint=models.UniqueConstraint(fields=('code', 'name'), name='unique_formation_code_name'),
        ),
        migrations.AddConstraint(
            model_name='formation',
            constraint=models.UniqueConstraint(fields=('code',), name='unique_formation_code'),
        ),
        migrations.RemoveConstraint(
            model_name='formation',
            name='unique_formation_code_name',
        ),
        migrations.AddField(
            model_name='session',
            name='public_cible',
            field=models.CharField(choices=[('Admin', 'Administrateurs'), ('Form', 'Formateurs'), ('Part', 'Participant')], default='Part', max_length=50),
        ),
        migrations.CreateModel(
            name='Formateur',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='RoleOsis',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.RemoveField(
            model_name='person',
            name='role',
        ),
        migrations.AddField(
            model_name='person',
            name='role_formation_metier',
            field=models.CharField(choices=[('Admin', 'Administrateurs'), ('Form', 'Formateurs'), ('Part', 'Participant')], default='Part', max_length=20),
        ),
        migrations.CreateModel(
            name='PersonRole',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('formateur', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='formation_metier.formateur')),
                ('participant', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='formation_metier.participant')),
                ('role_osis', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='formation_metier.roleosis')),
            ],
        ),
        migrations.AddField(
            model_name='participant',
            name='person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='formation_metier.person'),
        ),
        migrations.AddField(
            model_name='formateur',
            name='person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='formation_metier.person'),
        ),
        migrations.AddConstraint(
            model_name='personrole',
            constraint=models.CheckConstraint(check=models.Q(('participant__isnull', False), ('formateur__isnull', False), _connector='OR'), name='constraint_formateur_or_participant'),
        ),
        migrations.AlterField(
            model_name='roleosis',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='formation',
            name='code',
            field=models.CharField(max_length=6, validators=[django.core.validators.RegexValidator('^[A-Z]{1-4}[1-9]{1-2}$')]),
        ),
        migrations.DeleteModel(
            name='PersonRole',
        ),
        migrations.DeleteModel(
            name='RoleOsis',
        ),
        migrations.AlterField(
            model_name='formation',
            name='code',
            field=models.CharField(max_length=6, validators=[django.core.validators.RegexValidator('^[A-Z]{1-4}[0-9]{1-2}$')]),
        ),
        migrations.AlterField(
            model_name='formation',
            name='code',
            field=models.CharField(max_length=6, validators=[django.core.validators.RegexValidator('^[A-Za-z]{1,4}[0-9]{1,2}$')]),
        ),
        migrations.AlterField(
            model_name='person',
            name='role_formation_metier',
            field=models.CharField(blank=True, choices=[('CENTRAL_MANAGER_EDUCATION_GROUP', 'Central Manager Education Group'), ('FACTULTY_MANAGER_EDUCATION_GROUP', 'Faculty Manager Education Group'), ('CONTINUING_EDUCATION_TRAINING_MANAGER', 'Continuing Education Training Manager'), ('CONTINUING_EDUCATION_STUDENT_WORKER', 'Continuing Education Student Worker'), ('CONTINUING_EDUCATION_MANAGER', 'Continuing Education Manager'), ('PARTNERSHIP_ENTITY_MANAGER', 'Partnership Entity Manager'), ('PARTNERSHIP_VIEWER', 'Partnership Viewer'), ('PARCOURS_VIEWER', 'Parcours Viewer'), ('TUTOR', 'Tutor'), ('PROGRAM_MANAGER', 'Program Manager'), ('ENTITY_MANAGER', 'Entity Manager'), ('CATALOG_VIEWER', 'Catalog Viewer'), ('JURY_SECRETARY', 'Jury Secretary'), ('SIC_DIRECTOR', 'Sic Director'), ('SIC_MANAGER', 'Sic Manager'), ('SCEB', 'Sceb'), ('PROMOTER', 'Promoter'), ('DOCTORATE_READER', 'Doctorate Reader'), ('CDD_MANAGER', 'Cdd Manager'), ('COMMITTEE_MEMBER', 'Committee Member'), ('ADRE_SECRETARY', 'Adre Secretary'), ('CANDIDATE', 'Candidate'), ('CENTRAL_ADMISSION_MANAGER_EDUCATION_GROUP', 'Central Admission Manager Education Group'), ('CENTRAL_MANAGER_LEARNING_UNIT', 'Central Manager Learning Unit'), ('FACULTY_MANAGER_LEARNING_UNIT', 'Faculty Manager Learning Unit')], default=None, max_length=50),
        ),
        migrations.AlterField(
            model_name='session',
            name='public_cible',
            field=models.CharField(choices=[('CENTRAL_MANAGER_EDUCATION_GROUP', 'Central Manager Education Group'), ('FACTULTY_MANAGER_EDUCATION_GROUP', 'Faculty Manager Education Group'), ('CONTINUING_EDUCATION_TRAINING_MANAGER', 'Continuing Education Training Manager'), ('CONTINUING_EDUCATION_STUDENT_WORKER', 'Continuing Education Student Worker'), ('CONTINUING_EDUCATION_MANAGER', 'Continuing Education Manager'), ('PARTNERSHIP_ENTITY_MANAGER', 'Partnership Entity Manager'), ('PARTNERSHIP_VIEWER', 'Partnership Viewer'), ('PARCOURS_VIEWER', 'Parcours Viewer'), ('TUTOR', 'Tutor'), ('PROGRAM_MANAGER', 'Program Manager'), ('ENTITY_MANAGER', 'Entity Manager'), ('CATALOG_VIEWER', 'Catalog Viewer'), ('JURY_SECRETARY', 'Jury Secretary'), ('SIC_DIRECTOR', 'Sic Director'), ('SIC_MANAGER', 'Sic Manager'), ('SCEB', 'Sceb'), ('PROMOTER', 'Promoter'), ('DOCTORATE_READER', 'Doctorate Reader'), ('CDD_MANAGER', 'Cdd Manager'), ('COMMITTEE_MEMBER', 'Committee Member'), ('ADRE_SECRETARY', 'Adre Secretary'), ('CANDIDATE', 'Candidate'), ('CENTRAL_ADMISSION_MANAGER_EDUCATION_GROUP', 'Central Admission Manager Education Group'), ('CENTRAL_MANAGER_LEARNING_UNIT', 'Central Manager Learning Unit'), ('FACULTY_MANAGER_LEARNING_UNIT', 'Faculty Manager Learning Unit')], default=None, max_length=50),
        ),
        migrations.AlterField(
            model_name='person',
            name='role_formation_metier',
            field=models.CharField(blank=True, choices=[('PARTICIPANT', 'Participant'), ('FORMATEUR', 'Formateur'), ('ADMIN', 'Administrateur')], default=None, max_length=50),
        ),
        migrations.AddConstraint(
            model_name='person',
            constraint=models.UniqueConstraint(fields=('numberFGS',), name='unique_person'),
        ),
        migrations.AddField(
            model_name='session',
            name='duree',
            field=models.PositiveSmallIntegerField(default=60, validators=[django.core.validators.MaxValueValidator(600)]),
        ),
        migrations.RenameField(
            model_name='session',
            old_name='formateur',
            new_name='formateur',
        ),
        migrations.AlterField(
            model_name='session',
            name='formateur',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='formation_metier.formateur'),
        ),
        migrations.AddConstraint(
            model_name='session',
            constraint=models.UniqueConstraint(fields=('session_date', 'local', 'formateur'), name='unique_session'),
        ),
        migrations.AlterField(
            model_name='register',
            name='participant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='formation_metier.participant'),
        ),
        migrations.AddField(
            model_name='person',
            name='user',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddConstraint(
            model_name='person',
            constraint=models.CheckConstraint(check=models.Q(models.Q(('role_formation_metier__in', ['FORMATEUR', 'ADMIN']), ('user__isnull', False)), models.Q(('role_formation_metier', 'PARTICIPANT'), ('user__isnull', True)), _connector='OR'), name='only_participant_have_user_null'),
        ),
        migrations.AlterField(
            model_name='person',
            name='user',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='person',
            name='role_formation_metier',
            field=models.CharField(choices=[('PARTICIPANT', 'Participant'), ('FORMATEUR', 'Formateur'), ('ADMIN', 'Administrateur')], default='PARTICIPANT', max_length=50),
        ),
        migrations.AlterModelOptions(
            name='person',
            options={'permissions': (('access_to_formation_fare', 'Global access to module formation FARE'),)},
        ),
        migrations.RemoveField(
            model_name='session',
            name='public_cible',
        ),
        migrations.AddField(
            model_name='formation',
            name='public_cible',
            field=models.CharField(choices=[('CENTRAL_MANAGER_EDUCATION_GROUP', 'Central Manager Education Group'), ('FACTULTY_MANAGER_EDUCATION_GROUP', 'Faculty Manager Education Group'), ('CONTINUING_EDUCATION_TRAINING_MANAGER', 'Continuing Education Training Manager'), ('CONTINUING_EDUCATION_STUDENT_WORKER', 'Continuing Education Student Worker'), ('CONTINUING_EDUCATION_MANAGER', 'Continuing Education Manager'), ('PARTNERSHIP_ENTITY_MANAGER', 'Partnership Entity Manager'), ('PARTNERSHIP_VIEWER', 'Partnership Viewer'), ('PARCOURS_VIEWER', 'Parcours Viewer'), ('TUTOR', 'Tutor'), ('PROGRAM_MANAGER', 'Program Manager'), ('ENTITY_MANAGER', 'Entity Manager'), ('CATALOG_VIEWER', 'Catalog Viewer'), ('JURY_SECRETARY', 'Jury Secretary'), ('SIC_DIRECTOR', 'Sic Director'), ('SIC_MANAGER', 'Sic Manager'), ('SCEB', 'Sceb'), ('PROMOTER', 'Promoter'), ('DOCTORATE_READER', 'Doctorate Reader'), ('CDD_MANAGER', 'Cdd Manager'), ('COMMITTEE_MEMBER', 'Committee Member'), ('ADRE_SECRETARY', 'Adre Secretary'), ('CANDIDATE', 'Candidate'), ('CENTRAL_ADMISSION_MANAGER_EDUCATION_GROUP', 'Central Admission Manager Education Group'), ('CENTRAL_MANAGER_LEARNING_UNIT', 'Central Manager Learning Unit'), ('FACULTY_MANAGER_LEARNING_UNIT', 'Faculty Manager Learning Unit')], default=None, max_length=50),
        ),
        migrations.RenameModel(
            old_name='Session',
            new_name='Seance',
        ),
        migrations.RemoveConstraint(
            model_name='register',
            name='unique_register',
        ),
        migrations.RemoveConstraint(
            model_name='seance',
            name='unique_session',
        ),
        migrations.RenameField(
            model_name='register',
            old_name='session',
            new_name='seance',
        ),
        migrations.RenameField(
            model_name='seance',
            old_name='session_date',
            new_name='seance_date',
        ),
        migrations.AddConstraint(
            model_name='register',
            constraint=models.UniqueConstraint(fields=('seance', 'participant'), name='unique_register'),
        ),
        migrations.AddConstraint(
            model_name='seance',
            constraint=models.UniqueConstraint(fields=('seance_date', 'local', 'formateur'), name='unique_session'),
        ),
        migrations.CreateModel(
            name='EmployeUCLouvain',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('numberFGS', models.CharField(max_length=8)),
                ('role_formation_metier', models.CharField(choices=[('PARTICIPANT', 'Participant'), ('FORMATEUR', 'Formateur'), ('ADMIN', 'Administrateur')], default='PARTICIPANT', max_length=50)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'permissions': (('access_to_formation_fare', 'Global access to module formation FARE'),),
            },
        ),
        migrations.RemoveField(
            model_name='formateur',
            name='person',
        ),
        migrations.RemoveField(
            model_name='participant',
            name='person',
        ),
        migrations.DeleteModel(
            name='Person',
        ),
        migrations.AlterField(
            model_name='register',
            name='participant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='formation_metier.employeuclouvain'),
        ),
        migrations.AlterField(
            model_name='seance',
            name='formateur',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='formation_metier.employeuclouvain'),
        ),
        migrations.DeleteModel(
            name='Formateur',
        ),
        migrations.DeleteModel(
            name='Participant',
        ),
        migrations.AddConstraint(
            model_name='employeuclouvain',
            constraint=models.UniqueConstraint(fields=('numberFGS',), name='unique_person'),
        ),
        migrations.AlterField(
            model_name='seance',
            name='formateur',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='formation_metier.employeuclouvain', validators=[formation_metier.models.seance.validate_formateur]),
        ),
        migrations.AlterField(
            model_name='seance',
            name='participant_max_number',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.RemoveConstraint(
            model_name='employeuclouvain',
            name='unique_person',
        ),
        migrations.RenameField(
            model_name='employeuclouvain',
            old_name='numberFGS',
            new_name='number_fgs',
        ),
        migrations.AddConstraint(
            model_name='employeuclouvain',
            constraint=models.UniqueConstraint(fields=('number_fgs',), name='unique_person'),
        ),
        migrations.RemoveConstraint(
            model_name='register',
            name='unique_register',
        ),
        migrations.AlterUniqueTogether(
            name='register',
            unique_together={('seance', 'participant')},
        ),
    ]
