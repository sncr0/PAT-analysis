import argparse
from db_gateway.schema import init_db
from db_gateway.mqtt_listener import start as start_mqtt


def main():
    parser = argparse.ArgumentParser(
        description="🛠️ DB Gateway CLI — manage schema and MQTT ingestion",
        epilog="Examples:\n  python -m db_gateway init-db --drop-existing\n  python -m db_gateway mqtt",
        formatter_class=argparse.RawTextHelpFormatter
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    # Subcommand: init-db
    parser_init = subparsers.add_parser("init-db", help="Initialize the database schema")
    parser_init.add_argument(
        "--drop-existing",
        action="store_true",
        help="Drop existing tables before creating schema"
    )

    # Subcommand: mqtt
    subparsers.add_parser("mqtt", help="Start the MQTT listener service")

    args = parser.parse_args()

    if args.command == "init-db":
        print("🧱 Initializing DB schema...")
        init_db(drop_existing=args.drop_existing)
        print("✅ Done.")
    elif args.command == "mqtt":
        print("📡 Starting MQTT listener...")
        start_mqtt()


if __name__ == "__main__":
    main()
