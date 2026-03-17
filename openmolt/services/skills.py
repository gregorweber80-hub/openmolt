from __future__ import annotations

import importlib.util
from pathlib import Path
from typing import Protocol


class Skill(Protocol):
    name: str

    def run(self, text: str) -> str: ...


class SkillRegistry:
    def __init__(self, skills_dir: str = "openmolt/skills") -> None:
        self.skills_dir = Path(skills_dir)
        self.skills: dict[str, Skill] = {}

    def load(self) -> None:
        self.skills.clear()
        for file in self.skills_dir.glob("*.py"):
            if file.name.startswith("__"):
                continue
            spec = importlib.util.spec_from_file_location(file.stem, file)
            if not spec or not spec.loader:
                continue
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            skill = getattr(module, "skill", None)
            if skill and getattr(skill, "name", None):
                self.skills[skill.name] = skill

    def execute(self, name: str, text: str) -> str:
        skill = self.skills.get(name)
        if not skill:
            return f"Skill '{name}' not found."
        return skill.run(text)
