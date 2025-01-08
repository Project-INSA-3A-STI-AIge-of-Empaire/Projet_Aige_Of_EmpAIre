from behaviorTree import treeNode, ctrlNode, decoNode, leafNode, Sequence, Fallback, UntilFail, UntilSuccess, ForceFail, Action, Condition, Invert, TestLeaf

testTree=decoNode("waiting",
                  Sequence("waiting",[TestLeaf,
                                Fallback("waiting",[ForceFail("waiting",TestLeaf),
                                          TestLeaf]),
                                TestLeaf]))

decoNode.start(testTree)

#testing the structure of the tree
#the test fails at Forcefail (ironically) as of now bc of the asserts
#the resulting prints should theoretically be testing leaf repeated 4 times
#this is NOT the final tree

#removing forceFail presents other problems : update is apparently given 2 args somehow
