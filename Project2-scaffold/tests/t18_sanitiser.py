# ADVANCED — sanitiser pattern.
# Subtracting a value from itself always yields 0. A real sanitiser-aware
# analyser would prove the result is safe; ours sees taint propagate through
# the binop and reports an alarm (false positive).
from lang import *
prog = seq(
    Input("x"),
    Assign("y", Bin("-", Var("x"), Var("x"))),    # always 0, but both ops tainted
    Sink(Var("y")),
)
expected_alarms = 0
description = "ADVANCED — false positive: x - x is constant 0 but propagates taint"
