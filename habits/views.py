from drf_spectacular.utils import extend_schema
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from habits.models import Habit
from habits.paginations import CustomPagination
from habits.permissions import IsOwnerOrReadOnly
from habits.serializers import HabitSerializer


@extend_schema(
    methods=["GET"],
    summary="Get the list of Habits and public Habits",
    description="Retrieves the list of user's Habits and public Habits.",
    tags=["Habits"],
)
@extend_schema(
    methods=["POST"],
    summary="Create a new Habit",
    description="Creates a new Habit owned by the current user.",
    tags=["Habits"],
)
class HabitList(generics.ListCreateAPIView):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        user_habits = Habit.objects.filter(user=self.request.user)

        public_habits = Habit.objects.filter(is_public=True)

        return user_habits | public_habits

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(user=self.request.user)


@extend_schema(tags=["Habits"])
class HabitDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            user_habits = Habit.objects.filter(user=self.request.user)
        else:
            user_habits = Habit.objects.none()

        public_habits = Habit.objects.filter(is_public=True)
        return user_habits | public_habits

    @extend_schema(
        summary="Get the details of a Habit",
        description="Retrieves the details of a particular Habit.",
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        summary="Update a Habit",
        description="Updates the details of a particular Habit.",
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @extend_schema(
        summary="Partially update a Habit",
        description="Partially updates the details of a particular Habit.",
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @extend_schema(
        summary="Delete a Habit",
        description="This operation deletes a particular Habit.",
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
