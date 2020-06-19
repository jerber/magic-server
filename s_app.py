import serverless_sdk

sdk = serverless_sdk.SDK(
    org_id="jerber",
    application_name="firebase-lambda-test",
    app_uid="rvkdjb9JGGGs0VTFT6",
    org_uid="p33bb2HSC5ZKPwWx0M",
    deployment_uid="bb12dff2-de43-4641-8caf-e789fffc7382",
    service_name="firebase-lambda-test",
    should_log_meta=True,
    should_compress_logs=True,
    disable_aws_spans=False,
    disable_http_spans=False,
    stage_name="dev",
    plugin_version="3.6.13",
    disable_frameworks_instrumentation=False,
)
handler_wrapper_kwargs = {
    "function_name": "firebase-lambda-test-dev-app",
    "timeout": 15,
}
try:
    user_handler = serverless_sdk.get_user_handler("main.handler")
    handler = sdk.handler(user_handler, **handler_wrapper_kwargs)
except Exception as error:
    e = error

    def error_handler(event, context):
        raise e

    handler = sdk.handler(error_handler, **handler_wrapper_kwargs)
