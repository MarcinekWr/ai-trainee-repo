import json
import logging
import traceback
import uuid

import azure.functions as func
from ask_rag_plugin import ask_rag


def main(req: func.HttpRequest) -> func.HttpResponse:
    trace_id = str(uuid.uuid4())
    logging.info(f"[{trace_id}] Rozpoczęcie obsługi zapytania ask_rag")

    try:
        question = req.params.get("query")
        if not question:
            try:
                data = req.get_json()
                question = data.get("query") or data.get("question")
            except Exception as parse_error:
                logging.warning(
                    f"[{trace_id}] Nie udało się sparsować JSON-a: {str(parse_error)}"
                )

        if not question:
            logging.warning(f"[{trace_id}] Brak pytania w żądaniu")
            return func.HttpResponse("Brak pytania w żądaniu.", status_code=400)

        logging.info(f"[{trace_id}] Zapytanie użytkownika: {question}")

        result = ask_rag(question)

        response = {
            "status": "success",
            "message": "Odpowiedź wygenerowana pomyślnie",
            "trace_id": trace_id,
            "data": {
                "question": result["question"],
                "answer": result["answer"],
                "source_context": result["context"],
            },
        }

        logging.info(f"[{trace_id}] Odpowiedź wygenerowana pomyślnie")
        return func.HttpResponse(
            json.dumps(response, indent=2, ensure_ascii=False),
            mimetype="application/json",
        )

    except Exception as e:
        logging.error(f"[{trace_id}] Błąd wykonania funkcji:")
        logging.error(traceback.format_exc())
        return func.HttpResponse(
            f"Błąd serwera (trace_id: {trace_id}): {str(e)}", status_code=500
        )
