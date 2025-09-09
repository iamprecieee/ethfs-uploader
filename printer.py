import random
import time

from enums import Colors


def typewriter_print(text, delay=0.03, color=Colors.WHITE):
    print(f"{color}{Colors.BOLD}", end="", flush=True)
    for char in text:
        print(char, end="", flush=True)
        time.sleep(delay + random.uniform(0, 0.001))
    print(Colors.END)


class AnimatedPrinter:
    def __init__(self):
        self.monospace_font = True

    def create_dynamic_banner(self, message, padding=4):
        message_len = len(message)
        inner_width = message_len + (padding * 2)
        outer_width = inner_width + 4

        outer_top = "╔" + "═" * outer_width + "╗"
        outer_bottom = "╚" + "═" * outer_width + "╝"

        inner_top = "║ ╔" + "═" * inner_width + "╗ ║"
        inner_bottom = "║ ╚" + "═" * inner_width + "╝ ║"

        message_line = f"║ ║{' ' * padding}{message}{' ' * padding}║ ║"

        return [outer_top, inner_top, message_line, inner_bottom, outer_bottom]

    def print_banner_animated(self, message, color):
        banner_lines = self.create_dynamic_banner(message)

        print(f"\n{color}{Colors.BOLD}")
        for line in banner_lines:
            typewriter_print(f"    {line}", delay=0.001, color=color)
        print(Colors.END)

    def print_step_animated(self, step_num, total_steps, message):
        print()
        for i in range(3):
            print(
                f"\r{Colors.BLUE}{Colors.BOLD}[{'●' * (i + 1)}{'○' * (2 - i)}] ",
                end="",
                flush=True,
            )
            time.sleep(0.2)

        print(
            f"\r{Colors.BLUE}{Colors.BOLD}[{step_num}/{total_steps}]{Colors.END} ",
            end="",
            flush=True,
        )
        typewriter_print(message, delay=0.02)

    def print_success_animated(self, message):
        success_chars = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]

        for char in success_chars:
            print(
                f"\r{Colors.GREEN}{Colors.BOLD}{char} Processing...{Colors.END}",
                end="",
                flush=True,
            )
            time.sleep(0.1)

        print(f"\r{Colors.GREEN}{Colors.BOLD}✅ {message}{Colors.END}")

    def print_error_animated(self, message):
        for _ in range(3):
            print(f"\r{' ' * (len(message) + 3)}", end="", flush=True)
            time.sleep(0.2)
            print(
                f"\r{Colors.RED}{Colors.BOLD}❌ {message}{Colors.END}",
                end="",
                flush=True,
            )
            time.sleep(0.2)

        print("\n")

    def print_warning_animated(self, message):
        for i in range(3):
            print(
                f"\r{Colors.RED}{Colors.BOLD}⚠️ {message}{Colors.END}",
                end="",
                flush=True,
            )
            time.sleep(0.3)
            print(
                f"\r{Colors.YELLOW}{Colors.BOLD}⚠️ {message}{Colors.END}",
                end="",
                flush=True,
            )
            time.sleep(0.3)

        print()

    def print_info_animated(self, message):
        typewriter_print(f"{Colors.CYAN}ℹ️  {message}{Colors.END}", delay=0.02)

    def print_process_animated(self, message, color=Colors.GREEN):
        print(f"{color}  → ", end="", flush=True)
        typewriter_print(message, delay=0.01, color="")
        print(Colors.END, end="")

    def celebration_animation(self, message):
        """Victory animation for successful upload"""
        celebration = ["🎉", "✨", "🚀", "⭐", "🎊"]

        print(f"\n{Colors.GREEN}{Colors.BOLD}")
        for _ in range(5):
            symbols = "".join(random.choices(celebration, k=5))
            print(f"\r    {symbols} {message} {symbols}", end="", flush=True)
            time.sleep(0.3)

        print(f"{Colors.END}\n")


def print_banner(message, color=Colors.CYAN):
    printer = AnimatedPrinter()
    printer.print_banner_animated(message, color)


def print_step(step, total, message):
    printer = AnimatedPrinter()
    printer.print_step_animated(step, total, message)


def print_success(message):
    printer = AnimatedPrinter()
    printer.print_success_animated(message)


def print_error(message):
    printer = AnimatedPrinter()
    printer.print_error_animated(message)


def print_warning(message):
    printer = AnimatedPrinter()
    printer.print_warning_animated(message)


def print_info(message):
    printer = AnimatedPrinter()
    printer.print_info_animated(message)


def print_process(message, color=Colors.GREEN):
    printer = AnimatedPrinter()
    printer.print_process_animated(message, color)


def print_input(message):
    return input(f"{Colors.CYAN}{message}{Colors.END}")


def celebration(message):
    printer = AnimatedPrinter()
    printer.celebration_animation(message)
