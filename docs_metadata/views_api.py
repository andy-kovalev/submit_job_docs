from django.db.models import ProtectedError
from django.http import Http404
from rest_framework import views, viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from docs_metadata.models import Command, CompanyWelcome, Document, Action, ParseMode
from docs_metadata.serializers import CommandSerializer, CompanyWelcomeSerializer, DocumentSerializer


def enum_to_json(enum_class):
    return {f'{enum_class.__name__}': [enum[0] for enum in enum_class.__members__.items()]}


class ActionView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(enum_to_json(Action))


class ParseModeView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(enum_to_json(ParseMode))


class BaseViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        try:
            return super().destroy(request, *args, **kwargs)
        except ProtectedError as protected_error:
            protected_elements = [{"id": protected_object.pk, "used_by": str(protected_object)} for protected_object in
                                  protected_error.protected_objects]
            response_data = {"non_deletion_reason": protected_elements}
            return Response(data=response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CommandViewSet(BaseViewSet):
    permission_classes = [IsAuthenticated]

    queryset = Command.objects.all()
    serializer_class = CommandSerializer


class CompanyWelcomeViewSet(BaseViewSet):
    permission_classes = [IsAuthenticated]

    queryset = CompanyWelcome.objects.all()
    serializer_class = CompanyWelcomeSerializer

    def get_object(self):
        """
        Returns the object the view is displaying.

        Override, objects no using arguments in the url conf.
        """
        obj = CompanyWelcome.objects.first()

        if obj is None:
            raise Http404

        # May raise a permission denied
        self.check_object_permissions(self.request, obj)

        return obj


class DocumentViewSet(BaseViewSet):
    permission_classes = [IsAuthenticated]

    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
