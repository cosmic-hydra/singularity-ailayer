# Architecture Overview

## System Components

```
singularity-ailayer/
├── core/                    # Core application modules
│   ├── assistant.py         # Main GUI and assistant interface
│   ├── driver.py            # Action execution engine
│   ├── config.py            # Configuration management
│   ├── core_api.py          # OpenAI API integration
│   ├── core_imaging.py      # Vision/screenshot analysis
│   ├── voice.py             # Text-to-speech functionality
│   ├── ocr.py               # Optical character recognition
│   ├── window_elements.py   # UI element analysis
│   ├── window_focus.py      # Window management
│   └── logging_config.py    # Structured logging
├── tests/                   # Test suite
├── docs/                    # Documentation
└── .github/workflows/       # CI/CD pipelines
```

## Data Flow

1. **User Input** → Voice recognition or text input
2. **Intent Analysis** → OpenAI API processes the goal
3. **Action Generation** → AI generates JSON action sequence
4. **UI Analysis** → Window elements and screenshots analyzed
5. **Action Execution** → pyautogui/pywinauto execute actions
6. **Feedback Loop** → Vision analysis verifies success

## Key Design Decisions

### Configuration
- Environment-based configuration using Pydantic
- Supports `.env` files for local development
- Type-safe settings with validation

### Logging
- Structured logging with structlog
- JSON output for production, colored console for development
- Contextual logging with request tracking

### Testing
- pytest for unit and integration tests
- Mocked external dependencies (OpenAI, UI automation)
- Windows-specific tests run on Windows runners

## Extension Points

- **Custom Actions**: Add new action types in `driver.py`
- **App Space Maps**: Add application-specific knowledge
- **Voice Commands**: Extend voice command patterns
