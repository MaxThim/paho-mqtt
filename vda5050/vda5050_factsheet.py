from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum
from datetime import datetime

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
