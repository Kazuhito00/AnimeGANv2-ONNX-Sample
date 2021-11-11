#!/usr/bin/env python
# -*- coding: utf-8 -*-
import copy
import time
import argparse

import cv2 as cv
import numpy as np
import onnxruntime


def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("--device", type=int, default=0)
    parser.add_argument("--movie", type=str, default=None)
    parser.add_argument("--width", help='cap width', type=int, default=960)
    parser.add_argument("--height", help='cap height', type=int, default=540)

    parser.add_argument("--model",
                        type=str,
                        default='model/face_paint_512_v2_0.onnx')
    parser.add_argument("--input_size", type=int, default=512)

    args = parser.parse_args()

    return args


def run_inference(onnx_session, input_size, image):
    # リサイズ
    temp_image = copy.deepcopy(image)
    resize_image = cv.resize(temp_image, dsize=(input_size, input_size))
    x = cv.cvtColor(resize_image, cv.COLOR_BGR2RGB)

    # 前処理
    x = np.array(x, dtype=np.float32)
    x = x.transpose(2, 0, 1).astype('float32')
    x = x * 2 - 1
    x = x.reshape(-1, 3, input_size, input_size)

    # 推論
    input_name = onnx_session.get_inputs()[0].name
    output_name = onnx_session.get_outputs()[0].name
    onnx_result = onnx_session.run([output_name], {input_name: x})

    # 後処理
    onnx_result = np.array(onnx_result).squeeze()
    onnx_result = (onnx_result * 0.5 + 0.5).clip(0, 1)
    onnx_result = onnx_result * 255

    onnx_result = onnx_result.transpose(1, 2, 0).astype('uint8')
    onnx_result = cv.cvtColor(onnx_result, cv.COLOR_RGB2BGR)

    return resize_image, onnx_result


def main():
    # 引数解析 #################################################################
    args = get_args()
    cap_device = args.device
    cap_width = args.width
    cap_height = args.height

    if args.movie is not None:
        cap_device = args.movie

    model_path = args.model
    input_size = args.input_size

    # カメラ準備 ###############################################################
    cap = cv.VideoCapture(cap_device)
    cap.set(cv.CAP_PROP_FRAME_WIDTH, cap_width)
    cap.set(cv.CAP_PROP_FRAME_HEIGHT, cap_height)

    # モデルロード #############################################################
    onnx_session = onnxruntime.InferenceSession(model_path)

    elapsed_time = 0.0

    while True:
        start_time = time.time()

        # カメラキャプチャ #####################################################
        ret, image = cap.read()
        if not ret:
            break
        image_width, image_height = image.shape[1], image.shape[0]
        image = image[0:image_height,
                      int((image_width - image_height) / 2):image_width -
                      int((image_width - image_height) / 2)]

        resize_image, onnx_result = run_inference(
            onnx_session,
            input_size,
            image,
        )

        elapsed_time = time.time() - start_time

        # 描画 ###############################################################
        # フレーム経過時間
        elapsed_time_text = "Elapsed time: "
        elapsed_time_text += str(round((elapsed_time * 1000), 1))
        elapsed_time_text += 'ms'
        cv.putText(resize_image, elapsed_time_text, (10, 30),
                   cv.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 1, cv.LINE_AA)

        # 画面反映 ############################################################
        cv.imshow('AnimeGANv2 Before', resize_image)
        cv.imshow('AnimeGANv2 After', onnx_result)

        # キー処理(ESC：終了) #################################################
        key = cv.waitKey(1)
        if key == 27:  # ESC
            break

    cap.release()
    cv.destroyAllWindows()


if __name__ == '__main__':
    main()
