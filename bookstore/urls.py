"""
URL configuration for bookstore project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

import debug_toolbar  # Importação do debug_toolbar para fornecer informações de depuração
from django.conf import settings
from django.contrib import admin
from django.urls import path, re_path, include
from rest_framework.authtoken.views import obtain_auth_token
from django.http import HttpResponse

def health_check(request):
    return HttpResponse("API Running", status=200)

# Definição das rotas (URLs) para a aplicação
urlpatterns = [
    path("admin/", admin.site.urls),  # Rota para o painel administrativo do Django
    # Inclui URLs dos aplicativos "order" e "product" com suporte para versões v1 e v2
    re_path(r"bookstore/(?P<version>(v1|v2))/", include("order.urls")),  
    re_path(r"bookstore/(?P<version>(v1|v2))/", include("product.urls")),
    # Rota para autenticação de token usando Django Rest Framework
    path("api-token-auth/", obtain_auth_token, name="api_token_auth"),
    path('', health_check),  # Ponto de verificação básico
]


# Adicionando URLs do debug_toolbar se o modo DEBUG estiver ativado
if settings.DEBUG:
    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),  # Rota para acessar o Django Debug Toolbar
    ]
