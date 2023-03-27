from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from tracker.models import RoadCrack, PoliceBump
from tracker.paginations import SimplePagination
from tracker.serializers import RoadCrackSerializer, PoliceBumpSerializer


class RoadCrackListAPIView(ListAPIView):
    serializer_class = RoadCrackSerializer
    pagination_class = SimplePagination
    queryset = RoadCrack.objects.filter(approved=True)
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        location = request.data.get('location')
        address = request.data.get('address')
        city = request.data.get('city')
        danger_level = request.data.get('danger_level')

        distance_threshold = 1
        existing_crack = RoadCrack.objects.filter(location__distance_lte=(location, distance_threshold)).first()
        if existing_crack:
            if existing_crack.requested_amount >= 3:
                existing_crack.approved = True
            else:
                existing_crack.requested_amount += 1
            existing_crack.save()

            serializer = RoadCrackSerializer(existing_crack)
            return Response(serializer.data)

        new_crack = RoadCrack.objects.create(
            location=location,
            address=address,
            city=city,
            danger_level=danger_level
        )
        serializer = RoadCrackSerializer(new_crack)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class PoliceBumpListAPIView(ListAPIView):
    serializer_class = PoliceBumpSerializer
    pagination_class = SimplePagination
    queryset = PoliceBump.objects.all()
    permission_classes = [IsAuthenticated]
