# ADVANCED — false positive due to path-insensitivity.
# The sink only fires on the FALSE branch where y is constant.
# A path-sensitive analyser would prove the sink is clean.
# Our path-insensitive analyser will join {y:T} from the true branch with
# {y:U} from the false branch → y becomes T → ALARM (false positive).
from lang import *
prog = seq(
    Input("x"),
    Assign("flag", Num(0)),         # always false
    If(Bin("==", Var("flag"), Num(1)),
        Assign("y", Var("x")),       # tainted — but this branch is dead
        Assign("y", Num(99))),       # always taken — y stays clean
    Sink(Var("y")),
)
expected_alarms = 0   # ground truth says clean (dead branch)
description = "ADVANCED — false positive: path-insensitivity over a dead branch"
