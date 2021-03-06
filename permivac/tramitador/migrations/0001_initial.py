# Generated by Django 2.2.1 on 2019-09-12 10:20

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='Treballadors',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('usuari', models.CharField(max_length=20)),
                ('dni', models.CharField(blank=True, max_length=20, null=True)),
            ],
            options={
                'ordering': ['first_name', 'last_name'],
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcio', models.CharField(blank=True, max_length=255)),
                ('document', models.FileField(upload_to='%Y/%m/')),
                ('pujat_en', models.DateTimeField(auto_now_add=True)),
                ('pujat_per', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Tramit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creat_en', models.DateTimeField(auto_now_add=True)),
                ('modificat_en', models.DateTimeField(auto_now=True)),
                ('data_sol', models.CharField(help_text="Interval de dates amb guións '/', per dies no consecutios emprar ';' Exemple:2019-08-01-2019-08-20;2019-09-09", max_length=250)),
                ('tipus', models.CharField(choices=[('vacances', 'Vacances'), ('perm_precep', 'Permisos preceptius'), ('perm_no_precep', 'Permisos no preceptius'), ('asum_p', 'Asumptes personals'), ('perm_indisposicio', 'Permis Indisposicio'), ('perm_altres', 'Altres permissos')], default='asum_p', max_length=40)),
                ('finalitzat', models.BooleanField(default=False)),
                ('valRRHH', models.CharField(choices=[('conforme', 'conforme'), ('inconforme', 'no conforme'), ('espera', 'en espera')], default='espera', max_length=20)),
                ('valResp', models.CharField(choices=[('conforme', 'conforme'), ('inconforme', 'no conforme'), ('espera', 'en espera')], default='espera', max_length=20)),
                ('valPol', models.CharField(choices=[('conforme', 'conforme'), ('inconforme', 'no conforme'), ('espera', 'en espera')], default='espera', max_length=20)),
                ('missatge_usuari', models.CharField(max_length=2000, null=True)),
                ('missatge_responsable', models.CharField(blank=True, max_length=2000, null=True)),
                ('document', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='tramitador.Document')),
                ('treballador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Calendari',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('any', models.IntegerField(choices=[(1984, 1984), (1985, 1985), (1986, 1986), (1987, 1987), (1988, 1988), (1989, 1989), (1990, 1990), (1991, 1991), (1992, 1992), (1993, 1993), (1994, 1994), (1995, 1995), (1996, 1996), (1997, 1997), (1998, 1998), (1999, 1999), (2000, 2000), (2001, 2001), (2002, 2002), (2003, 2003), (2004, 2004), (2005, 2005), (2006, 2006), (2007, 2007), (2008, 2008), (2009, 2009), (2010, 2010), (2011, 2011), (2012, 2012), (2013, 2013), (2014, 2014), (2015, 2015), (2016, 2016), (2017, 2017), (2018, 2018), (2019, 2019), (2020, 2020)], default=2019, verbose_name='any')),
                ('vacances', models.IntegerField(default=22, verbose_name='Vacances disponibles')),
                ('vacances_dies', models.CharField(blank=True, max_length=500)),
                ('perm_precep', models.IntegerField(default=0, verbose_name='Permissos preceptius fets:')),
                ('perm_precep_dies', models.CharField(blank=True, max_length=500)),
                ('perm_no_precep', models.IntegerField(default=0, verbose_name='Permissos no preceptius fets:')),
                ('perm_no_precep_dies', models.CharField(blank=True, max_length=500)),
                ('asum_p', models.IntegerField(default=6, verbose_name='Assumptes perosnals disponibles:')),
                ('asum_p_dies', models.CharField(blank=True, max_length=500)),
                ('perm_indisposicio', models.IntegerField(blank=True, default=0, verbose_name='Permissos per indisposició fets:')),
                ('perm_indisposicio_dies', models.CharField(blank=True, max_length=500)),
                ('perm_altres', models.IntegerField(blank=True, default=0, verbose_name='Altres permissos')),
                ('perm_altres_dies', models.CharField(blank=True, max_length=500)),
                ('treballador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='treballadors',
            name='areas',
            field=models.ManyToManyField(to='tramitador.Area'),
        ),
        migrations.AddField(
            model_name='treballadors',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='treballadors',
            name='representant',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='treballadors',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
    ]
