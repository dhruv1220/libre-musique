from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import Piece, Collaborator, Recital, Note
from .serializers import PieceSerializer, CollaboratorSerializer, RecitalSerializer, NoteSerializer
from .authentication import FirebaseAuthentication
from .permissions import FirebasePermission

class PieceViewSet(viewsets.ModelViewSet):
    queryset = Piece.objects.all()
    serializer_class = PieceSerializer
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [FirebasePermission]

    def perform_create(self, serializer):
        user_instance, created = self.request.user
        serializer.save(user=user_instance)  # Assumes you have user field in Piece model
    
    def get_queryset(self):
        queryset = Piece.objects.all()
        user_id, created = self.request.user
        if user_id is not None:
            queryset = queryset.filter(user=user_id)
            return queryset
        return Piece.objects.none()

class CollaboratorViewSet(viewsets.ModelViewSet):
    queryset = Collaborator.objects.all()
    serializer_class = CollaboratorSerializer
    permission_classes = [permissions.IsAuthenticated]  # Adjust as needed

class RecitalViewSet(viewsets.ModelViewSet):
    queryset = Recital.objects.all()
    serializer_class = RecitalSerializer
    permission_classes = [permissions.IsAuthenticated]  # Adjust as needed

class NoteViewSet(viewsets.ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = [permissions.IsAuthenticated]  # Adjust as needed

    def perform_create(self, serializer):
        piece_id = self.kwargs.get('piece_pk')
        serializer.save(piece_id=piece_id)  # Assumes nested route under Piece
