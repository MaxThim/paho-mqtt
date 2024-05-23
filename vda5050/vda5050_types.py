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

# Everything needed for FactSheet VDA5050

# Enum classes for various string enumerations
class AgvKinematic(str, Enum):
    DIFF = "DIFF"
    OMNI = "OMNI"
    THREEWHEEL = "THREEWHEEL"

class AgvClass(str, Enum):
    FORKLIFT = "FORKLIFT"
    CONVEYOR = "CONVEYOR"
    TUGGER = "TUGGER"
    CARRIER = "CARRIER"

class LocalizationType(str, Enum):
    NATURAL = "NATURAL"
    REFLECTOR = "REFLECTOR"
    RFID = "RFID"
    DMC = "DMC"
    SPOT = "SPOT"
    GRID = "GRID"

class NavigationType(str, Enum):
    PHYSICAL_LINDE_GUIDED = "PHYSICAL_LINDE_GUIDED"
    VIRTUAL_LINE_GUIDED = "VIRTUAL_LINE_GUIDED"
    AUTONOMOUS = "AUTONOMOUS"

class WheelType(str, Enum):
    DRIVE = "DRIVE"
    CASTER = "CASTER"
    FIXED = "FIXED"
    MECANUM = "MECANUM"

class SupportType(str, Enum):
    SUPPORTED = "SUPPORTED"
    REQUIRED = "REQUIRED"

class ActionScope(str, Enum):
    INSTANT = "INSTANT"
    NODE = "NODE"
    EDGE = "EDGE"

class ValueDataType(str, Enum):
    BOOL = "BOOL"
    NUMBER = "NUMBER"
    INTEGER = "INTEGER"
    FLOAT = "FLOAT"
    STRING = "STRING"
    OBJECT = "OBJECT"
    ARRAY = "ARRAY"

# TypeSpecification class
class TypeSpecification(BaseModel):
    seriesName: str
    seriesDescription: Optional[str] = ""
    agvKinematic: AgvKinematic
    agvClass: AgvClass
    maxLoadMass: float = Field(..., gt=0) # gt = Greater than 0
    localizationTypes: List[LocalizationType]
    navigationTypes: List[NavigationType]

# PhysicalParameters class
class PhysicalParameters(BaseModel):
    speedMin: float
    speedMax: float
    accelerationMax: float
    decelerationMax: float
    heightMin: Optional[float]
    heightMax: float
    width: float
    length: float

# ProtocolLimits class
class MaxStringLens(BaseModel):
    msgLen: Optional[int]
    topicSerialLen: Optional[int]
    topicElemLen: Optional[int]
    idLen: Optional[int]
    idNumericalOnly: Optional[bool]
    enumLen: Optional[int]
    loadIdLen: Optional[int]

class MaxArrayLens(BaseModel):
    order_nodes: Optional[int]
    order_edges: Optional[int]
    node_actions: Optional[int]
    edge_actions: Optional[int]
    actions_actionsParameters: Optional[int]
    instantActions: Optional[int]
    trajectory_knotVector: Optional[int]
    trajectory_controlPoints: Optional[int]
    state_nodeStates: Optional[int]
    state_edgeStates: Optional[int]
    state_loads: Optional[int]
    state_actionStates: Optional[int]
    state_errors: Optional[int]
    state_information: Optional[int]
    error_errorReferences: Optional[int]
    information_infoReferences: Optional[int]

class Timing(BaseModel):
    minOrderInterval: float
    minStateInterval: float
    defaultStateInterval: Optional[float]
    visualizationInterval: Optional[float]

class ProtocolLimits(BaseModel):
    maxStringLens: MaxStringLens
    maxArrayLens: MaxArrayLens
    timing: Timing

# ProtocolFeatures class
class OptionalParameter(BaseModel):
    parameter: str
    support: SupportType
    description: Optional[str] = ""

class ActionParameter(BaseModel):
    key: str
    valueDataType: ValueDataType
    description: Optional[str] = ""
    isOptional: Optional[bool] = False

class AgvAction(BaseModel):
    actionType: str
    actionDescription: Optional[str] = ""
    actionScopes: List[ActionScope]
    actionParameters: List[ActionParameter] = []
    resultDescription: Optional[str] = ""

class ProtocolFeatures(BaseModel):
    optionalParameters: List[OptionalParameter]
    agvActions: List[AgvAction]

# AgvGeometry class
class Position(BaseModel):
    x: float
    y: float
    theta: Optional[float]

class WheelDefinition(BaseModel):
    type: WheelType
    isActiveDriven: bool
    isActiveSteered: bool
    position: Position
    diameter: float
    width: float
    centerDisplacement: Optional[float]
    constraints: Optional[str]

class PolygonPoint(BaseModel):
    x: float
    y: float

class Envelope2D(BaseModel):
    set: str
    polygonPoints: List[PolygonPoint]
    description: Optional[str] = ""

class Envelope3D(BaseModel):
    set: str
    format: str
    data: Optional[dict]
    url: Optional[str]
    description: Optional[str] = ""

class AgvGeometry(BaseModel):
    wheelDefinitions: List[WheelDefinition]
    envelopes2d: List[Envelope2D]
    envelopes3d: List[Envelope3D]

# LoadSpecification class
class BoundingBoxReference(BaseModel):
    x: float
    y: float
    z: float
    theta: Optional[float]

class LoadDimensions(BaseModel):
    length: float
    width: float
    height: Optional[float]

class LoadSet(BaseModel):
    setName: str
    loadType: str
    loadPositions: List[str] = []
    boundingBoxReference: BoundingBoxReference
    loadDimensions: LoadDimensions
    maxWeigth: float
    minLoadhandlingHeight: Optional[float]
    maxLoadhandlingHeight: Optional[float]
    minLoadhandlingDepth: Optional[float]
    maxLoadhandlingDepth: Optional[float]
    minLoadhandlingTilt: Optional[float]
    maxLoadhandlingTilt: Optional[float]
    agvSpeedLimit: Optional[float]
    agvAccelerationLimit: Optional[float]
    agvDecelerationLimit: Optional[float]
    pickTime: Optional[float]
    dropTime: Optional[float]
    description: Optional[str]

class LoadSpecification(BaseModel):
    loadPositions: Optional[List[str]] = []
    loadSets: List[LoadSet]

class FactSheet(BaseModel):
    version: str
    manufacturer: str
    serialNumber: str
    typeSpecification: TypeSpecification
    physicalParameters: PhysicalParameters
    protocolLimits: ProtocolLimits
    protocolFeatures: ProtocolFeatures
    agvGeometry: AgvGeometry
    loadSpecification: LoadSpecification
    headerId: Optional[int]
    timestamp: Optional[datetime] # Is datetime compatible with VDA5050's "date-time"?


    # Everything needed for State VDA5050

    # Enum classes for various string enumerations
class OperatingMode(str, Enum):
    AUTOMATIC = "AUTOMATIC"
    SEMIAUTOMATIC = "SEMIAUTOMATIC"
    MANUAL = "MANUAL"
    SERVICE = "SERVICE"
    TEACHIN = "TEACHIN"

class ActionStatus(str, Enum):
    WAITING = "WAITING"
    INITIALIZING = "INITIALIZING"
    RUNNING = "RUNNING"
    FINISHED = "FINISHED"
    FAILED = "FAILED"

class ErrorLevel(str, Enum):
    WARNING = "WARNING"
    FATAL = "FATAL"

class InfoLevel(str, Enum):
    INFO = "INFO"
    DEBUG = "DEBUG"

class EStopType(str, Enum):
    AUTOACK = "AUTOACK"
    MANUAL = "MANUAL"
    REMOTE = "REMOTE"
    NONE = "NONE"

# NodePosition class
class NodePosition(BaseModel):
    x: float
    y: float
    theta: float
    mapId: str

# NodeState class
class NodeState(BaseModel):
    nodeId: str
    sequenceId: int
    nodeDescription: Optional[str] = ""
    nodePosition: Optional[NodePosition]
    released: bool

# ControlPoint class
class ControlPoint(BaseModel):
    x: float
    y: float
    weight: Optional[float] = 1.0

# Trajectory class
class Trajectory(BaseModel):
    degree: int
    knotVector: List[float]
    controlPoints: List[ControlPoint]

# EdgeState class
class EdgeState(BaseModel):
    edgeId: str
    sequenceId: int
    edgeDescription: Optional[str] = ""
    released: bool
    trajectory: Optional[Trajectory]

# AgvPosition class
class AgvPosition(BaseModel):
    x: float
    y: float
    theta: float
    mapId: str
    positionInitialized: bool
    mapDescription: Optional[str] = ""
    localizationScore: Optional[float] = Field(None, ge=0.0, le=1.0)
    deviationRange: Optional[float]

# Velocity class
class Velocity(BaseModel):
    vx: Optional[float]
    vy: Optional[float]
    omega: Optional[float]

# BoundingBoxReference class
class BoundingBoxReference(BaseModel):
    x: float
    y: float
    z: float
    theta: Optional[float]

# LoadDimensions class
class LoadDimensions(BaseModel):
    length: float
    width: float
    height: Optional[float]

# Load class
class Load(BaseModel):
    loadId: Optional[str] = ""
    loadType: Optional[str] = ""
    loadPosition: Optional[str] = ""
    boundingBoxReference: Optional[BoundingBoxReference]
    loadDimensions: Optional[LoadDimensions]
    weight: Optional[float] = Field(None, ge=0.0)

# ActionState class
class ActionState(BaseModel):
    actionId: str
    actionType: Optional[str] = ""
    actionDescription: Optional[str] = ""
    actionStatus: ActionStatus
    resultDescription: Optional[str] = ""

# BatteryState class
class BatteryState(BaseModel):
    batteryCharge: float
    batteryVoltage: Optional[float]
    batteryHealth: Optional[float] = Field(None, ge=0, le=100)
    charging: bool
    reach: Optional[float] = Field(None, ge=0.0)

# ErrorReference class
class ErrorReference(BaseModel):
    referenceKey: str
    referenceValue: str

# Error class
class Error(BaseModel):
    errorType: str
    errorDescription: Optional[str] = ""
    errorLevel: ErrorLevel
    errorReferences: Optional[List[ErrorReference]] = []

# InfoReference class
class InfoReference(BaseModel):
    referenceKey: str
    referenceValue: str

# Information class
class Information(BaseModel):
    infoType: str
    infoDescription: Optional[str] = ""
    infoLevel: InfoLevel
    infoReferences: Optional[List[InfoReference]] = []

# SafetyState class
class SafetyState(BaseModel):
    eStop: EStopType
    fieldViolation: bool

# Main State class
class State(BaseModel):
    headerId: int
    timestamp: datetime
    version: str
    manufacturer: str
    serialNumber: str
    orderId: str
    orderUpdateId: int
    zoneSetId: Optional[str]
    lastNodeId: str
    lastNodeSequenceId: int
    driving: bool
    paused: Optional[bool]
    newBaseRequest: Optional[bool]
    distanceSinceLastNode: Optional[float]
    operatingMode: OperatingMode
    nodeStates: List[NodeState]
    edgeStates: List[EdgeState]
    agvPosition: Optional[AgvPosition]
    velocity: Optional[Velocity]
    loads: Optional[List[Load]]
    actionStates: List[ActionState]
    batteryState: BatteryState
    errors: List[Error]
    information: Optional[List[Information]] = []
    safetyState: SafetyState