#!/usr/bin/env python3
"""ROLEX AI application entry point.

Android/Kivy launches the cinematic UI. Non-Android/headless environments keep
the CLI so the core remains easy to test and operate from Termux.
"""
import os


def main():
    use_ui = os.environ.get("ROLEX_UI", "1") == "1"
    if use_ui:
        try:
            from rolex_ai.ui.rolex_ui import KIVY_AVAILABLE, RolexApp
            if KIVY_AVAILABLE:
                from rolex_ai.app import RolexAI
                RolexApp(core_factory=RolexAI).run()
                return
        except Exception as exc:
            print(f"ROLEX UI unavailable, falling back to CLI: {exc}")

    from rolex_ai.app import RolexAI
    rolex = RolexAI()
    print("ROLEX AI CORE 1.0")
    print("Local-first core online. Type 'exit' to quit.")
    while True:
        try:
            text = input("\nYOU: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nROLEX: Shutdown.")
            break
        if text.lower() in {"exit", "quit", "shutdown"}:
            print("ROLEX: Shutdown.")
            break
        print("ROLEX:", rolex.ask(text))


if __name__ == "__main__":
    main()
