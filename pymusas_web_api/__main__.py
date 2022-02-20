import argparse

import uvicorn


def main() -> None:
    description = "Arguments to run the uvicorn server."
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('--host', type=str, default="127.0.0.1",
                        help="Default: 127.0.0.1")
    parser.add_argument('--port', type=int, default=5000,
                        help="Default: 5000")
    parser.add_argument('--log-level', type=str, default='info',
                        help="Default: info")
    parser.add_argument('--reload', action='store_true',
                        help="Enable auto-reload (Default False)")
    args = parser.parse_args()
    print(args)

    uvicorn.run("server:app", host=args.host, port=args.port,
                log_level=args.log_level, reload=args.reload)


if __name__ == '__main__':
    main()
