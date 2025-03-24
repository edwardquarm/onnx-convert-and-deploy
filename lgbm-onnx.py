from pathlib import Path
import onnxmltools
import lightgbm as lgb
from skl2onnx.common.data_types import FloatTensorType
import onnxruntime as rt
import logging

logging.basicConfig(level=logging.INFO)

def load_model(model_path):
    model = lgb.Booster(model_file=model_path)

    return model

def convert_model(model, onnx_path):
    initial_type = [('float_input', FloatTensorType([None, 4]))]
    onnx_model = onnxmltools.convert_lightgbm(model, initial_types=initial_type)
    onnxmltools.utils.save_model(onnx_model, onnx_path)

    return onnx_path

def create_inference_session(onnx_path, input_data):
    session = rt.InferenceSession(str(onnx_path))
    output = session.run(None, {"float_input": input_data})
    return output


if __name__ == "__main__":
    model_path = Path("mnt", "models", "model.bst")
    # Load the model
    model = load_model(model_path)
    onnx_path = Path("mnt", "models", "model.onnx")
    # Convert the model
    onnx_path = convert_model(model, onnx_path)
    input_data = [[1, 2, 3, 4]]
    # Create an inference session
    output = create_inference_session(onnx_path, input_data)
    logging.info(f"Output: {output}")


