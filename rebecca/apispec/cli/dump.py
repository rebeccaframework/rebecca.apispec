import argparse
import json

from pyramid.paster import get_app

from rebecca.apispec.directives import get_apispec


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("config")
    args = parser.parse_args()
    app = get_app(args.config)
    apispec = get_apispec(app)
    print(json.dumps(apispec.to_dict(), indent=2))


if __name__ == "__main__":
    main()
