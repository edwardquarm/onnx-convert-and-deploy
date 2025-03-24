# onnx-convert-and-deploy
A repository to showcase the conversion of predictive models to ONNX format and serving them on KServe.

---

## Table of Contents
1. [Install Dependencies](#install-dependencies)
2. [LightGBM Local Development](#lightgbm-local-development)
3. [Convert LightGBM to ONNX Format](#convert-lightgbm-to-onnx-format)
4. [LightGBM Deployment to KServe](#lightgbm-deployment-to-kserve)

---

## INSTALL DEPENDENCIES

Install the required dependencies using the following command:

```bash
pip install -r requirements.txt
```

---

## LIGHTGBM LOCAL DEVELOPMENT

Follow these steps to set up LightGBM for local development:

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

## CONVERT LIGHTGBM TO ONNX FORMAT

Convert a LightGBM model to ONNX format using the provided script:

```bash
python lgbm-onnx.py
```

---

## LIGHTGBM DEPLOYMENT TO KSERVE

Deploy the LightGBM model to KServe using the following example template:

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