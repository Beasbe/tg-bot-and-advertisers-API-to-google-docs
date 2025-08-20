import subprocess, sys

def run_script(script_name, *args):
    command = ["python", script_name] + list(args)
    subprocess.run(command, check=True)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Использование: python script.py <дата> <курс доллара>")
        sys.exit(1)
    Date = sys.argv[1]
    Exchange = sys.argv[2]
    print(f"Дата: {Date}")
    print(f"Курс доллара: {Exchange}")

    try:
        run_script("GetTeasersStat.py", Date, Exchange) # собирает статистику из сетей
        run_script("SendTeasersStat.py", Date) # выгружает статистику рекламодателю
        run_script("GetStops.py") # загружает последние недобавленные стопы (вчера и сегодня)
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при выполнении {e.cmd}: {e}")

    print("Все скрипты выполнены.")
