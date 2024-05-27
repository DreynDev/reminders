if ("Notification" in window) {
  // Запрашиваем разрешение на показ уведомлений
  Notification.requestPermission()
    .then((permission) => {
      if (permission === "granted") {
        // Создаем уведомление при наступлении напоминания
        function showReminder(reminder) {
          new Notification(`Напоминание: ${reminder.title}`, {
            body: reminder.text,
            icon: "/images/notification-icon.png",
          });
        }

        // Получаем список напоминаний json
        fetch("/reminders")
          .then((response) => response.json())
          .then((data) => {
            data.forEach((reminder) => {
              // Преобразуем строку в объект Date
              const reminderDate = new Date(reminder.reminder_at);
              // Проверяем, наступило ли время напоминания
              if (reminderDate <= new Date()) {
                showReminder(reminder);
              } else {
                // Планируем показ уведомления при наступлении времени напоминания
                setTimeout(
                  () => showReminder(reminder),
                  reminderDate - new Date()
                );
              }
            });
          })
          .catch((error) => {
            console.error("Ошибка при получении списка напоминаний:", error);
          });
      }
    })
    .catch((error) => {
      console.error("Ошибка при получении разрешения на уведомления:", error);
    });
} else {
  console.error("Ваш браузер не поддерживает уведомления");
}
