from .models import Category
# In Django, context processors are functions that provide additional context data to templates. 
# They are used to make certain variables globally available in all templates without explicitly passing them in each view.

def category_links(request):
    links = Category.objects.all()
    return dict(links = links) # return the links as dictionary