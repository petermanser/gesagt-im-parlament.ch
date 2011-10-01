import json
from datetime import datetime
from django.core.management.base import NoArgsCommand
from apps.front import models

JSON_FILE = '/home/danilo/Projects/Parlament/data/affairs.json'

class Command(NoArgsCommand):
    args = '<json file>'
    help = 'Parse json file with affairs data and write it into database'

    def printO(self, message):
        """Print to stdout"""
        self.stdout.write(message + '\n')

    def printE(self, message):
        """Print to stderr"""
        self.stderr.write(message + '\n')

    def handle_noargs(self, **options):
        json_file = open(JSON_FILE, 'r') 
        for row in json_file:
            # Set initial flag
            failed = False

            # Parse json
            obj = json.loads(row)
            
            # Write affair
            try:
                affair = models.Affair()
                affair.id = obj['id']
                affair.title = obj['title']
                affair.type = obj['gsType']
                affair.congress = obj['congress']
                affair.state = obj['state']
                affair.submission_date = datetime.strptime(obj['submissionDate'], '%d.%m.%Y')
                affair.content = obj['content']
                affair.save()
                self.printO('Parsed [%s] %s' % (affair.id, affair.title))
            except Exception as e:
                failed = True
                self.printE('Failed to parse affair %s (%s)' % (obj['id'], str(e)))
            
            # Write person
            try:
                person = models.Person.objects.get(id=obj['submitterId'])
            except models.Person.DoesNotExist:
                try:
                    person = models.Person()
                    person.id = int(obj['submitterId'])
                    person.name = obj['submitter']
                    person.url = obj['submitterLink']
                    person.save()
                    self.printO('Created person %s.' % person.name)
                except Exception as e:
                    failed = True
                    self.printE('Failed to create person %s (%s)' % (obj['submitter'], str(e)))

            # Create relation
            if not failed:
                try:
                    person_affair = models.PersonAffair.objects.create(
                                        person = person,
                                        affair = affair,
                                        type = 0)
                except Exception as e:
                    self.printE('Failed to create relation with person %s and affair %s (%s)' % (person.name, affair.id, str(e)))
