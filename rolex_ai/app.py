from .config import DB_PATH, EXTERNAL_AI_DISABLED, ALLOW_NETWORK
from .storage.db import Database
from .core.memory import MemoryManager
from .core.router import CommandRouter
from .core.brain import LocalBrain
from .security.policy import SecurityPolicy
from .tools import ToolHub
from .knowledge.base import LocalKnowledge
from .voice.voice_manager import VoiceManager
from .voice.android_voice import AndroidSTT, AndroidTTS, android_available
from .vision.vision_manager import VisionManager
from .automation.scheduler import Scheduler
from .core.autonomous_intelligence import AutonomousIntelligence
from .core.autonomous_controller import AutonomousController
from .core.web_intelligence import WebIntelligence
from .core.self_repair import SelfRepairEngine
from .communication import CommunicationGateway
from .android.device_gateway import AndroidDeviceGateway
from .core.v20_26_platform import SmartHomeManager, FinanceBusinessManager, BackupSyncManager, SecurityHardeningManager, RemoteGatewayManager, ReliabilityManager, ProductionManager
from .core.system_integration_v27 import SystemIntegrationV27
from .core.watchdog_v28 import WatchdogV28
from .core.autonomous_scheduler_v29 import AutonomousSchedulerV29
from .core.v30_v35_runtime import AndroidRuntimeV30, DeviceIntegrationV31, LocalConnectorContractsV32, LearningLoopV33, SoakHarnessV34, ReleaseGateV35
from .core.v36_deep_core import DeepCoreV36

class RolexAI:
    def __init__(self):
        self.db = Database(DB_PATH)
        self.policy = SecurityPolicy(local_only=EXTERNAL_AI_DISABLED, allow_external_ai=False)
        self.memory = MemoryManager(self.db)
        self.router = CommandRouter()
        self.tools = ToolHub(self.db, DB_PATH)
        self.knowledge = LocalKnowledge()
        self.voice = VoiceManager()
        if android_available():
            self.voice.configure(listener=AndroidSTT(), speaker=AndroidTTS(), enabled=False)
        self.vision = VisionManager(root_dir=DB_PATH.parent.parent)
        self.scheduler = Scheduler(self.db)
        self.web = WebIntelligence(allow_network=ALLOW_NETWORK)
        self.self_repair = SelfRepairEngine(root_dir=DB_PATH.parent.parent, db=self.db, policy=self.policy)
        self.android = AndroidDeviceGateway(root_dir=DB_PATH.parent.parent)
        self.communication = CommunicationGateway(android=self.android)
        root = DB_PATH.parent.parent
        self.smart_home = SmartHomeManager(db=self.db)
        self.finance_business = FinanceBusinessManager(db=self.db)
        self.sync_backup = BackupSyncManager(root)
        self.security_hardening = SecurityHardeningManager(db=self.db)
        self.remote_gateway = RemoteGatewayManager()
        self.reliability = ReliabilityManager(db=self.db)
        self.production = ProductionManager(root)
        self.system_integration = SystemIntegrationV27(app=self, db=self.db, root=root)
        self.watchdog = WatchdogV28(system=self.system_integration, db=self.db)
        self.autonomous_scheduler = AutonomousSchedulerV29(db=self.db)
        self.autonomous_scheduler.register("watchdog", lambda: self.watchdog.run(recover=True))
        self.autonomous_scheduler.register("system_health", lambda: self.system_integration.check())
        self.autonomous_scheduler.add_job("watchdog", 300.0)
        self.autonomous_scheduler.add_job("system_health", 600.0)
        self.android_runtime = AndroidRuntimeV30(scheduler=self.autonomous_scheduler, watchdog=self.watchdog, db=self.db)
        self.device_integration = DeviceIntegrationV31(self.android)
        self.connector_contracts = LocalConnectorContractsV32(app=self)
        self.learning_loop = LearningLoopV33(db=self.db, memory=self.memory, knowledge=self.knowledge)
        self.soak_harness = SoakHarnessV34(system=self.system_integration, watchdog=self.watchdog, scheduler=self.autonomous_scheduler)
        self.release_gate = ReleaseGateV35(root, production=self.production)
        self.deep_core = DeepCoreV36(app=self, db=self.db, root=root)
        self.autonomous_engine = AutonomousIntelligence(db=self.db, memory=self.memory, personal=None, planner=self.tools.tasks, task_manager=self.tools.tasks, scheduler=self.scheduler, policy=self.policy, diagnostics=self.tools.diagnostics)
        self.autonomous = AutonomousController(engine=self.autonomous_engine, db=self.db, policy=self.policy)
        self.brain = LocalBrain(self.db, self.memory, self.router, self.tools, autonomous=self.autonomous)
        self.autonomous_engine.personal = self.brain.personal
        self.brain.attach_voice(self.voice); self.brain.attach_vision(self.vision); self.brain.attach_web(self.web); self.brain.attach_self_repair(self.self_repair); self.brain.attach_communication(self.communication)
        self.brain.multi_agent.web = self.web; self.brain.multi_agent.vision = self.vision; self.brain.multi_agent.android = self.android; self.brain.multi_agent.communication = self.communication
        ex = self.brain.autonomous_executor
        for name, value in {"communication":self.communication,"smart_home":self.smart_home,"finance_business":self.finance_business,"sync_backup":self.sync_backup,"security_hardening":self.security_hardening,"remote_gateway":self.remote_gateway,"reliability":self.reliability,"production":self.production,"system_integration":self.system_integration,"watchdog":self.watchdog,"autonomous_scheduler":self.autonomous_scheduler,"android_runtime":self.android_runtime,"device_integration":self.device_integration,"connector_contracts":self.connector_contracts,"learning_loop":self.learning_loop,"soak_harness":self.soak_harness,"release_gate":self.release_gate,"multi_agent":self.brain.multi_agent}.items(): setattr(ex, name, value)
        for name, value in {"autonomous_scheduler":self.autonomous_scheduler,"android_runtime":self.android_runtime,"device_integration":self.device_integration,"connector_contracts":self.connector_contracts,"learning_loop":self.learning_loop,"soak_harness":self.soak_harness,"release_gate":self.release_gate,"deep_core":self.deep_core,"watchdog":self.watchdog,"system_integration":self.system_integration}.items(): setattr(self.brain, name, value)

    def ask(self, text):
        return self.brain.answer(text)

    def voice_once(self):
        return self.voice.run_once(self.brain)

    def configure_voice(self, *, listener=None, speaker=None, enabled=None):
        return self.voice.configure(listener=listener, speaker=speaker, enabled=enabled)

    def status(self):
        return {"app":"ROLEX AI", "policy":self.policy.status(), "voice":self.voice.status(), "database":self.tools.diagnostics.check(), "modules":{"brain":True,"memory":True,"personal_intelligence":True,"math":True,"tasks":True,"documents":True,"knowledge":True,"automation_core":True,"autonomous_intelligence":True,"android":True,"vision":True,"voice":True,"web":True,"self_repair":True,"communication":True,"smart_home":True,"finance_business":True,"backup_sync":True,"security":True,"remote_gateway":True,"reliability":True,"production":True,"deep_core":True}}
