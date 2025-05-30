import logging
import traceback
import uuid

import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    trace_id = str(uuid.uuid4())
    logging.error(f"[{trace_id}] Testowe wywołanie wyjątku w raise_error")
    logging.error(traceback.format_exc())
    raise Exception(f"[{trace_id}] To jest testowy błąd do Application Insights")
