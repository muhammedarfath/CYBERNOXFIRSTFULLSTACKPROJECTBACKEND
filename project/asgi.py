import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
from socketconnection import routing  
from django_channels_jwt_auth_middleware.auth import JWTAuthMiddlewareStack

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AllowedHostsOriginValidator(  
        JWTAuthMiddlewareStack(  
            URLRouter(
                routing.websocket_urlpatterns
            )
        )
    ),
})
