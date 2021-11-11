# AnimeGANv2-ONNX-Sample
[PyTorch Implementation of AnimeGANv2](https://github.com/bryandlee/animegan2-pytorch)のPythonでのONNX推論サンプルです。<br>
ONNXに変換したモデルも同梱しています。変換自体を試したい方は[AnimeGANv2_Convert2ONNX.ipynb](AnimeGANv2_Convert2ONNX.ipynb)を使用ください。<br>

# Requirement(ONNX変換)
* Pytorch 1.9.0 or later
* onnx 1.10.2 or later
* onnx-simplifier 0.3.6 or later

# Requirement(ONNX推論)
* OpenCV 4.5.3.56 or later
* onnxruntime-gpu 1.9.0 or later ※onnxruntimeでも動作しますが、推論時間がかかるのでGPUをお勧めします

# Demo
デモの実行方法は以下です。
```bash
python sample_onnx.py
```
* --device<br>
カメラデバイス番号の指定<br>
デフォルト：0
* --movie<br>
動画ファイルの指定 ※指定時はカメラデバイスより優先<br>
デフォルト：指定なし
* --width<br>
カメラキャプチャ時の横幅<br>
デフォルト：960
* --height<br>
カメラキャプチャ時の縦幅<br>
デフォルト：540
* --model<br>
ロードするモデルの格納パス<br>
デフォルト：model/face_paint_512_v2_0.onnx
* --input_shape<br>
モデルの入力サイズ<br>
デフォルト：512

# Reference
* [bryandlee/animegan2-pytorch](https://github.com/bryandlee/animegan2-pytorch)

# Author
高橋かずひと(https://twitter.com/KzhtTkhs)
 
# License 
AnimeGANv2-ONNX-Sample is under [MIT License](LICENSE).

# License(Image)
女性の画像は[フリー素材ぱくたそ](https://www.pakutaso.com)様の写真を利用しています。
