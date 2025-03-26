# onnx-convert-and-deploy
A repository to showcase the conversion of predictive models to ONNX format and serving them on KServe.

---

## Table of Contents
1. [Install Dependencies](#install-dependencies)
2. [LightGBM Local Development](#lightgbm-local-development)
3. [Convert LightGBM to ONNX Format](#convert-lightgbm-to-onnx-format)
4. [LightGBM ONNX Deployment to KServe](#lightgbm-onnx-deployment-to-kserve)
5. [Build Fraud Detection Keras Model](#build-fraud-detection-keras-model)
6. [General Template to Deploy ONNX Model to KServe](#general-template-to-deploy-onnx-model-to-kserve)

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

## LIGHTGBM ONNX DEPLOYMENT TO KSERVE

Deploy the converted LightGBM ONNX model to KServe using the provided templates.

### Custom Runtime

```yaml
apiVersion: serving.kserve.io/v1alpha1
kind: ServingRuntime
metadata:
  name: lgb-onnx-runtime
  annotations:
    openshift.io/display-name: lgb-onnx ServingRuntime for KServe
  labels:
    opendatahub.io/dashboard: "true"
spec:
  annotations:
    prometheus.kserve.io/port: '8080'
    prometheus.kserve.io/path: "/metrics"
  supportedModelFormats:
    - name: onnx
      version: "1"
      autoSelect: true
      priority: 1
  protocolVersions:
    - v2
    - grpc-v2
  containers:
    - name: kserve-container
      image: nvcr.io/nvidia/tritonserver:23.05-py3
      args:
        - tritonserver
        - --model-store=/mnt/models
        - --grpc-port=9000
        - --http-port=8080
        - --allow-grpc=true
        - --allow-http=true
      resources:
        requests:
          cpu: "1"
          memory: 2Gi
        limits:
          cpu: "1"
          memory: 2Gi
```

### Inference Service

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

---

## BUILD FRAUD DETECTION KERAS MODEL

The notebook `keras/fraud_detection.ipynb` demonstrates an ML example to train a fraud detection model.

---

## GENERAL TEMPLATE TO DEPLOY ONNX MODEL TO KSERVE

This section provides a general template for deploying ONNX models to KServe. Refer to the [Custom Runtime](#custom-runtime) and [Inference Service](#inference-service) sections for examples.