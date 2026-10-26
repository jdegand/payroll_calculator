# Payroll Calculation Engine

A modular Python-based payroll processing and tax calculation engine designed to handle complex multi-jurisdictional tax rules, deductions, and wage garnishments using the Strategy design pattern.

## Features

* **Core Payroll Engine**: Processes gross-to-net calculations using robust validation rules and data models.
* **Dynamic Tax Strategies**: Uses a factory pattern to dynamically apply federal and state-specific tax calculations (including New Jersey and Pennsylvania).
* **Flexible Deductions & Garnishments**: Dedicated services to isolate and apply post-tax deductions and court-ordered garnishments.
* **Multi-Jurisdictional Architecture**: Easily extendable to support new state or local tax rules without modifying core engine logic.

## Project Structure

```text
├── app
│   ├── core                     # Core data models, validation, and main payroll engine
│   │   ├── jurisdiction_rules.py
│   │   ├── models.py
│   │   ├── payroll_engine.py
│   │   └── validators.py
│   ├── main.py                  # Application entry point
│   ├── services                 # Post-tax modifications and legal withholdings
│   │   ├── deduction_service.py
│   │   └── garnishment_service.py
│   └── strategies               # Extensible tax calculation algorithms
│       ├── base_tax_strategy.py # Interface for all tax strategies
│       ├── factory.py           # Dynamically resolves which tax strategy to use
│       ├── federal_tax.py
│       └── state                # State-specific tax compliance files
│           ├── nj_tax.py
│           └── pa_tax.py
```

## Getting Started

Follow these steps from the project **root** directory to set up your environment and run the payroll processor.

### 1. Set Up Environment

```bash
        # Create a virtual environment
        python3 -m venv .venv

        # Activate it (macOS/Linux)
        source .venv/bin/activate

        # Activate it (Windows PowerShell)
        # .venv\Scripts\Activate.ps1
```

### 2. Install Requirements

```bash
    pip3 install -r requirements.txt
```

### 3. Run the Payroll Processor

```bash
    python3 -m app.main
```
