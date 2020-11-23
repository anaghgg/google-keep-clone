import pytest

from django.urls import reverse
from .models import Note
from rest_framework.test import APIClient


@pytest.fixture
def api_client():
   return APIClient()

@pytest.mark.django_db
def test_add_note(api_client, django_user_model):
    user = django_user_model.objects.create_user(email='user1@user.com', password='user')
    api_client.force_login(user)

    # Add a note for this user  
    url = reverse('api:addnote')
    response = api_client.post(url, {'title': 'Test', 'text': 'Text'})
    assert response.status_code == 201

    # Add another user for next note
    user2 =  django_user_model.objects.create_user(email='a@b.com', password='abc')
    note2 = Note.objects.create(title='a',text='b',author=user2)
    
    # Only one note should be visible to the current user
    url = reverse('api:noteslist')
    response = api_client.get(url)
    assert len(response.json()) == 1


@pytest.mark.django_db
def test_note_delete(api_client, django_user_model):
    user1 = django_user_model.objects.create_user(email='user1@user.com', password='user')
    api_client.force_login(user1)  
    url = reverse('api:addnote')
    note1 = Note.objects.create(title='note1',text='note1text',author=user1)

    # Add another user for next note
    user2 =  django_user_model.objects.create_user(email='user2@user.com', password='user')
    note2 = Note.objects.create(title='note2',text='note2text',author=user2)

    # Delete first note
    url = reverse('api:editnote', kwargs={'pk': note1.id})
    response = api_client.delete(url)
    assert response.status_code == 204

    assert Note.objects.filter(pk=note1.id).exists() is False

    # Should not be able to delete note2
    url = reverse('api:editnote', kwargs={'pk': note2.id})
    response = api_client.delete(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_note_update(api_client, django_user_model):
    user1 = django_user_model.objects.create_user(email='user1@user.com', password='user')
    api_client.force_login(user1)  
    note1 = Note.objects.create(title='note1',text='note1text',author=user1)
    url = reverse('api:editnote', kwargs={'pk': note1.id})

    response = api_client.put(url, {'title': 'Test', 'text': 'Text'})
    assert response.status_code == 204
    get_updated_note = Note.objects.get(pk=note1.id)
    assert get_updated_note.title == 'Test'
    assert get_updated_note.text == 'Text'
    
    # Add another user for next note
    user2 =  django_user_model.objects.create_user(email='user2@user.com', password='user')
    note2 = Note.objects.create(title='note2',text='note2text',author=user2)

    # Should not be able to delete note2
    url = reverse('api:editnote', kwargs={'pk': note2.id})
    response = api_client.put(url, {'title': 'Test', 'text': 'Text'})
    assert response.status_code == 403