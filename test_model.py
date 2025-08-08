# Файл: C:\desk_agent\test_model.py

print("--- Starting standalone model test ---")
try:
    from sentence_transformers import SentenceTransformer
    print("[OK] Library imported successfully.")

    # Используем тот же локальный путь, что и в основном приложении
    model_path = './models/all-MiniLM-L6-v2'
    print(f"--> Loading model from: {model_path}")

    model = SentenceTransformer(model_path)
    print("[OK] Model loaded successfully.")

    test_sentence = "Это тестовое предложение для кодирования."
    print(f"--> Encoding sentence: '{test_sentence}'")

    # ЭТО ТА САМАЯ ОПЕРАЦИЯ, КОТОРАЯ ПРЕДПОЛОЖИТЕЛЬНО ВЫЗЫВАЕТ СБОЙ
    embedding = model.encode(test_sentence)

    print("[SUCCESS] Sentence encoded successfully!")
    print(f"      Embedding shape: {embedding.shape}")

except Exception as e:
    print("\n--- CAUGHT A PYTHON EXCEPTION ---")
    import traceback
    traceback.print_exc()

print("\n--- Test finished ---")