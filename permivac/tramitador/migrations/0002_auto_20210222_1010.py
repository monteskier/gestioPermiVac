# Generated by Django 3.1.7 on 2021-02-22 09:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tramitador', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='treballadors',
            name='foto',
            field=models.FileField(blank=True, null=True, upload_to='fotos'),
        ),
        migrations.AddField(
            model_name='treballadors',
            name='id_crosschex',
            field=models.IntegerField(blank=True, max_length=4, null=True),
        ),
        migrations.AddField(
            model_name='treballadors',
            name='observacions',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='treballadors',
            name='pass_crosschex',
            field=models.IntegerField(blank=True, max_length=4, null=True),
        ),
        migrations.AlterField(
            model_name='calendari',
            name='any',
            field=models.IntegerField(choices=[(1984, 1984), (1985, 1985), (1986, 1986), (1987, 1987), (1988, 1988), (1989, 1989), (1990, 1990), (1991, 1991), (1992, 1992), (1993, 1993), (1994, 1994), (1995, 1995), (1996, 1996), (1997, 1997), (1998, 1998), (1999, 1999), (2000, 2000), (2001, 2001), (2002, 2002), (2003, 2003), (2004, 2004), (2005, 2005), (2006, 2006), (2007, 2007), (2008, 2008), (2009, 2009), (2010, 2010), (2011, 2011), (2012, 2012), (2013, 2013), (2014, 2014), (2015, 2015), (2016, 2016), (2017, 2017), (2018, 2018), (2019, 2019), (2020, 2020), (2021, 2021), (2022, 2022)], default=2021, verbose_name='any'),
        ),
        migrations.AlterField(
            model_name='treballadors',
            name='first_name',
            field=models.CharField(blank=True, max_length=150, verbose_name='first name'),
        ),
    ]
