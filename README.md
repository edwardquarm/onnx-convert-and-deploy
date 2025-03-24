# onnx-convert-and-deploy
A repo to showcase the conversion of predictive models to onnx format and serving on KServe.


# LIGHTGBM LOCAL DEVELOPMENT:
1. Install [KServe Python SDK](https://github.com/kserve/kserve/tree/master/python/kserve) using ``pip`` or ``peotry``
2. Install [lgbm Server](https://github.com/kserve/kserve/tree/master/python/lgbserver) using ``peotry``
3. Save LightGBM model in local dir ``/mnt/models/*.bst``
4. Start the lgbm server locally by running ``python -m lgbserver --model_dir ./mnt/models/ --model_name lgb``
    a. To display swagger UI, run ``python -m lgbserver --model_dir ./mnt/models/ --model_name lgb --enable_docs_url True``

# LIGHTGBM DEPLOY TO KSERVE
Deploy to KServe using the example template:

```yaml
apiVersion: serving.kserve.io/v1beta1
kind: InferenceService
metadata:
  name: example-lgbm-onnx-deployment
spec:
  predictor:
    maxReplicas: 1
    minReplicas: 1
    model:
      modelFormat:
        name: onnx
        version: "1"
        resources:
      limits:
        cpu: "2"
        memory: 8Gi
      requests:
        cpu: "1"
        memory: 4Gi
      storageUri: s3://bucket/onnx_lgbm/iris.onnx

```

