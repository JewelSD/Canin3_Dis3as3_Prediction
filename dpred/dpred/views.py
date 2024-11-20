from django.shortcuts import render
from django.http import HttpResponse


def print_hell(request):
    movie_data={
        'movies':[
            {
        'title':'godha',
        'year':'2000',
        'summary':'fighter',
        'rate':True
    },
    {
        'title':'god',
        'year':'2001',
        'summary':'normar',
        'rate':False
    }
        ]
    }
    return render(request, "hello.html",movie_data)
