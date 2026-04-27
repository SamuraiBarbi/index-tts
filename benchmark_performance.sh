#!/bin/bash

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║         IndexTTS2 Performance Benchmark Test                ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Test texts of different lengths
SHORT_TEXT="Hello world, this is a test."
MEDIUM_TEXT="This is a medium length test to evaluate the performance of the optimized IndexTTS2 API. We expect significant improvements with FP16 and CUDA kernels enabled."
LONG_TEXT="This is a longer performance test to really push the system. The IndexTTS2 model has been optimized with FP16 precision and CUDA kernel acceleration. We should see approximately two to three times faster generation compared to the baseline configuration. This will help us understand the real-world performance gains."

echo -e "${BLUE}Testing API at http://localhost:8889${NC}"
echo ""

# Test 1: Health Check
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${YELLOW}Test 1: Health Check${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
curl -s http://localhost:8889/health | jq .
echo ""

# Test 2: Short Text (Warm-up)
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${YELLOW}Test 2: Warm-up (Short Text)${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Text: \"$SHORT_TEXT\""
echo ""

START=$(date +%s.%N)
curl -s -X POST "http://localhost:8889/v1/audio/speech" \
  -H "Authorization: Bearer test_token" \
  -H "Content-Type: application/json" \
  -d "{\"input\":\"$SHORT_TEXT\",\"voice\":\"alex\",\"response_format\":\"wav\"}" \
  --output /tmp/benchmark_warmup.wav
END=$(date +%s.%N)
WARMUP_TIME=$(echo "$END - $START" | bc)

if [ -f "/tmp/benchmark_warmup.wav" ] && [ -s "/tmp/benchmark_warmup.wav" ]; then
    SIZE=$(ls -lh /tmp/benchmark_warmup.wav | awk '{print $5}')
    echo -e "${GREEN}✅ Success${NC}"
    echo "Time: ${WARMUP_TIME}s"
    echo "Size: $SIZE"
else
    echo -e "${RED}❌ Failed${NC}"
fi
echo ""

# Test 3: Short Text (Actual Benchmark)
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${YELLOW}Test 3: Short Text Performance${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Text: \"$SHORT_TEXT\""
echo ""

START=$(date +%s.%N)
curl -s -X POST "http://localhost:8889/v1/audio/speech" \
  -H "Authorization: Bearer test_token" \
  -H "Content-Type: application/json" \
  -d "{\"input\":\"$SHORT_TEXT\",\"voice\":\"alex\",\"response_format\":\"wav\"}" \
  --output /tmp/benchmark_short.wav
END=$(date +%s.%N)
SHORT_TIME=$(echo "$END - $START" | bc)

if [ -f "/tmp/benchmark_short.wav" ] && [ -s "/tmp/benchmark_short.wav" ]; then
    SIZE=$(ls -lh /tmp/benchmark_short.wav | awk '{print $5}')
    echo -e "${GREEN}✅ Success${NC}"
    echo "Time: ${SHORT_TIME}s"
    echo "Size: $SIZE"
else
    echo -e "${RED}❌ Failed${NC}"
fi
echo ""

# Test 4: Medium Text
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${YELLOW}Test 4: Medium Text Performance${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Text length: ${#MEDIUM_TEXT} characters"
echo ""

START=$(date +%s.%N)
curl -s -X POST "http://localhost:8889/v1/audio/speech" \
  -H "Authorization: Bearer test_token" \
  -H "Content-Type: application/json" \
  -d "{\"input\":\"$MEDIUM_TEXT\",\"voice\":\"alex\",\"response_format\":\"wav\"}" \
  --output /tmp/benchmark_medium.wav
END=$(date +%s.%N)
MEDIUM_TIME=$(echo "$END - $START" | bc)

if [ -f "/tmp/benchmark_medium.wav" ] && [ -s "/tmp/benchmark_medium.wav" ]; then
    SIZE=$(ls -lh /tmp/benchmark_medium.wav | awk '{print $5}')
    DURATION=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 /tmp/benchmark_medium.wav 2>/dev/null)
    RTF=$(echo "scale=2; $MEDIUM_TIME / $DURATION" | bc)
    echo -e "${GREEN}✅ Success${NC}"
    echo "Generation time: ${MEDIUM_TIME}s"
    echo "Audio duration: ${DURATION}s"
    echo "RTF (Real-Time Factor): ${RTF}x"
    echo "Size: $SIZE"
else
    echo -e "${RED}❌ Failed${NC}"
fi
echo ""

# Test 5: Long Text
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${YELLOW}Test 5: Long Text Performance${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Text length: ${#LONG_TEXT} characters"
echo ""

START=$(date +%s.%N)
curl -s -X POST "http://localhost:8889/v1/audio/speech" \
  -H "Authorization: Bearer test_token" \
  -H "Content-Type: application/json" \
  -d "{\"input\":\"$LONG_TEXT\",\"voice\":\"alex\",\"response_format\":\"wav\"}" \
  --output /tmp/benchmark_long.wav
END=$(date +%s.%N)
LONG_TIME=$(echo "$END - $START" | bc)

if [ -f "/tmp/benchmark_long.wav" ] && [ -s "/tmp/benchmark_long.wav" ]; then
    SIZE=$(ls -lh /tmp/benchmark_long.wav | awk '{print $5}')
    DURATION=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 /tmp/benchmark_long.wav 2>/dev/null)
    RTF=$(echo "scale=2; $LONG_TIME / $DURATION" | bc)
    echo -e "${GREEN}✅ Success${NC}"
    echo "Generation time: ${LONG_TIME}s"
    echo "Audio duration: ${DURATION}s"
    echo "RTF (Real-Time Factor): ${RTF}x"
    echo "Size: $SIZE"
else
    echo -e "${RED}❌ Failed${NC}"
fi
echo ""

# Test 6: With Emotion
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${YELLOW}Test 6: With Emotion Control${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Text: \"I'm so excited about these performance improvements!\""
echo "Emotion: happy and excited"
echo ""

START=$(date +%s.%N)
curl -s -X POST "http://localhost:8889/v1/audio/speech" \
  -H "Authorization: Bearer test_token" \
  -H "Content-Type: application/json" \
  -d '{"input":"I am so excited about these performance improvements!","voice":"alex","emotion_text":"happy and excited","emotion_weight":0.8,"response_format":"wav"}' \
  --output /tmp/benchmark_emotion.wav
END=$(date +%s.%N)
EMOTION_TIME=$(echo "$END - $START" | bc)

if [ -f "/tmp/benchmark_emotion.wav" ] && [ -s "/tmp/benchmark_emotion.wav" ]; then
    SIZE=$(ls -lh /tmp/benchmark_emotion.wav | awk '{print $5}')
    echo -e "${GREEN}✅ Success${NC}"
    echo "Time: ${EMOTION_TIME}s"
    echo "Size: $SIZE"
else
    echo -e "${RED}❌ Failed${NC}"
fi
echo ""

# Summary
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                    Performance Summary                      ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""
echo "Short text:    ${SHORT_TIME}s"
echo "Medium text:   ${MEDIUM_TIME}s (RTF: ${RTF}x)"
echo "Long text:     ${LONG_TIME}s"
echo "With emotion:  ${EMOTION_TIME}s"
echo ""
echo -e "${GREEN}✅ All benchmarks complete!${NC}"
echo ""
echo "Generated files in /tmp/benchmark_*.wav"
echo "To play: aplay /tmp/benchmark_medium.wav"

# Cleanup
rm -f /tmp/benchmark_*.wav
