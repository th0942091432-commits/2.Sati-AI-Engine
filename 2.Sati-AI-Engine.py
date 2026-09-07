from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum

class Path(Enum):
    REFUSE = "sila_block"      # ศีล — ไม่ตอบ
    FAST = "fast"
    DELIBERATE = "deliberate"

@dataclass
class Claim:
    text: str
    evidence: list = field(default_factory=list)
    confidence: float = 0.0

@dataclass
class Response:
    claims: list[Claim]
    def render(self) -> str: ...

class SatiPassaddhiAI(ABC):
    def __init__(self, cfg):
        self.cfg = cfg                    # threshold แยกออกมา calibrate ได้

    def process(self, user_input, history=None):
        signal = self.sati_eval(user_input, history)   # สติต่อเนื่อง ไม่ใช่ครั้งเดียว

        # ชั้นศีล — มาก่อนเสมอ
        if signal.harm > self.cfg.harm_max:
            return self.compassionate_refusal(signal)

        # 2 แกนอิสระ ไม่ใช่ AND เดียว
        path = Path.DELIBERATE if signal.epistemic_risk > self.cfg.risk else Path.FAST
        resp = self.generate(user_input, path)

        # ปัสสัทธิ — ทุก path ไม่เว้น fast
        resp = self.passaddhi(resp)
        resp = self.samadhi_check(resp)                # ความสอดคล้องภายใน

        return self.right_speech_gate(resp, signal)

    def passaddhi(self, resp: Response) -> Response:
        for c in resp.claims:
            c.confidence = self.causal_trace(c)        # อิทัปปัจจยตา
            if c.confidence < self.cfg.tau_drop:
                c.text = None                          # ตัดทิ้ง + log
            elif c.confidence < self.cfg.tau_hedge:
                c.text = self.mark_uncertain(c.text)   # ไม่ลบ แต่บอกว่าไม่แน่ใจ
        return resp

    def right_speech_gate(self, resp, signal):
        t = resp.render()
        t = self.no_falsehood(t)      # มุสาวาท
        t = self.no_divisive(t)       # ปิสุณวาจา
        t = self.no_idle_talk(t)      # สัมผัปปลาปะ — คุมความยาว
        if signal.agitation > self.cfg.agitation:
            t = self.gentle_tone(t)   # ผรุสวาจา
            t = self.upekkha_guard(t) # กันไม่ให้กลายเป็นเออออ
        return t