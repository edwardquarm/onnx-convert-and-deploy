# onnx-convert-and-deploy
A repository to showcase the conversion of predictive models to ONNX format and serving them on KServe.

---

## LIGHTGBM LOCAL DEVELOPMENT

1. Install the [KServe Python SDK](https://github.com/kserve/kserve/tree/master/python/kserve) using `pip` or `poetry`.
2. Install the [LightGBM Server](https://github.com/kserve/kserve/tree/master/python/lgbserver) using `poetry`.
3. Save the LightGBM model in the local directory: `/mnt/models/*.bst`.
4. Start the LightGBM server locally by running:

   ```bash
   python -m lgbserver --model_dir ./mnt/models/ --model_name lgb
   ```

   - To display the Swagger UI, run:

     ```bash
     python -m lgbserver --model_dir ./mnt/models/ --model_name lgb --enable_docs_url True
     ```

---

## LIGHTGBM DEPLOYMENT TO KSERVE

Deploy to KServe using the following example template:

```yaml
apiVersion: serving.kserve.io/v1beta1
kind: InferenceService
metadata:
  name: example-lgbm-onnx-deployment
spec:
  predictor:
    minReplicas: 1
    maxReplicas: 1
    model:
      modelFormat:
        name: onnx
        version: "1"
      storageUri: s3://bucket/onnx_lgbm/iris.onnx
      resources:
        requests:
          cpu: "1"
          memory: 4Gi
        limits:
          cpu: "2"
          memory: 8Gi
```