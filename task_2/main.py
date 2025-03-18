import time
import random

from throttling_rate_limiter import ThrottlingRateLimiter


def test_throttling_limiter():
    limiter = ThrottlingRateLimiter(min_interval=10.0)

    print("\n=== Симуляція потоку повідомлень (Throttling) ===")
    for message_id in range(1, 11):
        user_id = str(message_id % 5 + 1)
        result = limiter.record_message(user_id)
        wait_time = limiter.time_until_next_allowed(user_id)

        print(
            f"Повідомлення {message_id:2d} | Користувач {user_id} | "
            f"{'✓' if result else f'× (очікування {wait_time:.1f}с)'}"
        )

        # Випадкова затримка між повідомленнями
        time.sleep(random.uniform(0.1, 1.0))

    print("\nОчікуємо 10 секунд...")
    time.sleep(10)

    print("\n=== Нова серія повідомлень після очікування ===")
    for message_id in range(11, 21):
        user_id = str(message_id % 5 + 1)
        result = limiter.record_message(user_id)
        wait_time = limiter.time_until_next_allowed(user_id)
        print(
            f"Повідомлення {message_id:2d} | Користувач {user_id} | "
            f"{'✓' if result else f'× (очікування {wait_time:.1f}с)'}"
        )
        time.sleep(random.uniform(0.1, 1.0))


if __name__ == "__main__":
    test_throttling_limiter()
