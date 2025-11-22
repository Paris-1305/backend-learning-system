from flask import Blueprint, jsonify
from ...infrastructure.repositories.sqlite_course_repository import SQLiteCourseRepository
from ...application.use_cases.get_course_by_id import GetCourseById
from ...application.use_cases.get_all_courses import GetAllCourses
from ..middleware.auth_middleware import require_api_key
from flask import request

course_bp = Blueprint('course', __name__)

# Initialize dependencies
course_repository = SQLiteCourseRepository()
get_all_courses = GetAllCourses(course_repository)
get_course_by_id = GetCourseById(course_repository)


@course_bp.route('/courses', methods=['GET'])
@require_api_key
def get_courses():
    """Get all courses"""
    courses = get_all_courses.execute()
    return jsonify(courses)


@course_bp.route('/courses/<int:course_id>', methods=['GET'])
@require_api_key
def get_course(course_id):
    """Get a specific course by ID"""
    course = get_course_by_id.execute(course_id)
    if course is None:
        return jsonify({
            'error': {
                'code': 'COURSE_NOT_FOUND',
                'message': 'The requested course does not exist'
            }
        }), 404

    return jsonify(course)

@course_bp.route("/courses", methods=["POST"])
@require_api_key
def create_course():
    print("POST /api/courses route is active")  # debug
    data = request.json
    course = course_repository.create(data)
    return jsonify(course.to_dict()), 201


# PUT /api/courses/<course_id>
@course_bp.route("/courses/<int:course_id>", methods=["PUT"])
@require_api_key
def update_course(course_id):
    data = request.json
    course = course_repository.update(course_id, data)
    if course is None:
        return jsonify({"error": "Course not found"}), 404
    return jsonify(course.to_dict()), 200


# DELETE /api/courses/<course_id>
@course_bp.route("/courses/<int:course_id>", methods=["DELETE"])
@require_api_key
def delete_course(course_id):
    success = course_repository.delete(course_id)
    if not success:
        return jsonify({"error": "Course not found"}), 404
    return jsonify({"message": f"Course {course_id} deleted successfully"}), 200