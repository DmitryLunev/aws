# 📁 Docker AWS Logs

## 📖 Кратко о проекте
Этот проект представляет собой программу на Python, которая запускает Docker-контейнер 
с заданным образом и командой bash, а затем отправляет логи контейнера в AWS CloudWatch. 
Программа создает необходимые группы и потоки логов в CloudWatch, если они не существуют.

## 🧾 TODO список (основные положения)
- Настроить создание Docker-контейнера с заданным образом и командой.
- Реализовать отправку логов контейнера в AWS CloudWatch.
- Обработка ошибок и перехват прерываний.
- Написать unit-тесты для основной функциональности.
- Документирование использования программы.
- Написать README.md с инструкциями по запуску и использованием программы.

## 💻 Запуск проекта
Клонирование репозитория:
``` bash
git clone git@github.com:DmitryLunev/docker_asw_task.git
cd docker_aws_logs
```
Создание виртуального окружения (venv):
```bash
python -m venv venv
```

Активация виртуального окружения (venv):
Linux / Mac:
```
```bash
source venv/bin/activate
```
Windows:

```bash
venv\Scripts\activate
```
Установка зависимостей:
```bash
pip install -r requirements.txt
```
Настройка переменных окружения:
Создайте файл .env на основе .env.example и укажите необходимые 
значения, такие как AWS Access Key, Secret Key и Region.

## Запуск программы:

```bash
python main.py \
  --docker-image python \
  --bash-command 'echo "pip install pip -U\npip install tqdm\necho \"import time; counter = 0; while True: print(counter); counter += 1; time.sleep(0.1)\" > script.py\npython3 script.py" > cmd.sh && sh cmd.sh' \
  --aws-cloudwatch-group "test-task-group-1" \
  --aws-cloudwatch-stream "test-task-stream-1" \
  --aws-access-key-id {ACCESS_KEY} \
  --aws-secret-access-key {SECRET_ACCESS_KEY} \
  --aws-region "eu-north-1"
```
Программа запустит Docker-контейнер с указанным образом и командой, а затем будет отправлять логи в AWS CloudWatch.

## 📑 Дополнительная информация
Для остановки программы нажмите Ctrl + C в консоли.

## Возникшие сложности. 
В ходе работы над проектом возникает проблема при попытке запуска контейнера. 
Проблему не удалось решить в указанный срок. 