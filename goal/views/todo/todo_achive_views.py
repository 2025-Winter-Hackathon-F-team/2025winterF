import logging
import json

from django.views.generic import UpdateView
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin

from goal.models.todo import Todos

logger = logging.getLogger(__name__)

class TodoAchieveView(LoginRequiredMixin, UpdateView):
    model = Todos

    def get_object(self, todo_id):
        """
        更新対象のTodoを取得する
        Returns:
            Todo: 指定されたTodoが存在すれば Todos インスタンスを返す
        """

        # 指定されたTodoを取得
        todo = Todos.get_todo(todo_id=todo_id)
        if not todo:
            logger.warning(f"[MonthGoal] Not found: todo_id={todo_id}")
            return None

        return todo

    def post(self, request, *args, **kwargs):
        """
        Todoを達成状態に更新するAPIエンドポイント
        Args:
            request (HttpRequest): クライアントからのリクエスト
        Returns:
            JsonResponse:
                - 成功時: 更新処理が完了したことを返す (status=200)
                - 失敗時: エラーメッセージを返す (status=400, 404, 500)
        """
        try:
            # リクエストボディをJSONとして読み込む
            data = json.loads(request.body)
        except json.JSONDecodeError:
            logger.warning("[TodoAchieveView] Invalid JSON format in request body")
            return JsonResponse({"error": "Invalid JSON format"}, status=400)

        todo_id = data.get("todo_id")
        if todo_id is None:
            logger.warning("[TodoAchieveView] todo_id is missing in request data")
            return JsonResponse({"error": "todo_id is required"}, status=400)

        todo = self.get_object(todo_id=todo_id)
        if not todo:
            return JsonResponse({"error": "Todo not found."}, status=404)

        try:
            # Todoを達成状態にする
            todo.mark_as_achieved()
            return JsonResponse({"success": "Successfully processed request"}, status=200)
        except Exception as e:
            logger.error(f"[Todo] Error marking todo {todo.id} as achieved: {e}")
            return JsonResponse({"error": "Failed to mark todo as achieved."}, status=500)