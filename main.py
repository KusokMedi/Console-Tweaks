import os
import time
from colorama import Fore, Style, init
try:
    from prompt_toolkit import PromptSession
    from prompt_toolkit.completion import WordCompleter
    from prompt_toolkit.styles import Style as PromptStyle
    prompt_toolkit_available = True
except ImportError:
    prompt_toolkit_available = False

init(autoreset=True)

# ----------------------------- UI -----------------------------
def start_screen():
    os.system("cls" if os.name == "nt" else "clear")
    banner = [
        "  ╔════════════════════════════════════════════╗",
        "  ║        ConsoleTweaks от KusokMedi          ║",
        "  ║               Версия 1.0.0                 ║",
        "  ╚════════════════════════════════════════════╝"
    ]
    for line in banner:
        print(Fore.CYAN + line)
        time.sleep(0.1)
    print(Fore.LIGHTBLACK_EX + "\nНапиши 'help' для списка команд, 'stop' для выхода или введи любую системную команду!\n")
    time.sleep(0.1)

def print_help():
    print(Fore.CYAN + "\n" + "═"*100 + "\n")
    print(Fore.LIGHTYELLOW_EX + "Меню помощи ConsoleTweaks:\n")
    commands_list = [
        ("stop", "Остановить программу"),
        ("credits", "Показать авторов"),
        ("changelog", "Показать историю версий"),
        ("version", "Показать версию программы"),
        ("cmdhelp", "Показать основные команды Windows CMD"),
        ("translit <текст>", "Транслитерировать текст с латиницы на кириллицу"),
        ("cls", "Очистить экран и показать баннер"),
    ]
    for cmd, desc in commands_list:
        print(Fore.WHITE + f"{cmd:<18}" + Fore.LIGHTBLACK_EX + f"- {desc}")
        time.sleep(0.01)
    print(Fore.CYAN + "\n" + "═"*100 + "\n")
    time.sleep(0.1)

def print_credits():
    print(Fore.CYAN + "\nАвторы:")
    time.sleep(0.01)
    print(Fore.LIGHTWHITE_EX + " - Главный разработчик: " + Fore.LIGHTYELLOW_EX + "@KusokMedi / TG: @KusokMedi52")
    time.sleep(0.1)
    print(Fore.CYAN + "\nСпасибо:")
    time.sleep(0.01)
    print(Fore.LIGHTWHITE_EX + " - Тестировщик: " + Fore.LIGHTYELLOW_EX + "@lifelawon\n")

def print_changelog():
    print(Fore.CYAN + "\nИстория изменений:")
    time.sleep(0.1)
    print(Fore.WHITE + "v1.0.0 - Первый релиз с базовыми командами\n")

def print_version():
    print(Fore.LIGHTYELLOW_EX + "\nВерсия ConsoleTweaks: " + Fore.CYAN + "1.0.0\n")

def print_cmdhelp():
    print(Fore.CYAN + "\nОсновные команды Windows CMD:\n")
    cmd_list = [
        ("dir", "показать список файлов и папок"),
        ("cd <путь>", "сменить директорию"),
        ("cls", "очистить экран"),
    ]
    for cmd, desc in cmd_list:
        print(Fore.WHITE + f"{cmd:<12}" + Fore.LIGHTBLACK_EX + f": {desc}")
        time.sleep(0.1)
    print(Fore.CYAN + "\nПодробнее тут:")
    time.sleep(0.1)
    print(Fore.LIGHTBLUE_EX + "https://serverspace.ru/support/help/shpargalka-po-cmd-komandam-v-windows/?utm_source=google.com&utm_medium=organic&utm_campaign=google.com&utm_referrer=google.com\n")

# ----------------------------- Translit -----------------------------
def translit_cmd(text: str) -> str:
    mapping = {
        "sch": "щ", "shh": "щ", "yo": "ё", "zh": "ж", "ch": "ч", "sh": "ш", "yu": "ю", "ya": "я", "ja": "я", "ju": "ю",
        "a": "а", "b": "б", "v": "в", "g": "г", "d": "д", "e": "е", "z": "з", "i": "и", "j": "й", "k": "к",
        "l": "л", "m": "м", "n": "н", "o": "о", "p": "п", "r": "р", "s": "с", "t": "т", "u": "у", "f": "ф",
        "h": "х", "y": "ы", "'": "ь", "c": "ц", "je": "э"
    }
    result = ""
    i = 0
    while i < len(text):
        for size in (3, 2, 1):
            chunk = text[i:i+size].lower()
            if chunk in mapping:
                sym = mapping[chunk].upper() if text[i].isupper() else mapping[chunk]
                result += sym
                i += size
                break
        else:
            result += text[i]
            i += 1
    return result

# ----------------------------- Command Mapping -----------------------------
commands = {
    "help": print_help,
    "credits": print_credits,
    "changelog": print_changelog,
    "version": print_version,
    "cmdhelp": print_cmdhelp,
    "cls": start_screen,
}

# ----------------------------- Autocomplete Setup -----------------------------
# Список команд для автодополнения
command_list = list(commands.keys()) + ["stop", "translit", "cd", "dir", "echo", "copy", "del", "mkdir", "rmdir", "type", "ren", "move"]

if prompt_toolkit_available:
    # Стиль для prompt_toolkit, чтобы избежать ANSI-кодов
    style = PromptStyle.from_dict({
        "prompt": "white",
        "arrow": "grey"
    })
    completer = WordCompleter(command_list, ignore_case=True)
    session = PromptSession(
        message=[("class:prompt", os.getcwd()), ("class:arrow", " → ")],
        style=style,
        completer=completer
    )

# ----------------------------- Main Loop -----------------------------
start_screen()

while True:
    # Формируем приглашение для input()
    prompt = Fore.WHITE + os.getcwd() + Fore.LIGHTBLACK_EX + " → " + Style.RESET_ALL

    # Используем prompt_toolkit, если доступен, иначе input()
    if prompt_toolkit_available:
        text = session.prompt().strip()
    else:
        text = input(prompt).strip()

    if not text:
        continue

    lower_text = text.lower()
    cmd_parts = text.split(maxsplit=1)
    cmd = cmd_parts[0].lower()
    args = cmd_parts[1] if len(cmd_parts) > 1 else ""

    if lower_text in commands:
        commands[lower_text]()
    elif lower_text.startswith("translit"):
        parts = text.split(maxsplit=1)
        if len(parts) == 1:
            print(Fore.LIGHTRED_EX + "Ошибка: нужно указать текст для транслита")
        else:
            print(Fore.LIGHTYELLOW_EX + "\nВаш результат:")
            print(Fore.WHITE + translit_cmd(parts[1]) + "\n")
    elif lower_text == "stop":
        confirm = input(Fore.LIGHTRED_EX + "\nЗавершить работу программы? (y/n): " + Style.RESET_ALL).strip().lower()
        if confirm in ["y", "yes", "д", "да"]:
            print(Fore.LIGHTRED_EX + "Остановка ConsoleTweaks и возврат в основную консоль...")
            break
        else:
            print(Fore.LIGHTYELLOW_EX + "\nОк, возвращаемся к программе ConsoleTweaks..\n")
    elif lower_text.startswith("cd"):
        path = args.strip('"') if args else (r"C:\Users\User" if os.name == "nt" else os.path.expanduser("~"))
        try:
            os.chdir(path)
            print(Fore.LIGHTYELLOW_EX + f"Директория изменена на: {os.getcwd()}")
            if prompt_toolkit_available:
                session.message = [("class:prompt", os.getcwd()), ("class:arrow", " → ")]
        except FileNotFoundError:
            print(Fore.LIGHTRED_EX + f"Система не может найти указанный путь: {path}")
    else:
        try:
            print("")
            os.system(text)
            print("")
        except Exception as e:
            print(Fore.LIGHTYELLOW_EX + f"Ошибка при выполнении команды: {e}")