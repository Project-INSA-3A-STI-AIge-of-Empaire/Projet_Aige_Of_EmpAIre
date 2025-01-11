from behaviorTree import BehaviorTree, treeNode, ctrlNode, decoNode, leafNode, Sequence, Fallback, UntilFail, UntilSuccess, ForceFail, Action, Condition, Invert, TestLeaf


t1=TestLeaf("success")
t2=TestLeaf("success")
t3=TestLeaf("failure")
t4=TestLeaf("success")
t5=TestLeaf("success")



Ff=ForceFail("waiting",t2)

F1=Fallback("waiting",[Ff,t3,t4])

S1=Sequence("waiting",[t1,F1,t5])

testTree=BehaviorTree("waiting",S1)


testTree.start()


#testing the structure of the tree
#the resulting prints should theoretically be testing leaf repeated 4 times
#this is NOT the final tree

# Problem : the child of a given ctrl or deco node is an instance of one of the many types of nodes i have created
# thus child has an "update(self)" method
# how do i access the relevant update method ?
# self.child.update(self.child) doesnt work, it seems to treat self.child as an int or sth weird like that


#attempt at a pseudo version of what a behavior tree might look like in the final version: 
#initialize all the nodes that dont depend on aggressivity (e.g the leaf nodes, the start nodes, the deco nodes)
#through a if-then or case match initialize different versions of the ctrl nodes (a more agressive tree might try attacking before fleeing in the corresponding fallback node, while a more passive one might put the fleeing node first)

# a snippet of the tree dealing with being attacked might look like this for exemple :

# profile="aggressive"
#
# attack=Action()
# flee=Action()
# checkifenemy=Condition()
# initialize all other nodes accordingly ...
# ...
# if(profile=="aggressive"):
#     underAttack=Fallback("waiting",[checkifenemy,attack,flee])
#     initialize the other ctrl nodes ...
# elif(profile=="passive"):
#     underAttack=Fallback("waiting",[checkifenemy,flee,attack])
#     initialize the other ctrl nodes ...
