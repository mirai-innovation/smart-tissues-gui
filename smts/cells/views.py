from django.shortcuts import render
from django.http import HttpResponse
import csv

filename = "smts\static\database.csv" ##database file
# Create your views here.
biocell = "Human-adipose tissue derived Mesenchymal Stem Cells"

def home(request ,*args, **kwargs):
    celist = readcells(biocell)
    celopc = cellsnames()
    print(args,kwargs)
    print(request.user)
    if request.method == 'POST':
        variable_value = request.POST.get('datalist_value', '')
        celist = readcells(variable_value)
        return render(request, "home.html" ,{'celist': celist, 'celop':celopc})
    return render(request, "home.html" ,{'celist': celist, 'celop':celopc})

def readcells(biocell):
    results = []
    with open(filename, 'r', encoding='cp932', errors='ignore') as csvfile:
        reader = csv.reader(csvfile ) # change contents to floattissiues
        results.append(next(reader))
        results.append(next(reader))
        results.append(next(reader))
        for row in reader: #each row is a list
            if row[15] == (biocell):
                results.append(row)
                    ##print(row)
    return results

def cellsnames():
    cells =[]
    cellsort= []
    with open(filename, 'r', encoding='cp932', errors='ignore') as csvfile:
        rd = csv.reader(csvfile ) # change contents to floattissiues
        for row in rd: # each row is a list
            cells.append(row[15])
        cells=set(cells)   #delete all the repetitive elements
        cellsort = sorted(cells) 
    return cellsort
