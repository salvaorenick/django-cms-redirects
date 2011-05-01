import StringIO
import csv
import datetime

from django.core.management.base import BaseCommand, CommandError
from django.contrib.sites.models import Site
from django.conf import settings
from django.utils import simplejson

from googleanalytics import Connection
from optparse import make_option

class Command(BaseCommand):
    can_import_settings = True
    help='''
    
    Sends to stdout a csv file that can be used to import redirects.
    
    Optionally, you can specify google analytics account information to
    prepopulate the csv file.
    
    Usage:
    ./manage.py redirect_csv > import.csv
    ./manage.py redirect_csv -ga > import_google_analytics.csv
    
    '''
    option_list = BaseCommand.option_list + (
            make_option('--rows',
                dest="num_rows",
                default=5,
                help="Use to specify the number of extra rows"),
            make_option('--ga',
                action='store_true',
                dest="use_analytics",
                default=False,
                help="Use google analytics data to preopulate the csv"),
            make_option('--gauser',
                dest="ga_user",
                default=getattr(settings,"REDIRECT_GA_USERNAME",None),
                help="Google analytics user, defaults to settings.REDIRECT_GA_USERNAME"),
            make_option('--gapwd',
                dest="ga_pwd",
                default=getattr(settings, "REDIRECT_GA_PASSWORD",None),
                help="Google analytics password, defaults to settings.REDIRECT_GA_PASSWORD"),
            make_option('--gaprofile',
                dest="ga_profile",
                default=getattr(settings, "REDIRECT_GA_PROFILE", None),
                help="Google analytics profile, defaults to settings.REDIRECT_GA_PROFILE"),
            make_option('--gamonths',
                dest="num_analytics_months",
                default=6,
                help="Number of months to pull google analytics data for"),
            )
    
    
    def execute(self, *args, **options):
        num_rows =  options["num_rows"]
        output = StringIO.StringIO()
        writer = csv.writer(output)
        writer.writerow(['Old Url','New Url','Response Code'])
        writer.writerow(["/old.html","/new",'301, 302 or 410'])
        if options["use_analytics"]:
            connection = Connection(options["ga_user"], options["ga_pwd"])
            account = connection.get_account(options["ga_profile"])
            end_date = datetime.date.today()
            num_months = options["num_analytics_months"]
            start_date = end_date - datetime.timedelta(num_months*365/12)
            data = account.get_data(start_date=start_date, end_date=end_date, dimensions=['pagepath'], metrics=['visits'])
            for url, visits in data.dict.iteritems():
                writer.writerow([csv_safe(url),'',''])
        else:
            [writer.writerow(['','','']) for row in range(0,num_rows)]
        print output.getvalue()
        
def csv_safe(s):
    if isinstance(s,basestring):
        return s.encode("utf-8")
    else:
        return s
        
        
        