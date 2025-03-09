from configparser import ConfigParser
from typing import Any, List, Optional

from facefusion import state_manager
from facefusion.common_helper import cast_bool, cast_float, cast_int

CONFIG_PARSER = None


def get_config_parser() -> ConfigParser:
	global CONFIG_PARSER

	if CONFIG_PARSER is None:
		CONFIG_PARSER = ConfigParser()
		CONFIG_PARSER.read(state_manager.get_item('config_path'), encoding = 'utf-8')
	return CONFIG_PARSER


def clear_config_parser() -> None:
	global CONFIG_PARSER

	CONFIG_PARSER = None


def get_str_value(section : str, option : str, fallback : Optional[str] = None) -> Optional[str]:
	config_parser = get_config_parser()

	if config_parser.has_option(section, option) and config_parser.get(section, option).strip():
		return config_parser.get(section, option)
	return fallback


def get_int_value(section : str, option : str, fallback : Optional[str] = None) -> Optional[int]:
	config_parser = get_config_parser()

	if config_parser.has_option(section, option) and config_parser.get(section, option).strip():
		return config_parser.getint(section, option)
	return cast_int(fallback)


def get_float_value(section : str, option : str, fallback : Optional[str] = None) -> Optional[float]:
	config_parser = get_config_parser()

	if config_parser.has_option(section, option) and config_parser.get(section, option).strip():
		return config_parser.getfloat(section, option)
	return cast_float(fallback)


def get_bool_value(section : str, option : str, fallback : Optional[str] = None) -> Optional[bool]:
	config_parser = get_config_parser()

	if config_parser.has_option(section, option) and config_parser.get(section, option).strip():
		return config_parser.getboolean(section, option)
	return cast_bool(fallback)


def get_str_list(key : str, fallback : Optional[str] = None) -> Optional[List[str]]:
	value = get_value_by_notation(key)

	if value or fallback:
		return [ str(value) for value in (value or fallback).split(' ') ]
	return None


def get_int_list(key : str, fallback : Optional[str] = None) -> Optional[List[int]]:
	value = get_value_by_notation(key)

	if value or fallback:
		return [ cast_int(value) for value in (value or fallback).split(' ') ]
	return None


def get_float_list(key : str, fallback : Optional[str] = None) -> Optional[List[float]]:
	value = get_value_by_notation(key)

	if value or fallback:
		return [ cast_float(value) for value in (value or fallback).split(' ') ]
	return None


def get_value_by_notation(key : str) -> Optional[Any]:
	config_parser = get_config_parser()

	if '.' in key:
		section, name = key.split('.')
		if section in config_parser and name in config_parser[section]:
			return config_parser[section][name]
	if key in config_parser:
		return config_parser[key]
	return None
