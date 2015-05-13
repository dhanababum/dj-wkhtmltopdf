from djwkhtmltopdf.utils import convert_html_to_pdf


def example_view(request):
    """
    This example view for testing don't use in your project
    it takes to params 'name' and number
    name is for pdf name if didn't pass the name it takes dynamic name from
    DATABASE. number is simple context variable for displying page number
    """
    if 'name' in request.GET:
        response = convert_html_to_pdf(
            request=request,
            name=request.GET.get('name', None),
            context={'page': 20})
    else:
        num = request.GET.get('number', 20)
        response = convert_html_to_pdf(request=request, context={'page': num})
    return response
