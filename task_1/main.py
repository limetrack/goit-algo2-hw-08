import time

from sliding_window_rate_limiter import SlidingWindowRateLimiter


def test_rate_limiter():
    import random

    print("\n=== Симуляція потоку повідомлень ===")
    limiter = SlidingWindowRateLimiter(window_size=10, max_requests=1)

    for message_id in range(1, 11):
        user_id = message_id % 5 + 1
        result = limiter.record_message(str(user_id))
        wait_time = limiter.time_until_next_allowed(str(user_id))

        print(
            f"Повідомлення {message_id:2d} | Користувач {user_id} | "
            f"{'✓' if result else f'× (очікування {wait_time:.1f}с)'}"
        )

        time.sleep(random.uniform(0.1, 1.0))

    print("\nОчікуємо 4 секунди...")
    time.sleep(4)

    print("\n=== Нова серія повідомлень після очікування ===")
    for message_id in range(11, 21):
        user_id = message_id % 5 + 1
        result = limiter.record_message(str(user_id))
        wait_time = limiter.time_until_next_allowed(str(user_id))
        print(
            f"Повідомлення {message_id:2d} | Користувач {user_id} | "
            f"{'✓' if result else f'× (очікування {wait_time:.1f}с)'}"
        )
        time.sleep(random.uniform(0.1, 1.0))


if __name__ == "__main__":
    test_rate_limiter()
