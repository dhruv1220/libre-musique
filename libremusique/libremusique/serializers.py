from rest_framework import serializers
from .models import Piece, Collaborator, Recital, Note

class CollaboratorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collaborator
        fields = ['id', 'email', 'first_name', 'last_name', 'instrument']

class RecitalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recital
        fields = ['id', 'date', 'venue', 'time']

class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ['id', 'text']

class PieceSerializer(serializers.ModelSerializer):
    collaborators = CollaboratorSerializer(many=True, required=False)
    recital = RecitalSerializer(many=True, required=False)
    notes = NoteSerializer(many=True, required=False)

    class Meta:
        model = Piece
        fields = ['id', 'name', 'composer', 'date_started', 'key', 'collaborators', 'recital', 'notes']
        extra_kwargs = {'user': {'read_only': True}}

    def create(self, validated_data):
        collaborators_data = validated_data.pop('collaborators', [])
        recitals_data = validated_data.pop('recital', [])
        notes_data = validated_data.pop('notes', [])

        piece = Piece.objects.create(**validated_data)

        for collaborator_data in collaborators_data:
            collaborator, created = Collaborator.objects.get_or_create(**collaborator_data)
            piece.collaborators.add(collaborator)
        
        for recital_data in recitals_data:
            recital, created = Recital.objects.get_or_create(**recital_data)
            piece.recital.add(recital)
        
        for note_data in notes_data:
            Note.objects.create(piece=piece, **note_data)
        
        return piece

    def update(self, instance, validated_data):
        collaborators_data = validated_data.pop('collaborators', [])
        recitals_data = validated_data.pop('recital', [])
        notes_data = validated_data.pop('notes', [])

        # Update the piece instance
        super().update(instance, validated_data)

        # Update collaborators
        instance.collaborators.clear()
        for collaborator_data in collaborators_data:
            collaborator, created = Collaborator.objects.get_or_create(**collaborator_data)
            instance.collaborators.add(collaborator)

        # Update recitals
        instance.recital.clear()
        for recital_data in recitals_data:
            recital, created = Recital.objects.get_or_create(**recital_data)
            instance.recital.add(recital)

        # Update or create notes
        for note_data in notes_data:
            note_id = note_data.get('id')
            if note_id:
                note = Note.objects.get(id=note_id, piece=instance)
                note.text = note_data.get('text', note.text)
                note.save()
            else:
                Note.objects.create(piece=instance, **note_data)
        
        return instance
    
    def delete_nested(self, instance, validated_data):
        # Delete collaborators
        collaborator_ids = [item['id'] for item in validated_data.get('collaborators', []) if 'id' in item]
        instance.collaborators.exclude(id__in=collaborator_ids).delete()

        # Delete recitals
        recital_ids = [item['id'] for item in validated_data.get('recital', []) if 'id' in item]
        instance.recital.exclude(id__in=recital_ids).delete()

        # Delete notes
        note_ids = [item['id'] for item in validated_data.get('notes', []) if 'id' in item]
        instance.notes.exclude(id__in=note_ids).delete()

        return instance
