import json
import re
from itertools import chain
from collections import defaultdict
from django.http import HttpResponse
from django.db.models import Count, Q
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic import TemplateView, ListView, DetailView
from apps.front import models
from apps.front.stopwords import stopwords
from apps.front.sentiments import positive
from apps.front.sentiments import negative
from apps.front.sentiments import neutral

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
        #contents = [a.content.split(' ') for a in affairs]
        sentence_list_of_lists = [a.content.split('.') for a in affairs]

        # Flatten "list in list"
        #wordlist_contents = sum(contents, [])
        sentences = sum(sentence_list_of_lists, [])

        #sentence_sentiments = map (lambda sentence: sentence:sentence_sentiment(sentence) , sentence_contents)

        def sentence_sentiment(sentence):
            sentiment = 0
            split_sentence = sentence.split(' ')
            for word in split_sentence:
                lowercase_word = word.lower()
                if (lowercase_word in positive):
                    sentiment += 1
                if (lowercase_word in negative):
                    sentiment -= 1
            return sentiment

        # Get all title words
        title_list_of_lists = [a.title.split(' ') for a in affairs]
        # Flatten "list in list"
        title_sentences = sum(title_list_of_lists, [])  

        def process_sentence(sentence, weight=1):
            # Strip all non-letters and convert to lowercase
                #pattern = re.compile('[\W]+')
                #words_clean = map(lambda x: pattern.sub('', x).lower(), words)
            sentiment = sentence_sentiment(sentence)
            wordlist = sentence.split(' ')
            words_semiclean = map(lambda x: filter(lambda y: y.isalnum() or y.isdigit(), x).lower(), wordlist)
            words_clean = filter(lambda w: not w.isdigit(), words_semiclean)
            # Remove all empty words
            words_filtered = filter(None, words_clean)
            # Remove stopwords
            words_relevant = filter(lambda x: x not in stopwords, words_filtered)

            # Create map with words as key and count as value
            word_counts = {}
            word_sentiments = {}
            for word in words_relevant:
                if word in word_counts:
                    word_counts[word] += weight
                else:
                    word_counts[word] = weight
                word_sentiments[word] = sentiment
            return (word_counts, word_sentiments)

        # Process both sets with different weights		
        #processed_contents = process_wordlist(wordlist_contents, 1)
        #processed_titles = process_wordlist(wordlist_titles, 3)
        aggregated_word_counts = {}
        aggregated_word_sentiments = {}
        def aggregate_sentence_statistics(word_counts, word_sentiments, sentence, weight=1):
            (counts, sentiments) = process_sentence(sentence)
            for word in counts:
                if word in word_counts:
                    old_count = word_counts[word]
                    word_counts[word] = old_count + weight*counts[word]
                else:
                    word_counts[word] = weight*counts[word]
                if word in word_sentiments:
                    old_sentiment = word_sentiments[word]
                    word_sentiments[word] = old_sentiment + sentiments[word]
                else:
                    word_sentiments[word] = sentiments[word]

        for sentence in sentences:
            aggregate_sentence_statistics(aggregated_word_counts, aggregated_word_sentiments, sentence)
        for title_sentence in title_sentences:
            aggregate_sentence_statistics(aggregated_word_counts, aggregated_word_sentiments, title_sentence, 3)

        # Combine both dictionaries, adding values
        #words = defaultdict(int)
        #for k, v in chain(processed_contents.iteritems(), processed_titles.iteritems()):
        #    words[k] += v

        # Sort words
        words_sorted = sorted(aggregated_word_counts.items(), key=lambda x: x[1], reverse=True)

        # Put words that appear enough times in final map
        final = {}
        for word, count in words_sorted[:max_words]:
            if count >= min_word_count:
                final[word] = (count, aggregated_word_sentiments[word])
            else:
                break

        # Update context
        context['affair_count'] = affairs.count()
        context['words'] = json.dumps(final)
        #print context['words']

        return context


class Search(ListView):
    context_object_name = 'persons'
    model = models.Person
    template_name = 'search_results.html'

    def get_queryset(self):
        self.q = filter(lambda c: c.isalnum(), self.request.GET.get('q', u''))
        if self.q:
            return self.model.objects.filter(
                Q(name__icontains=self.q) | Q(party__short_name__istartswith=self.q)
            )
        return None

    def get_context_data(self, **kwargs):
        context = super(Search, self).get_context_data(**kwargs)
        context['q'] = self.q
        return context
