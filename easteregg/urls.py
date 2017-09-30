from django.conf.urls import include, url

from django.contrib import admin
admin.autodiscover()

import egghunt.views

# Examples:
# url(r'^$', 'easteregg.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),

urlpatterns = [
    url(r'^$', egghunt.views.top_index, name='index'),
    url(r'^egghunt/', include('egghunt.urls')),
    url(r'^admin/', include(admin.site.urls)),
]
