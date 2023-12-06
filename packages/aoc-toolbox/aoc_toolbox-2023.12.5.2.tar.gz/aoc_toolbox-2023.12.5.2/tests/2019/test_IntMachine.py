import aoc_toolbox.intmachine as tb

def test_resolve_position_mode_argument():
    PROGRAM = "00001,5,5,5,99,-1"
    robot = tb.IntMachine(PROGRAM)
    robot._fetch()
    # read access
    assert robot._resolve_arg(0) == -1
    assert robot._resolve_arg(1) == -1
    # write access
    assert robot._resolve_arg(2) == 5

def test_resolve_immediate_mode_argument():
    PROGRAM = "11101,5,5,5,99,-1"
    robot = tb.IntMachine(PROGRAM)
    robot._fetch()
    #read access
    assert robot._resolve_arg(0) == 5
    assert robot._resolve_arg(1) == 5
    # write access
    assert robot._resolve_arg(2) == 5

def test_resolve_relative_mode_argument():
    PROGRAM = "22201,5,5,5,99,-1,-2"
    robot = tb.IntMachine(PROGRAM)
    robot._fetch()
    #read access
    assert robot._resolve_arg(0) == -1
    assert robot._resolve_arg(1) == -1
    # write access
    assert robot._resolve_arg(2) == 5
    robot.rbase+=1
    robot._fetch()
    #read access
    assert robot._resolve_arg(0) == -2
    assert robot._resolve_arg(1) == -2
    # write access
    assert robot._resolve_arg(2) == 6

def test_first_program():
    PROGRAM = "1,9,10,3,2,3,11,0,99,30,40,50"
    robot = tb.IntMachine(PROGRAM)
    robot._fetch()._execute()
    assert robot.ram[3] == 70
    robot._fetch()._execute()
    assert robot.ram[0] == 3500
    robot._fetch()._execute()
    assert robot.opcode == 99

def test_add_works():
    PROGRAM = "1,0,0,0,99"
    robot = tb.IntMachine(PROGRAM).run()
    assert robot.ram[0] == 2

def test_mul_works():
    PROGRAM = "2,5,6,0,99,3,2"
    robot = tb.IntMachine(PROGRAM).run()
    assert robot.ram[0] == 6
    PROGRAM = "2,4,4,5,99,0"
    robot = tb.IntMachine(PROGRAM).run()
    assert robot.ram[5] == 9801

def test_add_and_mul_work_together():
    PROGRAM = "1,1,1,4,99,5,6,0,99"
    robot = tb.IntMachine(PROGRAM).run()
    assert robot.ram[4] == 2
    assert robot.ram[0] == 30

def test_input_stores_in_ram():
    ADDR = 3
    PROGRAM = f"03,{ADDR},99"
    VALUE = -1
    robot = tb.IntMachine(PROGRAM)
    robot.input(VALUE)
    robot.run()
    assert robot.ram[ADDR] == VALUE

def test_output_prints_from_ram():
    VALUE = -1
    PROGRAM = f"004,3,99,{VALUE}"
    robot = tb.IntMachine(PROGRAM)
    robot.run()
    RESULT = robot.output()
    assert RESULT == VALUE

def test_less_than_stores_FALSE_when_false():
    ADDR = 5
    VALUE = 1
    PROGRAM = f"11107,{VALUE},1,{ADDR},99"
    robot = tb.IntMachine(PROGRAM)
    robot.run()
    assert robot.ram[ADDR] == tb.Bool.FALSE.value

def test_less_than_stores_TRUE_when_true():
    ADDR = 5
    VALUE = 0
    PROGRAM = f"11107,{VALUE},1,{ADDR},99"
    robot = tb.IntMachine(PROGRAM)
    robot.run()
    assert robot.ram[ADDR] == tb.Bool.TRUE.value


def test_equals_stores_FALSE_when_false():
    ADDR = 5
    VALUE = 1
    PROGRAM = f"11108,{VALUE},1,{ADDR},99"
    robot = tb.IntMachine(PROGRAM)
    robot.run()
    assert robot.ram[ADDR] == tb.Bool.TRUE.value

def test_equals_stores_TRUE_when_true():
    ADDR = 5
    VALUE = 0
    PROGRAM = f"11108,{VALUE},1,{ADDR},99"
    robot = tb.IntMachine(PROGRAM)
    robot.run()
    assert robot.ram[ADDR] == tb.Bool.FALSE.value

def test_jump_if_true_jumps_when_true():
    JMPADDR = 4
    CONDITION = tb.Bool.TRUE.value
    PROGRAM = f"1105,{CONDITION},{JMPADDR},99,99"
    robot = tb.IntMachine(PROGRAM)
    robot._fetch()._execute()
    assert robot.ptr == JMPADDR

def test_jump_if_true_DOES_NOT_jumps_when_false():
    JMPADDR = 4
    CONDITION = tb.Bool.FALSE.value
    PROGRAM = f"1105,{CONDITION},{JMPADDR},99,99"
    robot = tb.IntMachine(PROGRAM)
    robot._fetch()._execute()
    assert robot.ptr == 3


def test_jump_if_false_jumps_when_false():
    JMPADDR = 4
    CONDITION = tb.Bool.FALSE.value
    PROGRAM = f"1106,{CONDITION},{JMPADDR},99,99"
    robot = tb.IntMachine(PROGRAM)
    robot._fetch()._execute()
    assert robot.ptr == JMPADDR

def test_jump_if_false_DOES_NOT_jumps_when_true():
    JMPADDR = 4
    CONDITION = tb.Bool.TRUE.value
    PROGRAM = f"1106,{CONDITION},{JMPADDR},99,99"
    robot = tb.IntMachine(PROGRAM)
    robot._fetch()._execute()
    assert robot.ptr == 3


def test_outputs_stored_input():
    PROGRAM = "3,3,104,-1,99"
    VALUE = -2
    robot = tb.IntMachine(PROGRAM)
    robot.input(VALUE)
    robot.run()
    RESULT = robot.output()
    assert RESULT == VALUE

def test_equals_detects_equality_in_position_mode():
    # checks if input equals 8
    PROGRAM = "3,9,8,9,10,9,4,9,99,-1,8"
    VALUE = 8
    robot = tb.IntMachine(PROGRAM)
    robot.input(VALUE)
    robot.run()
    RESULT = robot.output()
    assert RESULT == tb.Bool.TRUE.value

def test_equals_detects_inequality_in_position_mode():
    # checks if input equals 8
    PROGRAM = "3,9,8,9,10,9,4,9,99,-1,8"
    VALUE = 7
    robot = tb.IntMachine(PROGRAM)
    robot.input(VALUE)
    robot.run()
    assert robot.output() == tb.Bool.FALSE.value

def test_less_than_detects_lesser_value_in_position_mode():
    # checks if input < 8
    PROGRAM = "3,9,7,9,10,9,4,9,99,-1,8"
    VALUE = 7
    robot = tb.IntMachine(PROGRAM)
    robot.input(VALUE)
    robot.run()
    assert robot.output() == tb.Bool.TRUE.value

def test_less_than_detects_equal_or_greater_value_in_position_mode():
    # checks if input < 8
    PROGRAM = "3,9,7,9,10,9,4,9,99,-1,8"
    VALUE = 8
    robot = tb.IntMachine(PROGRAM)
    robot.input(VALUE)
    robot.run()
    assert robot.output() == tb.Bool.FALSE.value

def test_equals_detects_equality_in_immediate_mode():
    # checks if input equals 8
    PROGRAM = "3,3,1108,-1,8,3,4,3,99"
    VALUE = 8
    robot = tb.IntMachine(PROGRAM)
    robot.input(VALUE)
    robot.run()
    assert robot.output() == tb.Bool.TRUE.value

def test_equals_detects_inequality_in_immediate_mode():
    # checks if input equals 8
    PROGRAM = "3,3,1108,-1,8,3,4,3,99"
    VALUE = 7
    robot = tb.IntMachine(PROGRAM)
    robot.input(VALUE)
    robot.run()
    assert robot.output() == tb.Bool.FALSE.value

def test_less_than_detects_lesser_value_in_immediate_mode():
    # checks if input < 8
    PROGRAM = "3,3,1107,-1,8,3,4,3,99"
    VALUE = 7
    robot = tb.IntMachine(PROGRAM)
    robot.input(VALUE)
    robot.run()
    assert robot.output() == tb.Bool.TRUE.value

def test_less_than_detects_equal_or_greater_value_in_immediate_mode():
    # checks if input < 8
    PROGRAM = "3,3,1107,-1,8,3,4,3,99"
    VALUE = 8
    robot = tb.IntMachine(PROGRAM)
    robot.input(VALUE)
    robot.run()
    assert robot.output() == tb.Bool.FALSE.value

def test_jump_if_true_jumps_with_true_condition():
    PROGRAM = "3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9"
    VALUE = 0
    robot = tb.IntMachine(PROGRAM)
    robot.input(VALUE)
    robot.run()
    assert robot.output() == 0


def test_jump_if_true_ignore_false_condition():
    PROGRAM = "3,3,1105,-1,9,1101,0,0,12,4,12,99,1"
    VALUE = 1
    robot = tb.IntMachine(PROGRAM)
    robot.input(VALUE)
    robot.run()
    assert robot.output() == 1

def test_prints_999_because_input_is_lesser_than_8():
    PROGRAM = "3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99" # noqa
    VALUE = 7
    robot = tb.IntMachine(PROGRAM)
    robot.input(VALUE)
    robot.run()
    assert robot.output() == 999

def test_prints_1000_because_input_equals_8():
    PROGRAM = "3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99" # noqa
    VALUE = 8
    robot = tb.IntMachine(PROGRAM)
    robot.input(VALUE)
    robot.run()
    assert robot.output() == 1000

def test_prints_1001_because_input_is_greater_than_8():
    PROGRAM = "3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99" # noqa
    VALUE = 9
    robot = tb.IntMachine(PROGRAM)
    robot.input(VALUE)
    robot.run()
    assert robot.output() == 1001

def test_outputs_copy_of_itself():
    PROGRAM =  "109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99"
    robot = tb.IntMachine(PROGRAM)
    robot.run()
    result = []
    try:
        while True:
            result.append(str(robot.output()))
    except StopIteration:
        RESULT = ",".join(result)
    except Exception as e:
        raise e
    assert RESULT == PROGRAM

def test_compute_large_number():
    PROGRAM =  "1102,34915192,34915192,7,4,7,99,0"
    robot = tb.IntMachine(PROGRAM)
    robot.run()
    RESULT = robot.output()
    assert len(str(RESULT)) == 16

def test_outputs_large_number():
    PROGRAM = "104,1125899906842624,99"
    robot = tb.IntMachine(PROGRAM)
    robot.run()
    assert robot.output() == 1125899906842624
