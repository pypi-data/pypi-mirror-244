import typing
import json
import argparse


class Config():
    __options = None

    def __init__(self, options: dict = None, json_file_path: str = None):
        if not options and json_file_path:
            options = self._load_options_from_file(json_file_path=json_file_path)
        elif not options:
            options = {}

        if isinstance(options, dict):
            self.__options = options
        elif isinstance(options, Config):
            self.__options = options.__options

    def __str__(self):
        return self.to_string()

    def to_string(self):
        return str(self.__options)

    def to_json(self):
        return json.dumps(self.__options)

    def process_args(self, args: dict):
        if args:
            print(f'processing args [{args}]')
            if isinstance(args, argparse.ArgumentParser):
                args = args.parse_args()
                print(f'process command line arguments [{args}]')
            if isinstance(args, argparse.Namespace):
                args = vars(args)
                print(f'converted args to dictionary [{args}]')

            for arg in args:
                print(f'processing args [arg={arg}]')
                # value = getattr(args, arg)
                value = args.get(arg)
                print(f'processing args [arg={arg}][value={value}]')
                if value:
                    print(f'set config [key={arg}][value={value}]')
                    self.set(arg, value)

    def _load_options_from_file(self, json_file_path: str = None) -> dict:
        options = None
        with open(json_file_path, "rb") as f:
            options = json.load(f)
        return options

    def get(self, key: str, default_value: typing.Any = None):
        keys = key.split('.')

        value = self.__options
        for subkey in keys:
            if value:
                if subkey in value:
                    value = value[subkey]
                else:
                    value = None
            else:
                value = None

        if not value:
            value = default_value

        return value

    def getAsBool(self, key: str, default_value: typing.Any = None) -> bool:
        value_raw = self.get(key=key, default_value=default_value)
        value = None
        true_values = [True, 'TRUE', 'T', '1', 1]
        if isinstance(value_raw, str):
            value_raw = value_raw.upper()
        value = value_raw in true_values
        return value

    def getAsInt(self, key: str, default_value: int = None) -> int:
        value_raw = self.get(key=key, default_value=default_value)
        try:
            value = int(value_raw)
        except Exception as ex:
            raise Exception(f'Invalid config value (expected numeric value) [key={key}][value={value_raw}]') from ex
        return value

    # support key=a.b.c where it will create intermediate dictionaries
    def set(self, key: str, value: typing.Any):
        print('options.set')
        keys = key.split('.')

        parent = self.__options
        print('options', self.__options)
        print(f'keys [keys:{keys}][key count:{len(keys)}]')
        for key_number in range(0, len(keys) - 1):
            key = keys[key_number]
            print(f'iterate keys [key_num:{key_number}][key={key}][parent={parent}]')
            if not key in parent:
                print(f'init item [key={key}][parent={parent}]')
                parent[key] = {}
                print(f'init item complete [key={key}][parent={parent}]')
            parent = parent.get(key)
            print(f'new parent [parent={parent}]')
            print('options l', self.__options)

        last_key = keys[len(keys) - 1]
        print(f'set parent to value [parent={parent}][last_key={last_key}][value={value}]')
        parent[last_key] = value
        print('options', self.__options)
