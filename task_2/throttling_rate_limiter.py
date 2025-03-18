import time
from typing import Dict


class ThrottlingRateLimiter:
    def __init__(self, min_interval: float = 10.0):
        self.min_interval = min_interval
        self.last_message_time: Dict[str, float] = {}

    def can_send_message(self, user_id: str) -> bool:
        """Перевіряє, чи може користувач відправити повідомлення."""
        last_time = self.last_message_time.get(user_id, 0)
        return (time.time() - last_time) >= self.min_interval

    def record_message(self, user_id: str) -> bool:
        """Записує час відправки повідомлення, якщо можливо."""
        if self.can_send_message(user_id):
            self.last_message_time[user_id] = time.time()
            return True
        return False

    def time_until_next_allowed(self, user_id: str) -> float:
        """Розраховує час до можливості відправлення наступного повідомлення."""
        last_time = self.last_message_time.get(user_id, 0)
        elapsed_time = time.time() - last_time
        return max(0, self.min_interval - elapsed_time)
