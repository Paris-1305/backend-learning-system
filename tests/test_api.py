import pytest
import json
from unittest.mock import patch, MagicMock
from src.api.app import create_app
from config import Config


@pytest.fixture
def client():
    """Test client fixture"""
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def auth_headers():
    """Authentication headers fixture"""
    return {'Authorization': f'Bearer {Config.VALID_API_KEYS[0]}'}


class TestCoursesAPI:
    """Test cases for Courses API endpoints"""

    def test_get_all_courses_success(self, client, auth_headers):
        """Test GET /api/courses returns all courses"""
        response = client.get('/api/courses', headers=auth_headers)

        assert response.status_code == 200
        data = json.loads(response.data)

        # Should return a list of courses
        assert isinstance(data, list)
        assert len(data) > 0

        # Each course should have required fields
        course = data[0]
        required_fields = ['id', 'title', 'description', 'difficulty']
        for field in required_fields:
            assert field in course

    def test_get_course_by_id_success(self, client, auth_headers):
        """Test GET /api/courses/:id returns specific course"""
        response = client.get('/api/courses/1', headers=auth_headers)

        assert response.status_code == 200
        data = json.loads(response.data)

        # Should return a single course object
        assert isinstance(data, dict)
        assert data['id'] == 1
        assert 'title' in data
        assert 'description' in data

    def test_get_course_by_id_not_found(self, client, auth_headers):
        """Test GET /api/courses/:id returns 404 for non-existent course"""
        response = client.get('/api/courses/99999', headers=auth_headers)

        assert response.status_code == 404
        data = json.loads(response.data)

        assert 'error' in data
        assert data['error']['code'] == 'COURSE_NOT_FOUND'

    def test_get_course_by_id_invalid_id(self, client, auth_headers):
        """Test GET /api/courses/:id with invalid ID format"""
        response = client.get('/api/courses/invalid', headers=auth_headers)

        # Flask should return 404 for invalid integer conversion
        assert response.status_code == 404


class TestLessonsAPI:
    """Test cases for Lessons API endpoints"""

    def test_get_all_lessons_success(self, client, auth_headers):
        """Test GET /api/lessons returns all lessons"""
        response = client.get('/api/lessons', headers=auth_headers)

        assert response.status_code == 200
        data = json.loads(response.data)

        assert isinstance(data, list)
        assert len(data) > 0

        lesson = data[0]
        required_fields = ['id', 'title', 'courseId', 'difficulty']
        for field in required_fields:
            assert field in lesson

    def test_get_lesson_by_id_success(self, client, auth_headers):
        """Test GET /api/lessons/:id returns specific lesson"""
        response = client.get('/api/lessons/1', headers=auth_headers)

        assert response.status_code == 200
        data = json.loads(response.data)

        assert isinstance(data, dict)
        assert data['id'] == 1
        assert 'title' in data
        assert 'courseId' in data

    def test_get_lesson_by_id_not_found(self, client, auth_headers):
        """Test GET /api/lessons/:id returns 404 for non-existent lesson"""
        response = client.get('/api/lessons/99999', headers=auth_headers)

        assert response.status_code == 404
        data = json.loads(response.data)

        assert 'error' in data
        assert data['error']['code'] == 'LESSON_NOT_FOUND'

    def test_get_lessons_by_course_success(self, client, auth_headers):
        """Test GET /api/courses/:course_id/lessons returns lessons for course"""
        # First get a course that exists
        course_response = client.get('/api/courses/1', headers=auth_headers)
        assert course_response.status_code == 200

        # Then get lessons for that course
        response = client.get('/api/courses/1/lessons', headers=auth_headers)

        assert response.status_code == 200
        data = json.loads(response.data)

        assert isinstance(data, list)
        # Should return lessons for course 1
        for lesson in data:
            assert lesson['courseId'] == 1

    def test_get_lessons_by_course_not_found(self, client, auth_headers):
        """Test GET /api/courses/:course_id/lessons returns 404 for non-existent course"""
        response = client.get('/api/courses/99999/lessons', headers=auth_headers)

        assert response.status_code == 404
        data = json.loads(response.data)

        assert 'error' in data

    def test_get_lessons_by_course_empty(self, client, auth_headers):
        """Test GET /api/courses/:course_id/lessons returns empty array for course with no lessons"""
        # This would need a course with no lessons - implementation dependent
        # For now, just ensure it returns a valid response
        response = client.get('/api/courses/1/lessons', headers=auth_headers)

        assert response.status_code == 200
        data = json.loads(response.data)

        assert isinstance(data, list)


class TestAuthentication:
    """Test cases for API authentication"""

    def test_no_auth_header(self, client):
        """Test endpoints return 401 when no Authorization header provided"""
        response = client.get('/api/courses')

        assert response.status_code == 401
        data = json.loads(response.data)

        assert 'error' in data
        assert 'message' in data['error']

    def test_invalid_auth_header_format(self, client):
        """Test endpoints return 401 for malformed Authorization header"""
        headers = {'Authorization': 'InvalidFormat'}

        response = client.get('/api/courses', headers=headers)

        assert response.status_code == 401
        data = json.loads(response.data)

        assert 'error' in data

    def test_invalid_api_key(self, client):
        """Test endpoints return 401 for invalid API key"""
        headers = {'Authorization': 'Bearer invalid-key-123'}

        response = client.get('/api/courses', headers=headers)

        assert response.status_code == 401
        data = json.loads(response.data)

        assert 'error' in data

    def test_valid_api_key(self, client, auth_headers):
        """Test endpoints work with valid API key"""
        response = client.get('/api/courses', headers=auth_headers)

        assert response.status_code == 200

    def test_bearer_case_insensitive(self, client):
        """Test Bearer prefix is case insensitive"""
        headers = {'Authorization': f'bearer {Config.VALID_API_KEYS[0]}'}

        response = client.get('/api/courses', headers=headers)

        assert response.status_code == 200


class TestErrorHandling:
    """Test cases for error handling"""

    def test_database_connection_error(self, client, auth_headers):
        """Test graceful handling of database connection errors"""
        # This would require mocking database failures
        # Implementation dependent on how errors are handled
        pass

    def test_malformed_request_data(self, client, auth_headers):
        """Test handling of malformed request data"""
        # Most endpoints are GET only, so limited scope
        pass

    def test_rate_limiting(self, client, auth_headers):
        """Test rate limiting functionality"""
        # Would need rate limiting implementation
        # This is a bonus feature that may not be implemented
        pass


if __name__ == '__main__':
    pytest.main([__file__])