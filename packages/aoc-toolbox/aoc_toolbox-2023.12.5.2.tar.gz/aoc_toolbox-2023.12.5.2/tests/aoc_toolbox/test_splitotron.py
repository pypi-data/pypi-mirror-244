import aoc_toolbox as tb

def test_can_wrap_a_splitter_using_condensed_form():
	pattern = '_[ 2]int[:1]int+[|2]int+'
	splitter = tb.split.from_pattern(pattern)
	assert splitter == {
		":":[
			{" ":[
				False,
				int
			]},
			{
				"|":[
					{" ":int},
					{" ":int}
				]
			}
		]
	}

def test_can_wrap_a_splitter():
	splitter = tb.split.in_two(
		":",
		left=tb.split.in_two(
			" ",
			left=tb.split.IGNORE,
			right=int
		),
		right=tb.split.in_two(
			"|",
			both=tb.split.numbers()
		)
	)
	assert splitter == {
		":":[
			{" ":[
				False,
				int
			]},
			{
				"|":[
					{" ":int},
					{" ":int}
				]
			}
		]
	}


def test_can_split_2023d4():
	# GIVEN the following input 'game 1: 12 34 55 | 23 24 11' and the '_ int<-:->|'
	# WHEN we run the splitotron
	# THEN we should obtain the following output : 1,{12,34,55},{23,24,11}

	# GRAMMAR
	# SPLITTER = {SYMBOL: SPLIT_IN_TWO | PROCESS}
	#
	# SPLIT_IN_TWO = SPLIT_SYMBOL:[SPLITTER | PROCESS, SPLITTER | PROCESS]
	pattern = '_[ 2]int[:1]int+[|2]int+'
	splitter = tb.split.from_pattern(pattern)
	line = 'game 1: 12 34 55 | 23 24 11'

	result_with_splitter = tb.split.parse(line, splitter)
	result_with_splitter_pattern = tb.split.parse(line, pattern)

	assert result_with_splitter == (1,[12,34,55],[23,24,11])
	assert result_with_splitter_pattern == (1,[12,34,55],[23,24,11])