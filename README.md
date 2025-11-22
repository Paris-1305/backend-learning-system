# 🐍 Backend Challenge: Help Barry Build His API!

## Barry's Backend Story
Barry has been learning Flask and wants to build a robust API for his learning platform. He's set up the basic structure with clean architecture, but the API is missing some crucial pieces. Help Barry implement the missing endpoints and authentication so his frontend can finally connect to real data!

## 🎯 Your Backend Mission
Complete Barry's Flask API by implementing two key missing pieces:

### Task 1: The Missing Lessons Endpoint
Barry needs an endpoint to get all lessons for a specific course. The route is already set up, but the implementation is missing.

**What to implement:**
- Route: `GET /api/courses/{course_id}/lessons`
- Use the existing `SQLiteLessonRepository.get_by_course_id()` method
- Return proper JSON response with lessons data
- Handle cases where course doesn't exist (404 error)
- Handle cases where course exists but has no lessons (empty array)

### Task 2: API Key Authentication
Barry's API needs proper authentication. The middleware decorator exists but isn't implemented.

**What to implement:**
- Check for `Authorization` header with `Bearer YOUR_API_KEY` format
- Validate the API key against `Config.VALID_API_KEYS`
- Return proper error responses for missing/invalid keys
- Allow requests to proceed when authentication passes

## 🏗️ Architecture Overview
Barry has organized his code following clean architecture principles:

```
backend/src/
├── api/                    # Flask routes and middleware
├── application/           # Use cases and business logic
├── domain/               # Entities and business rules
└── infrastructure/       # Database and external concerns
```

## 🚀 Getting Started
```bash
cd backend
pip install -r requirements.txt
python run.py
```

## 📋 Implementation Checklist

### Task 1: Lessons by Course
- [ ] Complete `get_lessons_by_course` function in `lesson_routes.py`
- [ ] Use existing repository method
- [ ] Return proper JSON format
- [ ] Handle 404 for non-existent courses
- [ ] Handle empty lesson arrays

### Task 2: Authentication Middleware
- [ ] Complete `require_api_key` decorator in `auth_middleware.py`
- [ ] Extract Authorization header
- [ ] Validate "Bearer " prefix
- [ ] Check API key validity
- [ ] Return appropriate error responses

## 🧪 Testing Your Implementation

### Manual Testing
- Use the test API key: `test-api-key-12345`
- Access Swagger docs at: `http://localhost:5000/docs`
- Test all endpoints with proper authentication headers

### Automated Testing
Run the comprehensive test suite to verify your implementation:

```bash
cd backend
python -m pytest tests/ -v
```

**Test Coverage Requirements:**
- ✅ All 4 API endpoints functional
- ✅ Authentication middleware working
- ✅ Error handling for invalid inputs
- ✅ Proper HTTP status codes
- ✅ JSON response formats match specifications

**Key Test Cases:**
- Course CRUD operations (GET all, GET by ID)
- Lesson retrieval (GET all, GET by ID, GET by course)
- Authentication validation (valid/invalid keys, missing headers)
- Error responses (404s, 401s for invalid requests)
- Data integrity (course-lesson relationships)

## 💡 Pro Tips
- The database is pre-populated with 50 courses and ~400 lessons
- All existing endpoints work without authentication for testing
- Focus on clean, readable code that follows the existing patterns
- Test edge cases like invalid course IDs and missing auth headers

## 🎉 Help Barry Ship His API!
By completing these tasks, you're helping Barry take a big step toward his web development dreams. Show him how to build production-ready APIs with proper authentication and error handling!

**Remember:** Barry's counting on you to make his API production-ready! 🚀