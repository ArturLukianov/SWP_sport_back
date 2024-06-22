from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from api.serializers.student import BatchStudentUpdateSerializer
from api.crud import update_students
from api.permissions import IsStaff


@api_view(["PUT"])
@permission_classes([IsStaff])
def batch_update_students(request):
    """
    Updates multiple students at once.
    """
    serializer = BatchStudentUpdateSerializer(data=request.data,
                                              partial=True)

    if serializer.is_valid(raise_exception=True):
        students = update_students(serializer.validated_data['students'])
        return Response({"message": "Students updated successfully",
                         "students": students}, status=status.HTTP_200_OK)
