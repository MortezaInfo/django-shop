from home.models import Products

def advanced_filter(request, products):
    order_by = request.GET.get('sort_by')
    name = request.GET.get('name')
    min_star = request.GET.get('min_star')
    max_star = request.GET.get('max_star')
    description = request.GET.get('description')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    category = request.GET.get('category')

    if order_by == '1':
            products = products.order_by('-created')

    elif order_by == '2': 
        products = products.order_by('vote', 'star')

    elif order_by == '4':
        products = products.order_by('-discount')

    elif order_by == '5':
        pass


    if name:
        products = products.filter(name = name)

    if min_star:
        products = products.filter(star__gte=min_star)
        
    if max_star:
        products = products.filter(star__lte=max_star)

    if description:
        products = products.filter(description = description)

    if min_price:
        products = products.filter(price__gte=min_price)

    if max_price:
        products = products.filter(price__lte=max_price)

    if category:
        products = products.filter(category__name = category)    

    return products