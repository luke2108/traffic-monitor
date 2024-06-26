from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from django.core.exceptions import ValidationError
from django.db.models import Q

from .models import UserError
from .serializers import UserErrorSerializer

class UserErrorViewSet(viewsets.ModelViewSet):
    serializer_class = UserErrorSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = UserError.objects.all()
        return queryset
    
    def create(self, request, *args, **kwargs):
        domain = request.data.get('domain')
        status = request.data.get('status')
        ip_address = self.get_client_ip(request)
        user_agent = request.META['HTTP_USER_AGENT']


        user_error = UserError(
            ip_user=ip_address,
            user_agent=user_agent,
            domain=domain,
            status=status,
        )
        user_error.save()
        return Response(status=201)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
