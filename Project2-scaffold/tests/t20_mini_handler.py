# ADVANCED — small "request handler" mixing many features.
# Two inputs, two sinks, a sanitising-looking branch, and a loop.
# Ground truth: BOTH sinks fire — the analyser should report 2 alarms.
from lang import *
prog = seq(
    Input("user_id"),
    Input("query"),

    # validate user_id ∈ [0, 100]
    If(Bin("&&", Bin(">=", Var("user_id"), Num(0)),
                 Bin("<=", Var("user_id"), Num(100))),
        Assign("uid", Var("user_id")),    # tainted
        Assign("uid", Num(0))),            # clean
    Sink(Var("uid")),                       # tainted on join → ALARM 1

    # process query in a loop
    Assign("result", Num(0)),
    Assign("i", Num(0)),
    While(Bin("<", Var("i"), Num(3)),
        seq(
            Assign("result", Bin("+", Var("result"), Var("query"))),
            Assign("i", Bin("+", Var("i"), Num(1))),
        )),
    Sink(Var("result")),                    # tainted from query → ALARM 2
)
expected_alarms = 2
description = "ADVANCED — mini handler: 2 sources, 2 sinks, branch, loop"
