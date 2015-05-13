from djwkhtmltopdf import convert_html_to_pdf


def home(request):
    response = convert_html_to_pdf(request=request, context={'page':20, 'name': 'Anvesh'})
    return response


def test(request):
    response = convert_html_to_pdf(request=request,name=123, context={'page':20})

    return response

