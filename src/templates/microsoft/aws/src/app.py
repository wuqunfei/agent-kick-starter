from config import Settings

def run():
    s = Settings()
    print(f"{s.agent_name}: Hello from microsoft on {s.model_provider or 'unknown'} using {s.model_name}")

if __name__ == "__main__":
    run()