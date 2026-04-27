# AI Content Recommender v1.0
from enum import Enum
from typing import Dict, List, Any

class ContentType(Enum):
    REPORT = "report"
    MEETING = "meeting"  
    PLAN = "plan"
    ANALYSIS = "analysis"
    BUDGET = "budget"
    UNKNOWN = "unknown"

class ContentAnalyzer:
    KEYWORDS = {
        ContentType.REPORT: ["report", "summary"],
        ContentType.MEETING: ["meeting", "minutes"],
        ContentType.PLAN: ["plan", "planning"],
        ContentType.ANALYSIS: ["analysis", "research"],
        ContentType.BUDGET: ["budget", "cost"],
    }
    
    @classmethod
    def analyze(cls, text: str) -> ContentType:
        text_lower = text.lower()
        scores = {}
        for ct, kws in cls.KEYWORDS.items():
            score = sum(1 for kw in kws if kw in text_lower)
            if score > 0:
                scores[ct] = score
        return max(scores, key=scores.get) if scores else ContentType.UNKNOWN

def analyze_content(text: str) -> Dict[str, Any]:
    ct = ContentAnalyzer.analyze(text)
    return {
        "type": ct,
        "type_name": ct.value,
        "recommendation": {
            "template_name": f"{ct.value}_template",
            "confidence": 0.8,
            "structure": ["Intro", "Main", "Conclusion"]
        }
    }