import sqlite3

conn = sqlite3.connect('biosphere2_rag.db')
cursor = conn.cursor()

# Count embeddings
cursor.execute('SELECT COUNT(*) FROM embeddings')
embedding_count = cursor.fetchone()[0]
print(f'Total embeddings: {embedding_count}')

# Count documents
cursor.execute('SELECT COUNT(*) FROM documents')
doc_count = cursor.fetchone()[0]
print(f'Total documents: {doc_count}')

# List all document IDs
cursor.execute('SELECT doc_id FROM documents ORDER BY doc_id')
doc_ids = cursor.fetchall()
print(f'\nAll {len(doc_ids)} document IDs:')
for i, (doc_id,) in enumerate(doc_ids, 1):
    print(f'{i:2d}. {doc_id}')

conn.close()


