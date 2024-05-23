from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum
from datetime import datetime

# Everything needed for Order VDA5050

class ActionBlockingType(str, Enum):
    # “NONE” – allows driving and other actions
    NONE = "NONE"
    # “SOFT” - allows other actions, but not driving
    SOFT = "SOFT"
    # “HARD” - is the only allowd action at that time
    HARD = "HARD"

class ActionParameter(BaseModel):
    key: str
    value: str

class Action(BaseModel):
    actionType: str
    actionId: str
    blockingType: ActionBlockingType = ActionBlockingType.HARD
    actionParameters: List[ActionParameter] = []
    actionDescription: str = ""

class NodePosition(BaseModel):
    x: float
    y: float
    theta: float = 0.0
    mapId: str = ""
    mapDescription: str = ""
    allowedDeviationXY: float = 0.0
    allowedDeviationTheta: float = 0.0

class Node(BaseModel):
    nodeId: str
    sequenceId: int
    released: bool = True
    nodePosition: Optional[NodePosition]
    actions: List[Action] = []
    nodeDescription: str = ""

class Edge(BaseModel):
    edgeId: str
    sequenceId: int
    edgeDescription: str = ""
    released: bool = True
    startNodeId: str
    endNodeId: str
    actions: List[Action] = []

class Order(BaseModel):
    headerId: int = 0
    timestamp: str = ""
    version: str = "2.0.0"
    manufacturer: str = ""
    serialNumber: str = ""
    orderId: str
    orderUpdateId: int
    nodes: List[Node]
    edges: List[Edge]