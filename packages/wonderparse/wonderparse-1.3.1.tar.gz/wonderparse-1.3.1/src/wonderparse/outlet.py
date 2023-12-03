import dataclasses as _dataclasses


@_dataclasses.dataclass
class OutfileInformation:
	dest:str
	option_strings:tuple
	get_manager:callable
	help:str


