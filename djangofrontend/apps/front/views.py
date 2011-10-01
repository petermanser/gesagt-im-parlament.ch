import json
from django.http import HttpResponse
from django.shortcuts import render_to_response
from apps.front import models
from apps.front.stopwords import stopwords


def persons(request):
    persons = models.Person.objects.all()
    context = {
        'persons': persons,
    }
    return render_to_response('persons.html', context)


def tagcloud(request, id):
    # Minimum of times a word must appear to be in the final list
    min_word_count = 3
    max_words = 30

    person = models.Person.objects.get(pk=id)    
    affairs = person.affair_set.all()

    # Get all content words
    contents = [a.content.split(' ') for a in affairs]
    # Flatten "list in list"
    words = sum(contents, [])  
    # Strip all non-letters and convert to lowercase
    words_clean = map(lambda x: filter(lambda y: y.isalpha(), x).lower(), words)
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

    # Get photo
    context = {
        'affair_count': affairs.count(),
        'words': json.dumps(final),
        'person': person,
    }
    return render_to_response('tagcloud.html', context)
