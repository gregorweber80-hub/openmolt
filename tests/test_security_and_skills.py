from openmolt.core.security import SecurityPolicy
from openmolt.services.skills import SkillRegistry


def test_security_policy_allows_only_allowlist_in_secure_mode() -> None:
    policy = SecurityPolicy(mode="secure", require_explicit_send_approval=True, allowed_domains={"example.com"})
    assert policy.can_visit("https://example.com/path")
    assert not policy.can_visit("https://openai.com")


def test_send_requires_approval() -> None:
    policy = SecurityPolicy(mode="secure", require_explicit_send_approval=True, allowed_domains={"example.com"})
    assert not policy.can_send_mail(approved=False)
    assert policy.can_send_mail(approved=True)


def test_skill_registry_loads_example_skill() -> None:
    reg = SkillRegistry("openmolt/skills")
    reg.load()
    assert "echo" in reg.skills
    assert reg.execute("echo", "hallo") == "[echo-skill] hallo"
