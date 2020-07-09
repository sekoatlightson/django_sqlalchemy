from django.shortcuts import render

def index(reques):
    return render(reques, 'rental/rental_list.html')
