import os
import csv
from optparse import make_option

from django.core.management.base import BaseCommand, CommandError
from django.contrib.sites.models import Site
from django.core.exceptions import ObjectDoesNotExist

from cms_redirects.models import CMSRedirect

class Command(BaseCommand):
    can_import_settings = True
    help='''Import redirects'''
    args = "<csv_path>"
    
    option_list = BaseCommand.option_list + (
            make_option('--site',
                dest="site",
                default=Site.objects.get_current(),
                help="Use to specify the domain of the site you are importing redirects into.  Defaults to current site."),
            )
    
    def execute(self, *args, **options):
        if len(args) != 1:
            raise CommandError("Must pass in the absolute path to the csv import file")
        csv_path = args[0]
        
        if not os.path.exists(csv_path):
            raise CommandError("File not found, invalid path: %s" % csv_path)
        csv_file = open(csv_path, "rb")
        reader = csv.reader(csv_file)
        header_row = reader.next()
        if header_row != ["Old Url","New Url","Response Code"]:
            raise CommandError("CSV file is missing the correct header row.  Should be Old Url, New Url and Response Code")
        reader = csv.DictReader(csv_file, header_row)
            
        current_site = options["site"]
        if not isinstance(current_site, Site):
            try:
                current_site = Site.objects.get(domain=options["site"])
            except ObjectDoesNotExist:
                raise CommandError("No site found, invalid domain: %s" % options["site"])
                
        for row in reader:
            old_url = row["Old Url"]
            new_url = row["New Url"]
            resp_code = row["Response Code"]
            if resp_code not in ['301', '302']:
                resp_code = '301'
            redirect, created = CMSRedirect.objects.get_or_create(site=current_site, old_path=old_url)
            redirect.new_path = new_url
            redirect.response_code = resp_code
            redirect.save()
            
        
        
        
            
            
          
          
        
