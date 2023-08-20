from plyer import notification


def notify_user(title, message):
    notification.notify(
        title=title,
        message=message,
        timeout=10  # duration the notification stays on screen
    )