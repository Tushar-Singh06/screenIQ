from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import Application
from .serializers import (
    ScreenCandidateSerializer,
    ApplicationSerializer
)
from .services import AIService
from .pagination import ApplicationPagination


class ScreenCandidateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = ScreenCandidateSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data

        try:
            ai_result = AIService.screen_candidate(
                job_description=data['job_description'],
                resume=data['resume']
            )

            application = Application.objects.create(
                candidate_name=data['candidate_name'],
                job_description=data['job_description'],
                resume=data['resume'],
                ai_score=ai_result['score'],
                ai_reasons=ai_result['reasons'],
                created_by=request.user
            )

            return Response(
                ApplicationSerializer(application).data,
                status=status.HTTP_201_CREATED
            )

        except Exception as e:
            return Response(
                {
                    "error": str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ApplicationListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        applications = Application.objects.filter(
            created_by=request.user
        ).order_by('-created_at')

        paginator = ApplicationPagination()

        paginated_queryset = paginator.paginate_queryset(
            applications,
            request
        )

        serializer = ApplicationSerializer(
            paginated_queryset,
            many=True
        )

        return paginator.get_paginated_response(
            serializer.data
        )


class ApplicationDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):

        try:
            application = Application.objects.get(
                pk=pk,
                created_by=request.user
            )

            serializer = ApplicationSerializer(application)

            return Response(serializer.data)

        except Application.DoesNotExist:
            return Response(
                {
                    "error": "Application not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )