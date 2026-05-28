import socket
import requests
import time
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
from rich import print

console = Console()
history = []

# ---------------------------
# HELPERS
# ---------------------------
def clean_input(text: str):
    return text.strip().lower()


def log(action, value):
    history.append((datetime.now().strftime("%H:%M:%S"), action, value))


def safe_request(url, timeout=5):
    try:
        return requests.get(url, timeout=timeout)
    except Exception as e:
        console.print(f"[red]REQUEST ERROR[/red] {e}")
        return None


# ---------------------------
# BANNER
# ---------------------------
def banner():
    console.clear()
    console.print(Panel.fit(
        "[bold green]OSINT ULTRA PRO TOOL[/bold green]\n"
        "[cyan]LEGAL • PUBLIC DATA ONLY • NO INTRUSION[/cyan]\n"
        "[grey]SOC TERMINAL v3.1 (IMPROVED)[/grey]",
        border_style="green"
    ))


# ---------------------------
# SCAN EFFECT
# ---------------------------
def scan_effect(text="Scanning"):
    speed = 0.005
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
    ) as progress:
        task = progress.add_task(f"[cyan]{text}...", total=100)

        for _ in range(100):
            time.sleep(speed)
            progress.update(task, advance=1)


# ---------------------------
# USERNAME TOOL
# ---------------------------
def username_tool(username):
    username = clean_input(username)
    log("USERNAME", username)

    scan_effect("Username OSINT Scan")

    table = Table(title="USERNAME INTEL", style="green")
    table.add_column("Platform", style="cyan")
    table.add_column("URL", style="white")

    sites = {
        "GitHub": f"https://github.com/{username}",
        "X": f"https://x.com/{username}",
        "Reddit": f"https://reddit.com/user/{username}",
        "Instagram": f"https://instagram.com/{username}",
        "TikTok": f"https://tiktok.com/@{username}",
    }

    for k, v in sites.items():
        table.add_row(k, v)

    console.print(table)


# ---------------------------
# DOMAIN TOOL
# ---------------------------
def domain_tool(domain):
    domain = clean_input(domain)
    log("DOMAIN", domain)

    scan_effect("Domain Recon")

    table = Table(title="DOMAIN INTEL", style="cyan")
    table.add_column("Field", style="green")
    table.add_column("Value", style="white")

    try:
        host = socket.gethostbyname_ex(domain)
        ip_list = ", ".join(host[2])

        table.add_row("Domain", domain)
        table.add_row("Resolved IP(s)", ip_list)
        table.add_row("DNS Status", "OK (Public Resolution)")
        table.add_row("WHOIS", "SIMULATED SAFE MODE")

    except Exception as e:
        console.print(f"[red]DNS ERROR[/red] {e}")
        return

    console.print(table)


# ---------------------------
# IP TOOL
# ---------------------------
def ip_tool(ip):
    ip = clean_input(ip)
    log("IP", ip)

    scan_effect("IP Intelligence Lookup")

    res = safe_request(f"http://ip-api.com/json/{ip}")
    if not res:
        return

    data = res.json()

    if data.get("status") != "success":
        console.print("[red]API returned no valid data[/red]")
        return

    table = Table(title="IP INTEL REPORT", style="yellow")
    table.add_column("Field", style="cyan")
    table.add_column("Value", style="white")

    fields = [
        ("IP", ip),
        ("Country", data.get("country")),
        ("Region", data.get("regionName")),
        ("City", data.get("city")),
        ("ISP", data.get("isp")),
        ("Org", data.get("org")),
        ("Status", data.get("status")),
    ]

    for k, v in fields:
        table.add_row(str(k), str(v))

    console.print(table)


# ---------------------------
# MENU
# ---------------------------
def menu():
    console.print(Panel(
        "[1] Username OSINT\n"
        "[2] Domain Recon\n"
        "[3] IP Intelligence\n"
        "[4] Exit",
        title="MAIN MENU",
        border_style="green"
    ))


# ---------------------------
# HISTORY
# ---------------------------
def show_history():
    table = Table(title="HISTORY", style="magenta")
    table.add_column("Time", style="cyan")
    table.add_column("Action", style="white")
    table.add_column("Value", style="green")

    for h in history[-10:]:
        table.add_row(*h)

    console.print(table)


# ---------------------------
# MAIN LOOP
# ---------------------------
def main():
    while True:
        banner()
        menu()

        print("[grey]H = History[/grey]")
        choice = input("\n[?] Select ➜ ")

        if choice == "1":
            username_tool(input("Username ➜ "))

        elif choice == "2":
            domain_tool(input("Domain ➜ "))

        elif choice == "3":
            ip_tool(input("IP ➜ "))

        elif choice == "4":
            console.print("[red]Shutting down OSINT terminal...[/red]")
            break

        elif choice.lower() == "h":
            show_history()

        else:
            console.print("[red]Invalid option[/red]")

        input("\nPress ENTER to continue...")


if __name__ == "__main__":
    main()
