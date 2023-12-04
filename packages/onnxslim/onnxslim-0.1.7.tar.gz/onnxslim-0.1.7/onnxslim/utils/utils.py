import numpy as np
import onnx


def format_bytes(size_in_bytes):
    # Define the units and their corresponding suffixes
    units = ["B", "KB", "MB", "GB"]

    # Determine the appropriate unit and conversion factor
    unit_index = 0
    while size_in_bytes >= 1024 and unit_index < len(units) - 1:
        size_in_bytes /= 1024
        unit_index += 1

    # Format the result with two decimal places
    formatted_size = "{:.2f} {}".format(size_in_bytes, units[unit_index])
    return formatted_size


def onnx_dtype_to_numpy(onnx_dtype):
    import onnx.mapping as mapping

    return np.dtype(mapping.TENSOR_TYPE_TO_NP_TYPE[onnx_dtype])


def gen_onnxruntime_input_data(model):
    input_info = []
    for input_tensor in model.graph.input:
        name = input_tensor.name
        shape = []
        for dim in input_tensor.type.tensor_type.shape.dim:
            if dim.HasField("dim_param"):
                shape.append(dim.dim_param)
            elif dim.HasField("dim_value"):
                shape.append(dim.dim_value)
            else:
                shape.append(None)
        dtype = onnx_dtype_to_numpy(input_tensor.type.tensor_type.elem_type)

        input_info.append([name, shape, dtype])

    input_data_dict = {}
    for name, shapes, dtype in input_info:
        shapes = [
            shape if (shape != -1 and not isinstance(shape, str)) else 1
            for shape in shapes
        ]
        shapes = shapes if shapes else [1]
        if dtype in [np.int32, np.int64]:
            random_data = np.random.randint(10, size=shapes).astype(dtype)
        else:
            random_data = np.random.rand(*shapes).astype(dtype)
        input_data_dict[name] = random_data

    return input_data_dict


def onnxruntime_inference(model, input_data):
    import onnxruntime as rt

    sess = rt.InferenceSession(
        model.SerializeToString(), providers=["CPUExecutionProvider"]
    )
    onnx_output = sess.run(None, input_data)

    output_names = [output.name for output in sess.get_outputs()]
    onnx_output = dict(zip(output_names, onnx_output))

    return onnx_output
