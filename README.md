# Galatiq Case Study: Invoice Processing Automation

## Overview

This project is an end-to-end invoice processing system that combines AI-driven extraction with deterministic validation to automate a traditionally manual workflow.

The system processes invoices end-to-end by:
1. Parsing invoice files from local storage  
2. Extracting structured invoice data using xAI's Grok  
3. Validating invoice contents against a local SQLite inventory database  
4. Making an approval decision using an AI approval agent  
5. Running a critique/self-check loop on the approval decision  
6. Processing mock payment for approved invoices or skipping payment for rejected ones  
7. Logging the final result for traceability  

---

## Problem Statement

Acme Corp currently handles invoices manually. Invoices arrive in messy formats, data extraction is error-prone, validation is slow, approvals happen through manual review, and payments are delayed.

This creates:
- High error rates  
- Slow processing times  
- Operational frustration  
- Risk of incorrect approvals or payments  

This prototype addresses that by introducing a workflow-first multi-agent system.

---

## System Design

The workflow is:

Invoice File -> Parser -> Extraction Agent -> Validation Layer -> Approval Agent -> Critique Loop -> Payment / Rejection -> Logging

This hybrid approach ensures that AI is used for reasoning, while critical business logic remains deterministic.

### Why this design

- Parser is deterministic because file reading should be reliable and reproducible  
- Extraction Agent uses Grok because invoice formats are messy and unstructured, requiring interpretation  
- Validation Layer is deterministic because inventory checks and business rules should be explicit and testable  
- Approval Agent uses Grok because final decision-making benefits from reasoning and explanation  
- Critique Loop reviews the approval decision to ensure it is consistent with invoice data and validation results  
- Payment and Logging are deterministic because execution and traceability should be predictable  

This separation keeps the system modular, easy to debug, and aligned with real-world workflow design.

---

## Components

### 1. Parser (core/parser.py)
Reads invoice files and converts them into raw text.

Supported formats:
- TXT  
- JSON  
- CSV  
- PDF  
- XML  

### 2. Extraction Agent (agents/extraction_agent.py)
Uses Grok to extract structured fields from messy invoice text.

Extracted fields:
- invoice_id  
- vendor  
- amount  
- due_date  
- items  

### 3. Schema (core/schema.py)
Defines the expected invoice structure and checks for missing required fields.

### 4. Validation Layer (core/validator.py)
Validates extracted invoice data against:
- required fields  
- positive quantities  
- item existence in SQLite inventory  
- stock availability  

### 5. Approval Agent (agents/approval_agent.py)
Uses Grok to decide whether an invoice should be approved, rejected, or escalated.

### 6. Critique Loop
Validates whether the approval decision is consistent with validation and extracted data.

### 7. Payment Layer (core/payment.py)
Simulates payment for approved invoices.

### 8. Logging (core/logger.py)
Writes structured logs to run_log.jsonl.

### 9. Orchestrator (core/orchestrator.py)
Coordinates the entire workflow.

---

## Tech Stack

- Python  
- xAI Grok API  
- SQLite  
- requests  
- python-dotenv  
- PyMuPDF  

---

## How to Run

### 1. Install dependencies
```bash
pip3 install -r requirements.txt
```

### 2. Setup database
```bash
python3 setup_db.py
```

### 3. Run pipeline
```bash
python3 main.py --invoice data/invoices/invoice_1001.txt
```

---

## Bulk Testing

The pipeline was tested across all provided sample invoices.

Full bulk test output is available in:
`bulk_test_output.txt`

## System Robustness

The system includes safeguards to handle LLM and data inconsistencies:

- Extraction retry mechanism for invalid JSON responses
- Critique feedback loop to verify approval consistency
- Deterministic validation layer to enforce business rules before execution

## Design Considerations

In a production setting, the system can be extended with:
- invoice history for duplicate and revision detection
- normalization for item and vendor naming variations
- a human-in-the-loop workflow for escalated invoices