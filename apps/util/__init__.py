from django.contrib.sites.models import Site

def url_with_domain(path):
    domain = Site.objects.get_current().domain
    return u'{}{}'.format(domain, path)
