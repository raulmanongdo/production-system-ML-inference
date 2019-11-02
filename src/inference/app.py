import os
try:
    import utilities
except ModuleNotFoundError:  # This is thrown when using pytest.
    from . import utilities


MODEL_URI = os.environ['MODEL_URI']
WRITER_QUEUE = os.environ['WRITER_QUEUE'] 


def predict(event, context):
    """Makes inference on the passed data."""
    df = utilities.load_dataframe_from_sqs_event(event)
    X = utilities.preprocess(df)

    model = utilities.load_model(MODEL_URI)
    y = model.predict(X)
    results = utilities.postprocess(X, y)

    msg = utilities.SQSMessage()
    msg.dataframe = results
    msg.send(queue=WRITER_QUEUE)
    return {
        "status": "success",
    } 
