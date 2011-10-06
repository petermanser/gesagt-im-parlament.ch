import json
import re
from django.http import HttpResponse
from django.db.models import Count, Q
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic import TemplateView, ListView, DetailView
from apps.front import models
from apps.front.stopwords import stopwords


class Persons(ListView):
    queryset = models.Faction.objects.annotate(person_count=Count('persons')).order_by('-person_count')
    context_object_name = 'factions'
    template_name = 'persons.html'

    def get_context_data(self, **kwargs):
        context = super(Persons, self).get_context_data(**kwargs)
        nofaction_persons = models.Person.objects.all().filter(faction__isnull=True)
        context['nofaction_persons'] = nofaction_persons
        return context


class Person(DetailView):
    model = models.Person
    context_object_name = 'person'
    template_name = 'person.html'

    def get_context_data(self, object, **kwargs):
        context = super(Person, self).get_context_data(**kwargs)
        
        # Minimum of times a word must appear to be in the final list
        min_word_count = 3
        max_words = 30

        affairs = object.affair_set.all()

        # Get all content words
        contents = [a.content.split(' ') for a in affairs]
        # Flatten "list in list"
        words = sum(contents, [])  
        # Strip all non-letters and convert to lowercase
        pattern = re.compile('[\W]+')
        words_clean = map(lambda x: filter(lambda y: y.isalnum() and not y.isdigit(), x).lower(), words)
        # Remove all empty words
        words_filtered = filter(None, words_clean)
        # Remove stopwords
        words_relevant = filter(lambda x: x not in stopwords, words_filtered)

        # Create map with words as key and count as value
        word_counts = {}
        for word in words_relevant:
            if word in word_counts:
                word_counts[word] += 1
            else:
                word_counts[word] = 1

        # Sort words
        words_sorted = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)

        # Put words that appear enough times in final map
        final = {}
        for word, count in words_sorted[:max_words]:
            if count >= min_word_count:
                final[word] = count
            else:
                break

        # Update context
        context['affair_count'] = affairs.count()
        context['words'] = json.dumps(final)

        return context


class Search(ListView):
    context_object_name = 'persons'
    model = models.Person
    template_name = 'search_results.html'

    def get_queryset(self):
        q = self.request.GET.get('q', None)
        if q:
            return self.model.objects.filter(
                Q(name__icontains=q) | Q(party__short_name__istartswith=q)
            )
        return None

    def get_context_data(self, **kwargs):
        context = super(Search, self).get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q', None)
        return context
