from flask import Blueprint, request, jsonify
from extensions import db
import models
from schemas import TaskSchema
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

bp = Blueprint('tasks', __name__, url_prefix='/tasks')

task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)

@bp.route('', methods=['GET'])
def list_tasks():
    """
        Get all tasks
        ---
        tags:
          - Tasks
        parameters:
          - name: page
            in: query
            type: integer
            description: Page number
          - name: per_page
            in: query
            type: integer
            description: Items per page
          - name: completed
            in: query
            type: boolean
            description: Filter by completion status
        responses:
          200:
            description: A paginated list of tasks
        """
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))
    completed = request.args.get('completed')
    query = models.Task.query
    if completed is not None:
        if completed.lower() in ('true', '1'):
            query = query.filter_by(completed=True)
        elif completed.lower() in ('false', '0'):
            query = query.filter_by(completed=False)
    pag = query.order_by(models.Task.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)
    return jsonify({'items': tasks_schema.dump(pag.items),'page': pag.page,'per_page': pag.per_page,'total': pag.total,'pages': pag.pages})

@bp.route('/<int:id>', methods=['GET'])
def get_task(id):
    """
        Get a single task by ID
        ---
        tags:
          - Tasks
        parameters:
          - name: id
            in: path
            required: true
            type: integer
            description: Task ID
        responses:
          200:
            description: Task details
          404:
            description: Task not found
        """
    task = models.Task.query.get_or_404(id)
    return jsonify(task_schema.dump(task)), 201

@bp.route('', methods=['POST'])
@jwt_required()
def create_task():
    """
        Create a new task
        ---
        tags:
          - Tasks
        security:
          - Bearer: []
        consumes:
          - application/json
        parameters:
          - in: body
            name: body
            required: true
            schema:
              type: object
              required:
                - title
              properties:
                title:
                  type: string
                description:
                  type: string
                completed:
                  type: boolean
        responses:
          201:
            description: Task created successfully
          400:
            description: Validation error
          401:
            description: Unauthorized (missing/invalid token)
        """
    data = request.get_json() or {}
    errors = task_schema.validate(data, session=db.session)  # <-- pass session here
    if errors:
        return jsonify(errors), 400

    user_id = int(get_jwt_identity())
    task = models.Task(
        title=data.get('title'),
        description=data.get('description'),
        completed=data.get('completed', False),
        user_id=user_id
    )
    db.session.add(task)
    db.session.commit()
    return jsonify(task_schema.dump(task)), 201

@bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_task(id):
    """
        Update an existing task
        ---
        tags:
          - Tasks
        security:
          - Bearer: []
        parameters:
          - name: id
            in: path
            required: true
            type: integer
            description: Task ID
          - in: body
            name: body
            schema:
              type: object
              properties:
                title:
                  type: string
                description:
                  type: string
                completed:
                  type: boolean
        responses:
          200:
            description: Task updated successfully
          403:
            description: Forbidden — not your task
          404:
            description: Task not found
        """
    task = models.Task.query.get_or_404(id)
    user_id = int(get_jwt_identity())
    role = get_jwt().get('role', 'user')  # get role from additional_claims
    if task.user_id != user_id and role != 'admin':
        return jsonify({'msg': 'forbidden'}), 403

    data = request.get_json() or {}
    task.title = data.get('title', task.title)
    task.description = data.get('description', task.description)
    if 'completed' in data:
        task.completed = data['completed']
    db.session.commit()
    return jsonify(task_schema.dump(task)), 201

@bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_task(id):
    """
        Delete a task
        ---
        tags:
          - Tasks
        security:
          - Bearer: []
        parameters:
          - name: id
            in: path
            required: true
            type: integer
            description: Task ID
        responses:
          204:
            description: Task deleted successfully
          403:
            description: Forbidden — not your task
          404:
            description: Task not found
        """
    task = models.Task.query.get_or_404(id)
    user_id = int(get_jwt_identity())
    role = get_jwt().get('role', 'user')
    if task.user_id != user_id and role != 'admin':
        return jsonify({'msg': 'forbidden'}), 403

    db.session.delete(task)
    db.session.commit()
    # return '', 204
    return jsonify({'msg': 'Successfully Deleted'}), 201

