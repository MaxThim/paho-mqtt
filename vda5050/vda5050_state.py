from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum
from datetime import datetime

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