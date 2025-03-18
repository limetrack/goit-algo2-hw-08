import time
from collections import deque
from typing import Dict


class SlidingWindowRateLimiter:
    def __init__(self, window_size: int = 10, max_requests: int = 1):
        self.window_size = window_size
        self.max_requests = max_requests
        self.user_requests: Dict[str, deque] = {}

    def _cleanup_window(self, user_id: str, current_time: float) -> None:
        """Видаляє старі запити, які вийшли за межі вікна"""
        if user_id in self.user_requests:
            while (
                self.user_requests[user_id]
                and self.user_requests[user_id][0] <= current_time - self.window_size
            ):
                self.user_requests[user_id].popleft()

            # Якщо вікно очищене - видаляємо користувача
            if not self.user_requests[user_id]:
                del self.user_requests[user_id]

    def can_send_message(self, user_id: str) -> bool:
        """Перевіряє, чи може користувач відправити повідомлення"""
        current_time = time.time()
        self._cleanup_window(user_id, current_time)
        return len(self.user_requests.get(user_id, [])) < self.max_requests

    def record_message(self, user_id: str) -> bool:
        """Реєструє нове повідомлення, якщо це можливо"""
        if self.can_send_message(user_id):
            if user_id not in self.user_requests:
                self.user_requests[user_id] = deque()
            self.user_requests[user_id].append(time.time())
            return True
        return False

    def time_until_next_allowed(self, user_id: str) -> float:
        """Розраховує, скільки залишилося чекати до наступного дозволеного повідомлення"""
        if user_id not in self.user_requests or not self.user_requests[user_id]:
            return 0.0
        current_time = time.time()
        self._cleanup_window(user_id, current_time)
        return max(
            0.0, self.user_requests[user_id][0] + self.window_size - current_time
        )
