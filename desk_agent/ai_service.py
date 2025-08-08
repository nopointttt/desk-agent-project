# Файл: desk_agent/desk_agent/ai_service.py

import os
import json
from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot
import tools
import openai

class AIService(QObject):
    create_frame_signal = pyqtSignal(dict)
    
    def __init__(self):
        super().__init__()
        self.client = None
        self.tools_map = {}
        print("[AI Service] Cоздан, ожидает инициализации в потоке.")

    @pyqtSlot()
    def initialize(self):
        """Инициализация API клиента в фоновом потоке."""
        print("[AI Service] Начало инициализации...")
        try:
            api_key = os.environ.get("OPENAI_API_KEY")
            if not api_key:
                print("[AI Service] ОШИБКА: Переменная окружения OPENAI_API_KEY не найдена.")
                return
            
            self.client = openai.OpenAI(api_key=api_key)
            self.tools_map = {tool["name"]: tool["function"] for tool in tools.TOOLS}
            print("[AI Service] Инициализация завершена. Готов к работе.")
        except Exception as e:
            print(f"[AI Service] Ошибка при инициализации OpenAI клиента: {e}")

    def _prepare_prompt(self, command: str) -> str:
        """Готовит системный промпт для LLM с описанием инструментов и их параметров."""
        tools_with_params_description = []
        for tool in tools.TOOLS:
            params_str = ", ".join([f"{p['name']}: {p['type']}" for p in tool.get('parameters', [])])
            tools_with_params_description.append(
                f"- {tool['name']}({params_str}): {tool['description']}\n"
            )
        
        prompt = f"""
        Ты - ИИ-ассистент, управляющий десктоп-приложением. Твоя задача - проанализировать команду пользователя, выбрать один инструмент из списка и извлечь из команды параметры для этого инструмента.
        Ответь ТОЛЬКО в формате JSON, содержащем "tool_name" и "parameters".

        Пример ответа:
        {{
          "tool_name": "create_text_frame",
          "parameters": {{
            "title": "Заголовок из команды",
            "content": "Содержимое заметки из команды"
          }}
        }}

        Доступные инструменты:
        {''.join(tools_with_params_description)}

        Команда пользователя: "{command}"
        """
        return prompt

    def execute_command(self, command: str):
        """Использует LLM для выбора инструмента, извлечения параметров и выполнения."""
        if not self.client:
            print("[AI Service] Сервис не инициализирован.")
            return

        print(f"[AI Service] Получена команда: '{command}'. Отправка запроса в OpenAI...")
        prompt = self._prepare_prompt(command)
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"}
            )
            
            tool_choice_str = response.choices[0].message.content
            print(f"[AI Service] Получен ответ от OpenAI: {tool_choice_str}")
            
            response_data = json.loads(tool_choice_str)
            tool_name = response_data.get("tool_name")
            params = response_data.get("parameters", {})

            if tool_name and tool_name in self.tools_map:
                print(f"[AI Service] Выполнение инструмента: {tool_name} с параметрами: {params}")
                tool_function = self.tools_map[tool_name]
                frame_data = tool_function(**params)
                
                # Отправляем сигнал, только если инструмент вернул данные для фрейма
                if frame_data:
                    self.create_frame_signal.emit(frame_data)
            else:
                print(f"[AI Service] LLM вернул неизвестный инструмент: '{tool_name}'")
        except Exception as e:
            print(f"[AI Service] Ошибка при обращении к OpenAI API: {e}")