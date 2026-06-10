# app/routes.py
# Routes connect URLs to functions.
# When someone visits /todos, Flask runs the matching function below.

from flask import Blueprint, jsonify, request
from app import models

bp = Blueprint("todos", __name__)


@bp.route("/todos", methods=["GET"])
def list_todos():
    """GET /todos — return all todos as JSON."""
    return jsonify(models.get_all()), 200


@bp.route("/todos", methods=["POST"])
def create_todo():
    """POST /todos — create a new todo.
    Expects JSON body: { "title": "Buy milk" }
    """
    data = request.get_json()
    if not data or "title" not in data:
        return jsonify({"error": "title is required"}), 400

    todo = models.create(data["title"])
    return jsonify(todo), 201   # 201 = Created


@bp.route("/todos/<int:todo_id>", methods=["PATCH"])
def update_todo(todo_id):
    """PATCH /todos/1 — mark a todo done or undone.
    Expects JSON body: { "done": true }
    """
    data = request.get_json()
    todo = models.update(todo_id, data.get("done", False))
    if not todo:
        return jsonify({"error": "not found"}), 404
    return jsonify(todo), 200


@bp.route("/todos/<int:todo_id>", methods=["DELETE"])
def delete_todo(todo_id):
    """DELETE /todos/1 — delete a todo."""
    deleted = models.delete(todo_id)
    if not deleted:
        return jsonify({"error": "not found"}), 404
    return jsonify({"message": "deleted"}), 200


@bp.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok",
        "version": "v3",
        "message": "CI/CD pipeline working! 🚀"
    }), 200