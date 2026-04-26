#!/bin/bash

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║         IndexTTS2 API - Comprehensive Test Suite            ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test counter
PASSED=0
FAILED=0

# Test 1: Health Check
echo "Test 1: Health Check"
echo "--------------------"
RESPONSE=$(curl -s http://localhost:8000/health)
if echo "$RESPONSE" | grep -q '"status":"ok"'; then
    echo -e "${GREEN}✅ PASSED${NC} - Health check successful"
    echo "$RESPONSE" | jq .
    ((PASSED++))
else
    echo -e "${RED}❌ FAILED${NC} - Health check failed"
    echo "$RESPONSE"
    ((FAILED++))
fi
echo ""

# Test 2: WAV Generation
echo "Test 2: WAV Generation"
echo "----------------------"
HTTP_CODE=$(curl -s -o test_wav.wav -w "%{http_code}" \
  -X POST "http://localhost:8000/v1/audio/speech" \
  -H "Authorization: Bearer test_token" \
  -H "Content-Type: application/json" \
  -d '{"input":"Hello world, this is a WAV test.","voice":"alex","response_format":"wav"}')

if [ "$HTTP_CODE" = "200" ] && [ -f "test_wav.wav" ] && [ -s "test_wav.wav" ]; then
    echo -e "${GREEN}✅ PASSED${NC} - WAV generation successful"
    ls -lh test_wav.wav
    file test_wav.wav
    ((PASSED++))
else
    echo -e "${RED}❌ FAILED${NC} - WAV generation failed (HTTP $HTTP_CODE)"
    ((FAILED++))
fi
echo ""

# Test 3: MP3 Generation
echo "Test 3: MP3 Generation"
echo "----------------------"
HTTP_CODE=$(curl -s -o test_mp3.mp3 -w "%{http_code}" \
  -X POST "http://localhost:8000/v1/audio/speech" \
  -H "Authorization: Bearer test_token" \
  -H "Content-Type: application/json" \
  -d '{"input":"Hello world, this is an MP3 test.","voice":"alex","response_format":"mp3"}')

if [ "$HTTP_CODE" = "200" ] && [ -f "test_mp3.mp3" ] && [ -s "test_mp3.mp3" ]; then
    echo -e "${GREEN}✅ PASSED${NC} - MP3 generation successful"
    ls -lh test_mp3.mp3
    file test_mp3.mp3
    ((PASSED++))
else
    echo -e "${RED}❌ FAILED${NC} - MP3 generation failed (HTTP $HTTP_CODE)"
    ((FAILED++))
fi
echo ""

# Test 4: Python Client (WAV)
echo "Test 4: Python Client (WAV)"
echo "---------------------------"
if python api_client_example.py --text "Python client WAV test" --voice alex --format wav --output client_wav.wav 2>&1 | grep -q "✅"; then
    if [ -f "client_wav.wav" ] && [ -s "client_wav.wav" ]; then
        echo -e "${GREEN}✅ PASSED${NC} - Python client WAV test successful"
        ls -lh client_wav.wav
        ((PASSED++))
    else
        echo -e "${RED}❌ FAILED${NC} - File not created"
        ((FAILED++))
    fi
else
    echo -e "${RED}❌ FAILED${NC} - Python client failed"
    ((FAILED++))
fi
echo ""

# Test 5: Python Client (MP3)
echo "Test 5: Python Client (MP3)"
echo "---------------------------"
if python api_client_example.py --text "Python client MP3 test" --voice alex --format mp3 --output client_mp3.mp3 2>&1 | grep -q "✅"; then
    if [ -f "client_mp3.mp3" ] && [ -s "client_mp3.mp3" ]; then
        echo -e "${GREEN}✅ PASSED${NC} - Python client MP3 test successful"
        ls -lh client_mp3.mp3
        ((PASSED++))
    else
        echo -e "${RED}❌ FAILED${NC} - File not created"
        ((FAILED++))
    fi
else
    echo -e "${RED}❌ FAILED${NC} - Python client failed"
    ((FAILED++))
fi
echo ""

# Summary
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                      Test Summary                            ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""
echo -e "${GREEN}Passed: $PASSED${NC}"
echo -e "${RED}Failed: $FAILED${NC}"
echo ""

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}🎉 All tests passed!${NC}"
    echo ""
    echo "Generated files:"
    ls -lh test_*.wav test_*.mp3 client_*.wav client_*.mp3 2>/dev/null
    exit 0
else
    echo -e "${RED}❌ Some tests failed${NC}"
    exit 1
fi
