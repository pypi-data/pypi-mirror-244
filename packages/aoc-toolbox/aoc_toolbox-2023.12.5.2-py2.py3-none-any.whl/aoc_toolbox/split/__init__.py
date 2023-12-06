from typing import Iterator, Dict, Callable, Tuple, List

AS_IS = True
IGNORE = False

def numbers()->Dict:
	return {" ":int}

def in_two(
		symbol:str,
		left:Callable|bool|None=AS_IS,
		right:Callable|bool|None=AS_IS,
		both:Callable|bool|None=None
	)->Dict:

	if both is not None:
		left=both
		right=both

	return {symbol:[left, right]}

def _parse(string:str, splitter:Dict|Callable)->Iterator:
	if isinstance(splitter, Callable):
		return [splitter(string)]

	if isinstance(splitter, bool):
		if splitter == AS_IS:
			return [string]
		return [None]

	if not isinstance(splitter, Dict):
		raise TypeError()

	if len(splitter.keys()) != 1 :
		raise ValueError(f"""
Ambiguous split order, could not identify next split; \
must have a single key per step @ {splitter.keys()}""")

	symbol = list(splitter.keys()).pop()
	process = splitter[symbol]

	if isinstance(process, Callable):
		if process == int:
			string = string.strip()
		return [[process(_) for _ in string.split(symbol)]]

	if not isinstance(process, List):
		raise TypeError(f"Unknown mapping type '{type(process)}' @ {splitter}. Must map symbol to a Function or a 2-values Mapping List.") # noqa

	if len(process) != 2:
		raise ValueError(f"Only left and right assignments are supported, list must have two and only two values @ {splitter}") # noqa

	left, right = string.split(symbol)

	return [*_parse(left, process[0]),*_parse(right, process[1])]



def parse(string:str, splitter:Dict|Callable|str)->Iterator:
	if isinstance(splitter, str):
		splitter = from_pattern(splitter)

	return tuple(elem for elem in _parse(string, splitter) if elem is not None)


def from_pattern(pattern:str)->Dict:
	"""
	Example :
	```
	line='game 1: 12 34 55 | 23 24 11'
	splitter = from_pattern('_[ 2]int[:1]int+[|2]int+')

	parse(line, splitter) == [1,[12,34,55],[23,24,11]]
	```

	Splitter syntax :
	- Starts with '['
	- immediately followed by the splitting symbol
	- immediately followed by a priority value (less is higher priority)
	- immediately ended with ']'

	i.e. [|12] has a priority of 12 and splits on the '|' symbol.
	The splitter [ 3] has a priority of 3 and splits on a ' ' symbol.

	In a splitting pattern, the highest priority should always belong to a single splitter.
	:raises: `ValueError` if two or more spliters share the highest priority.


	Leaf Processing :
	- '_' to Ignore a field
	- 'int' to convert the value to a unique integer
	- 'str' to keep the value as-is
	- 'int+' to convert the value as space separated integers into a table

	"""
	import re
	def _priority(m:Tuple):
		return int(m.groupdict()["priority"])

	SPLIT_PATTERN = "\[(?P<symbol>[^0-9]+)(?P<priority>\d+)\]"

	splits = list(re.finditer(SPLIT_PATTERN, pattern))

	if len(splits) == 0:
		# Leaf obtained
		# We return an evaluation depending on the string
		match pattern:
			case "ints":
				raise ValueError("Invalid command, do you mean int+ ?")
			case "int+":
				return numbers()
			case "int":
				return int
			case "str":
				return str
			case "_":
				return IGNORE
	else:
		splits = sorted(splits, key=_priority)

		if len(splits) > 1 and _priority(splits[0]) == _priority(splits[1]):
			raise ValueError(f"Ambiguous split order, could not identify next split in '{pattern}'") # noqa

		split_match:re.Match = splits[0]
		left_pattern = pattern[:split_match.span()[0]]
		right_pattern = pattern[split_match.span()[1]:]

		return in_two(
			split_match.groupdict()["symbol"],
			left=from_pattern(left_pattern),
			right=from_pattern(right_pattern))

