import json
import logging

import azure.functions as func
from ask_rag_plugin import ask_rag


def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        question = req.params.get("query")
        if not question:
            try:
                data = req.get_json()
                question = data.get("query") or data.get("question")
            except:
                pass

        if not question:
            return func.HttpResponse("Brak pytania w żądaniu.", status_code=400)

        result = ask_rag(question)
        response = {
            "status": "success",
            "message": "Odpowiedź wygenerowana pomyślnie",
            "data": {
                "question": result["question"],
                "answer": result["answer"],
                "source_context": result["context"],
            },
        }
        return func.HttpResponse(
            json.dumps(response, indent=2, ensure_ascii=False),
            mimetype="application/json",
        )

    except Exception as e:
        return func.HttpResponse(f"Błąd: {str(e)}", status_code=500)
