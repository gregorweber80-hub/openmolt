class EchoSkill:
    name = "echo"

    def run(self, text: str) -> str:
        return f"[echo-skill] {text}"


skill = EchoSkill()
