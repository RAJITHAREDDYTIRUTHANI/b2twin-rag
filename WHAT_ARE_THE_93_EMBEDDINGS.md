# What Are the 93 Embeddings? 📊

## Quick Answer

**The 93 embeddings are vector representations of your 31 document chunks**, where some chunks create multiple embeddings.

**Each embedding = 1 piece of text converted into 384 numbers**

---

## 🔢 The Math

**Expected**: 31 documents × 1 embedding each = 31 embeddings  
**Actual**: 93 embeddings

**Why more?** Some document chunks might be:
- Split into multiple segments (if text is too long)
- Creating multiple embeddings for different parts
- Or there might be duplicates/updates

---

## 📝 What Each Embedding Represents

Each of the **93 embeddings** represents a **document chunk** - a piece of text from your sensor data. Here's what they cover:

### **1. Summary Embeddings (6 total)**
One for each sensor type:
- `temperature_summary` → Embedding #1
- `fan_direction_summary` → Embedding #2
- `fan_output_summary` → Embedding #3
- `fan_status_summary` → Embedding #4
- `valve_command_summary` → Embedding #5
- `valve_limit_summary` → Embedding #6

**What they represent:**
- High-level overview of each sensor
- Total readings, time range, value range

### **2. Sample Data Embeddings (~25 total)**
Five samples per sensor:
- `temperature_sample_0` through `temperature_sample_4` (5 embeddings)
- `fan_output_sample_0` through `fan_output_sample_4` (5 embeddings)
- Similar for other sensors with enough data

**What they represent:**
- Individual sensor reading examples
- Timestamp, value, status for each sample

### **3. Statistics Embeddings (6 total)**
One for each sensor:
- `temperature_statistics` → Embedding
- `fan_direction_statistics` → Embedding
- etc.

**What they represent:**
- Min/max/mean values
- Data quality information
- Statistical summaries

### **4. System Overview Embedding (1 total)**
- `system_overview` → Embedding

**What it represents:**
- Overall system summary
- Total sensors, total readings
- Monitoring period overview

---

## 🔍 How to See Your Actual Embeddings

Run this to see exactly what you have:

```python
import sqlite3

conn = sqlite3.connect('biosphere2_rag.db')
cursor = conn.cursor()

# Get all embeddings
cursor.execute('SELECT doc_id FROM embeddings ORDER BY doc_id')
embeddings = cursor.fetchall()

print(f"Total embeddings: {len(embeddings)}")
print("\nAll embedding document IDs:")
for i, (doc_id,) in enumerate(embeddings, 1):
    print(f"{i:2d}. {doc_id}")

conn.close()
```

---

## 📊 Breakdown by Type

Based on your code, here's the expected structure:

### **By Chunk Type:**
- **Summary chunks**: 6 (one per sensor)
- **Sample data chunks**: ~25 (5 samples × 5 sensors with data)
- **Statistics chunks**: 6 (one per sensor)
- **System overview**: 1
- **Total**: ~38 document chunks

### **Why 93 Embeddings?**

Possible reasons for 93 vs 31:
1. **Multiple embeddings per chunk** - Some long chunks might be split
2. **Duplicate entries** - Re-runs might have created duplicates
3. **Different versions** - Chunks updated/re-embedded
4. **Additional processing** - Extra embeddings for specific features

---

## 🎯 What Each Embedding Contains

### **Structure of Each Embedding:**

```
Embedding = {
    doc_id: "temperature_summary",
    embedding_vector: [0.234, -0.891, 0.445, ...],  # 384 numbers
    linked_to_document: "temperature_summary" document in SQLite
}
```

### **What the 384 Numbers Mean:**

Each embedding is a **384-dimensional vector** that represents:
- Semantic meaning of the text
- Relationships between concepts
- Context and associations
- All learned through the neural network model

---

## 💡 Example: Temperature Summary Embedding

**Document Chunk:**
```
"Temperature Sensor Summary:
- Total readings: 507
- Time range: 2025/09/21 00:00:01 to 2025/09/28 23:45:02
- Value range: 66.14°F to 86.38°F
- Sensor type: temperature"
```

**Embedding:**
```
[0.234, -0.891, 0.445, 0.123, -0.567, 0.789, ...]  # 384 numbers
```

**What it captures:**
- Temperature-related concepts (position 1: 0.234)
- Numerical values (position 2: -0.891)
- Range information (position 3: 0.445)
- Sensor context (position 4: 0.123)
- ... and 380 more semantic features

---

## 🔄 How They're Used

### **When you ask: "What's the temperature range?"**

1. **Query embedding created**: Your question → 384 numbers
2. **FAISS searches**: Compares against all 93 embeddings
3. **Finds matches**: Top 5 most similar embeddings
   - `temperature_summary` (score: 0.95) ✓
   - `temperature_statistics` (score: 0.87) ✓
   - `temperature_sample_0` (score: 0.72) ✓
   - etc.
4. **Retrieves documents**: Gets full text from SQLite for matched embeddings
5. **Context for AI**: Sends to Claude API with retrieved context

---

## 📈 Visual Representation

```
Your 93 Embeddings in FAISS Index:

[0] temperature_summary        → [0.234, -0.891, ...]
[1] temperature_statistics     → [0.231, -0.889, ...]
[2] temperature_sample_0       → [0.198, -0.856, ...]
[3] temperature_sample_1       → [0.201, -0.859, ...]
[4] temperature_sample_2       → [0.199, -0.857, ...]
[5] temperature_sample_3       → [0.202, -0.860, ...]
[6] temperature_sample_4       → [0.200, -0.858, ...]
[7] fan_output_summary         → [0.145, -0.234, ...]
[8] fan_output_statistics      → [0.142, -0.231, ...]
...
[92] system_overview           → [0.178, -0.456, ...]

Each is a 384-number "fingerprint" of that document's meaning!
```

---

## 🎓 Key Points

1. **93 embeddings = 93 pieces of text** converted to 384-number vectors
2. **Each represents a document chunk** from your sensor data
3. **Used for semantic search** - finding relevant information by meaning
4. **Stored in FAISS** for fast similarity search
5. **Linked to SQLite** for retrieving full document text

---

## 💬 Simple Explanation for Your Team

> "The 93 embeddings are semantic representations of our sensor data chunks. Each embedding is 384 numbers that capture the meaning of a piece of text - like a summary, sample data point, or statistics. When you ask a question, we convert your question to a 384-number vector, search through all 93 embeddings to find the most similar ones, then retrieve the actual text content to answer your question."

---

## 🔍 To Find Out Exactly What You Have

Check your database:

```python
import sqlite3

conn = sqlite3.connect('biosphere2_rag.db')
cursor = conn.cursor()

# Count by type
cursor.execute('''
    SELECT metadata FROM documents
''')
docs = cursor.fetchall()

# Group by sensor type
from collections import defaultdict
by_type = defaultdict(int)
by_chunk_type = defaultdict(int)

for (meta_json,) in docs:
    import json
    meta = json.loads(meta_json)
    by_type[meta.get('sensor_type', 'unknown')] += 1
    by_chunk_type[meta.get('chunk_type', 'unknown')] += 1

print("By sensor type:")
for sensor, count in by_type.items():
    print(f"  {sensor}: {count}")

print("\nBy chunk type:")
for chunk_type, count in by_chunk_type.items():
    print(f"  {chunk_type}: {count}")

conn.close()
```

This will show you exactly what your 93 embeddings represent!


