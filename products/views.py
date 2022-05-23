import csv
import json
import itertools
from products.models import Products
from django.template import loader
from django.http import HttpResponse, JsonResponse
from .popularity import popularity_based_recommendation
from .collaborative import model_based_recommendation
from .hybrid import hybrid_based_recommendation
from .knn import knn_based_recommendation

def get_products(request):
    products_list = Products.objects.all()[:50]
    print(products_list)
    template = loader.get_template('products/index.html')
    context = {
        'products_list': products_list,
    }
    return HttpResponse(template.render(context, request))

def popularity_based(request):
    df = popularity_based_recommendation()

    json_records = df.reset_index().to_json(orient ='records')
    recommendation_list = []
    recommendation_list = json.loads(json_records)

    template = loader.get_template('products/popularity.html')
    context = {
        'recommendation_list': recommendation_list
    }
    return HttpResponse(template.render(context, request))

def model_based(request):
    df = model_based_recommendation()

    json_records = df.reset_index().to_json(orient ='records')
    recommendation_list = []
    recommendation_list = json.loads(json_records)

    template = loader.get_template('products/collaborative.html')
    context = {
        'recommendation_list': recommendation_list
    }
    return HttpResponse(template.render(context, request))
    
def hybrid_based(request):
    df = hybrid_based_recommendation()

    json_records = df.reset_index().to_json(orient ='records')
    recommendation_list = []
    recommendation_list = json.loads(json_records)

    template = loader.get_template('products/hybrid.html')
    context = {
        'recommendation_list': recommendation_list
    }
    return HttpResponse(template.render(context, request))

def knn_based(request):
    df = knn_based_recommendation()

    json_records = df.reset_index().to_json(orient ='records')
    recommendation_list = []
    recommendation_list = json.loads(json_records)

    template = loader.get_template('products/knn.html')
    context = {
        'recommendation_list': recommendation_list
    }
    return HttpResponse(template.render(context, request))