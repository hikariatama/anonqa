# Based on https://github.com/rodion-gudz/telegram-bot-template/blob/master/app/config.py

import os
from dataclasses import MISSING, dataclass, fields

import toml


@dataclass
class ConfigMain:
    token: str
    throttling_rate: float
    secret: str
    local_api_endpoint: str
    postgres_uri: str
    admins: list[int]
    owner_id: int
    default_ratelimit: str
    recaptcha_site_key: str
    dev: bool
    prime_a: int
    prime_b: int


@dataclass
class Config:
    main: ConfigMain

    @classmethod
    def parse(cls, data: dict) -> "Config":
        sections = {}

        for section in fields(cls):
            pre = {}
            current = data[section.name]

            for field in fields(section.type):
                if field.name in current:
                    pre[field.name] = current[field.name]
                elif field.default is not MISSING:
                    pre[field.name] = field.default
                else:
                    raise ValueError(
                        f"Missing field {field.name} in section {section.name}"
                    )

            sections[section.name] = section.type(**pre)

        return cls(**sections)


def parse(config_file: str) -> Config:
    if not os.path.isfile(config_file) and not config_file.endswith(".toml"):
        config_file += ".toml"

    if not os.path.isfile(config_file):
        raise FileNotFoundError(f"Config file not found: {config_file} no such file")

    with open(config_file, "r") as f:
        data = toml.load(f)

    return Config.parse(dict(data))
