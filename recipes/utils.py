def get_ingredient(request):
    ingredients = {}
    for key, value in request.POST.items():
        if key.startswith('nameIngredient'):
            number = key.split('_')[1]
            ingredients[value] = request.POST.get(f'valueIngredient_{number}')
    return ingredients
