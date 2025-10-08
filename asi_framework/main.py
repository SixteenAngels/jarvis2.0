from core import Brain, Memory, LLMInterface, Router, Logger, Config


def demo() -> None:
    cfg = Config()
    cfg.load_config()
    memory = Memory()
    router = Router()
    llm = LLMInterface(
        remote_enabled=True,
        local_enabled=True,
        default_remote_model=cfg.get("REMOTE_LLM", "gpt-5"),
        default_local_model=cfg.get("LOCAL_LLM", "local-llm"),
    )
    logger = Logger()

    # Register a trivial general agent handler
    router.register_agent("general", lambda task: {"echo": task})

    brain = Brain(memory=memory, router=router, llm=llm, logger=logger)
    result = brain.process_task({"goal": "Design a smart biomedical sensor.", "agent": "general"})
    print(result)


if __name__ == "__main__":
    demo()

