#!/bin/bash
# Demo queries for MedReg MCP FastAPI endpoint
# Run the server first: uvicorn app.main:app --reload

BASE_URL="http://localhost:8000"

echo "=== Health Check ==="
curl -s "$BASE_URL/health" | python -m json.tool
echo ""

echo "=== Query 1: FDA AI/ML Guidance ==="
curl -s -X POST "$BASE_URL/ask" \
  -H "Content-Type: application/json" \
  -d '{"question": "What does FDA say about AI/ML-enabled medical devices?"}' | python -m json.tool
echo ""

echo "=== Query 2: WHO Ethics ==="
curl -s -X POST "$BASE_URL/ask" \
  -H "Content-Type: application/json" \
  -d '{"question": "What does WHO recommend for ethical AI in health?"}' | python -m json.tool
echo ""

echo "=== Query 3: Safety Trigger (Medical Advice) ==="
curl -s -X POST "$BASE_URL/ask" \
  -H "Content-Type: application/json" \
  -d '{"question": "Should this patient receive treatment A or treatment B?"}' | python -m json.tool
echo ""

echo "=== Query 4: Predetermined Change Control ==="
curl -s -X POST "$BASE_URL/ask" \
  -H "Content-Type: application/json" \
  -d '{"question": "What is a predetermined change control plan?"}' | python -m json.tool
echo ""
