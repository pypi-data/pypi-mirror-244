# Kadita CV 



<p align="center"><img src="https://github.com/Kastara-Digital-Technology/assets/raw/main/logo/V2/cvColorLogo.png" width="200" height="240"></p>

Kadita CV is a lightweight face recognition and facial attribute analysis ([age](https://sefiks.com/2019/02/13/apparent-age-and-gender-prediction-in-keras/), [gender](https://sefiks.com/2019/02/13/apparent-age-and-gender-prediction-in-keras/), [emotion](https://sefiks.com/2018/01/01/facial-expression-recognition-with-keras/) and [race](https://sefiks.com/2019/11/11/race-and-ethnicity-prediction-in-keras/)) framework for python. It is a hybrid face recognition framework wrapping **state-of-the-art** models: [`VGG-Face`](https://sefiks.com/2018/08/06/deep-face-recognition-with-keras/), [`Google FaceNet`](https://sefiks.com/2018/09/03/face-recognition-with-facenet-in-keras/), [`OpenFace`](https://sefiks.com/2019/07/21/face-recognition-with-openface-in-keras/), [`Facebook DeepFace`](https://sefiks.com/2020/02/17/face-recognition-with-facebook-deepface-in-keras/), [`DeepID`](https://sefiks.com/2020/06/16/face-recognition-with-deepid-in-keras/), [`ArcFace`](https://sefiks.com/2020/12/14/deep-face-recognition-with-arcface-in-keras-and-python/), [`Dlib`](https://sefiks.com/2020/07/11/face-recognition-with-dlib-in-python/) and `SFace`.

Experiments show that human beings have 97.53% accuracy on facial recognition tasks whereas those models already reached and passed that accuracy level.
 It's worth mentioning that Kadita CV is not limited to face recognition alone; it can also be used for object detection with YOLO, OpenCV, SVM, CNN, and TensorFlow Lite.

By incorporating multiple leading models, Kadita CV has the potential to deliver highly accurate face recognition solutions. With the inclusion of these models, it may be able to meet or even exceed the accuracy achieved by humans in facial recognition tasks.

Additionally, its ability to perform object detection with YOLO, OpenCV, and TensorFlow Lite makes it a versatile tool for a wide range of computer vision applications.
## Installation 

The easiest way to install kadita is to download it from [`PyPI`](https://pypi.org/project/deepface/). It's going to install the library itself and its prerequisites as well.

```shell
$ pip install kadita
```



Secondly, you can install kadita from its source code.

```shell
$ git clone https://github.com/Kastara-Digital-Technology/KaditaCV.git
$ cd kadita
$ pip install -e .
```

Then you will be able to import the library and use its functionalities.

```python
from kadita import DeepFace
```

**Face Recognition** - [`Demo`](https://youtu.be/WnUVYQP4h44)

A modern [**face recognition pipeline**](https://sefiks.com/2020/05/01/a-gentle-introduction-to-face-recognition-in-deep-learning/) consists of 5 common stages: [detect](https://sefiks.com/2020/08/25/deep-face-detection-with-opencv-in-python/), [align](https://sefiks.com/2020/02/23/face-alignment-for-face-recognition-in-python-within-opencv/), [normalize](https://sefiks.com/2020/11/20/facial-landmarks-for-face-recognition-with-dlib/), [represent](https://sefiks.com/2018/08/06/deep-face-recognition-with-keras/) and [verify](https://sefiks.com/2020/05/22/fine-tuning-the-threshold-in-face-recognition/). While Kadita CV handles all these common stages in the background, you don’t need to acquire in-depth knowledge about all the processes behind it. You can just call its verification, find or analysis function with a single line of code. In this below this is code for Face Recognition.
```python
from kadita import DeepFace

DeepFace.stream("dataset") 


```


<p align="center"><img src="https://raw.githubusercontent.com/Kastara-Digital-Technology/KaditaCV/main/icon/Screenshot%202023-10-20%20164710.png" width="75%" height="75%"></p>
<p align="center"><i> 1 face in frame</i></p>

Face Recogniton function can also handle many faces in the face pairs, example when 2 people face a webcam it will detect 2 people. 

<p align="center"><img src="https://raw.githubusercontent.com/Kastara-Digital-Technology/KaditaCV/main/icon/Screenshot%202023-10-20%20164843.png" width="75%" height="75%"></p>
<p align="center"><i> 2 face in frame</i></p>


**Face Recognition models** - [`Demo`](https://youtu.be/i_MOwvhbLdI)

Kadita CV is a **hybrid** face recognition package. It currently wraps many **state-of-the-art** face recognition models: [`VGG-Face`](https://sefiks.com/2018/08/06/deep-face-recognition-with-keras/) , [`Google FaceNet`](https://sefiks.com/2018/09/03/face-recognition-with-facenet-in-keras/), [`OpenFace`](https://sefiks.com/2019/07/21/face-recognition-with-openface-in-keras/), [`Facebook DeepFace`](https://sefiks.com/2020/02/17/face-recognition-with-facebook-deepface-in-keras/), [`DeepID`](https://sefiks.com/2020/06/16/face-recognition-with-deepid-in-keras/), [`ArcFace`](https://sefiks.com/2020/12/14/deep-face-recognition-with-arcface-in-keras-and-python/), [`Dlib`](https://sefiks.com/2020/07/11/face-recognition-with-dlib-in-python/) and `SFace`. The default configuration uses VGG-Face model.


```python
models = [
  "VGG-Face", 
  "Facenet", 
  "Facenet512", 
  "OpenFace", 
  "DeepFace", 
  "DeepID", 
  "ArcFace", 
  "Dlib", 
  "SFace",
]

#Face Recognition
dfs = kadita.find(img_path = "Rafi.jpg",
      db_path = "D:\Kumpulan Projek\Library CV KDT\Kadita CV - Face Recogntion DeepFace\tests\dataset", 
      model_name = models[1]
)

```

[//]: # (<p align="center"><img src="https://raw.githubusercontent.com/serengil/deepface/master/icon/model-portfolio-v8.jpg" width="95%" height="95%"></p>)

FaceNet, VGG-Face, ArcFace and Dlib are [overperforming](https://youtu.be/i_MOwvhbLdI) ones based on experiments. You can find out the scores of those models below. 

| Model | LFW Score | YTF Score |
| ---   | --- | --- |
| Facenet512 | 99.65% | - |
| SFace | 99.60% | - |
| ArcFace | 99.41% | - |
| Dlib | 99.38 % | - |
| Facenet | 99.20% | - |
| VGG-Face | 98.78% | 97.40% |
| *Human-beings* | *97.53%* | - |
| OpenFace | 93.80% | - |
| DeepID | - | 97.05% |

<p align="center"><i>Result LFW and YTF score</i></p>

- The "LFW score" refers to the performance metric or measurement of face recognition algorithms tested using the Labeled Faces in the Wild (LFW) dataset.
- The "YTF score" is an abbreviation for "YouTube Face Dataset score." This dataset is used in face recognition research, and the "YTF score" typically refers to the performance measurement of face recognition algorithms tested using the YouTube Face (YTF) dataset.
**Similarity**

Face recognition models are regular [convolutional neural networks](https://sefiks.com/2018/03/23/convolutional-autoencoder-clustering-images-with-neural-networks/) and they are responsible to represent faces as vectors. We expect that a face pair of same person should be [more similar](https://sefiks.com/2020/05/22/fine-tuning-the-threshold-in-face-recognition/) than a face pair of different persons.

Similarity could be calculated by different metrics such as [Cosine Similarity](https://sefiks.com/2018/08/13/cosine-similarity-in-machine-learning/), Euclidean Distance and L2 form. The default configuration uses cosine similarity.

```python
metrics = ["cosine", "euclidean", "euclidean_l2"]

#face verification
result = DeepFace.verify(img1_path = "img1.jpg", 
          img2_path = "img2.jpg", 
          distance_metric = metrics[1]
)

#face recognition
dfs = DeepFace.find(img_path = "img1.jpg", 
          db_path = "D:\Kumpulan Projek\Library CV KDT\Kadita CV - Face Recogntion DeepFace\tests\dataset", 
          distance_metric = metrics[2]
)
```

Euclidean L2 form [seems](https://youtu.be/i_MOwvhbLdI) to be more stable than cosine and regular Euclidean distance based on experiments.

**Facial Attribute Analysis** - [`Demo`](https://youtu.be/GT2UeN85BdA)

Kadita CV also comes with a strong facial attribute analysis module including [`age`](https://sefiks.com/2019/02/13/apparent-age-and-gender-prediction-in-keras/), [`gender`](https://sefiks.com/2019/02/13/apparent-age-and-gender-prediction-in-keras/), [`facial expression`](https://sefiks.com/2018/01/01/facial-expression-recognition-with-keras/) (including angry, fear, neutral, sad, disgust, happy and surprise) and [`race`](https://sefiks.com/2019/11/11/race-and-ethnicity-prediction-in-keras/) (including asian, white, middle eastern, indian, latino and black) predictions. Result is going to be the size of faces appearing in the source image.

```python
objs = DeepFace.analyze(img_path = "img4.jpg", 
        actions = ['age', 'gender', 'race', 'emotion']
)
```

<p align="center"><img src="https://raw.githubusercontent.com/Kastara-Digital-Technology/KaditaCV/main/icon/Screenshot%202023-10-04%20174140.png" width="75%" height="75%"></p>
<p align="center"><i>Age, Gender, Race, Emotion Example</i></p>

Age model got ± 4.65 MAE; gender model got 97.44% accuracy, 96.29% precision and 95.05% recall as mentioned.

**Face Detection Haar Cascade OpenCV** - [`Demo`](https://youtu.be/GZ2p2hj2H5k)

Face detection and alignment are important early stages of a modern face recognition pipeline. Experiments show that just alignment increases the face recognition accuracy almost 40%. [`OpenCV`](https://sefiks.com/2020/02/23/face-alignment-for-face-recognition-in-python-within-opencv/), and [`YOLOv8 Face`](https://github.com/derronqi/yolov8-face) detectors are wrapped in KaditaCV.

<p align="center"><img src="https://raw.githubusercontent.com/Kastara-Digital-Technology/KaditaCV/main/icon/CV%202.png" width="95%" height="95%"></p>

All deepface functions accept an optional detector backend input argument. You can switch among those detectors with this argument. OpenCV is the default detector.

```python
from modules.image import Vision
from modules.routine import FaceRecognition
from modules.routine import FaceRecognitionTraining
from modules.routine import ImgBuster as Yolo
from utility.data import YAMLDataHandler

if __name__ == "__main__":
        try:
            while True:
                try:
                    frame = cam.read(640, True)
                    face_detect = face.predict(frame)
                    face_condition = 1 if face_detect else 0
                    condition = 1 if (face_condition) else 0
                    data.update("face-condition", str(condition))
                    yolo.draw(frame, face_detect)
                    cam.show(frame, "frame")
                    if cam.wait(1) == ord('q') or face.isStop():
                        if face.isTraining():
                            t = FaceRecognitionTraining()
                            t.process()
                        break
                except Exception as err:
                    print(err)
            cam.release()
            cam.destroy()
        except Exception as e:
            print(f"[INFO] {time.time()} Main Initialize Failed: \n{e}")

```

Face Detection Haar cascade OpenCV models are actually the simplest way to face recognition models, because they don't have any model like CNN but his a just simple algorithm Local Binary Pattern Histograms (LBPH). So here the result of OpenCV :

<p align="center"><img src="https://raw.githubusercontent.com/Kastara-Digital-Technology/KaditaCV/main/icon/Screenshot%202023-09-03%20061905.png" width="75%" height="75%"></p>
<p align="center"><i> Open CV</i></p>

**Face Detection YOLOV8** - [`Demo`](https://youtu.be/GZ2p2hj2H5k)

Face detection and alignment are important early stages of a modern face recognition pipeline. Experiments show that just alignment increases the face recognition accuracy almost 100%. [`OpenCV`](https://sefiks.com/2020/02/23/face-alignment-for-face-recognition-in-python-within-opencv/), [`SSD`](https://sefiks.com/2020/08/25/deep-face-detection-with-opencv-in-python/), [`Dlib`](https://sefiks.com/2020/07/11/face-recognition-with-dlib-in-python/),  [`MTCNN`](https://sefiks.com/2020/09/09/deep-face-detection-with-mtcnn-in-python/), [`RetinaFace`](https://sefiks.com/2021/04/27/deep-face-detection-with-retinaface-in-python/), [`MediaPipe`](https://sefiks.com/2022/01/14/deep-face-detection-with-mediapipe/), [`YOLOv8 Face`](https://github.com/derronqi/yolov8-face) and [`YuNet`](https://github.com/ShiqiYu/libfacedetection) detectors are wrapped in deepface.

<p align="center"><img src="https://raw.githubusercontent.com/Kastara-Digital-Technology/KaditaCV/main/icon/CV%202.png" width="95%" height="95%"></p>

All deepface functions accept an optional detector backend input argument. You can switch among those detectors with this argument. Yolov8 is the default detector and here the result : 

```python
from ultralytics import YOLO
import cv2

model = YOLO('assets/models/yolov8n-face.pt')

cap = cv2.VideoCapture(0)

while cap.isOpened():
    success, frame = cap.read()

    if success:
        results = model(frame)
        annotated_frame = results[0].plot()
        cv2.imshow("YOLOv8 Face", annotated_frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        break

cap.release()
cv2.destroyAllWindows()
```

Face recognition models are actually CNN models and they expect standard sized inputs. So, resizing is required before representation. To avoid deformation, Kadita CV adds black padding pixels according to the target size argument after detection and alignment. If you think Dlib and RetinaFace is hard, you can use the Yolov8 algorithm instead of the default like RetinaFace, Dlib, and OpenCV.

<p align="center"><img src="https://raw.githubusercontent.com/Kastara-Digital-Technology/KaditaCV/main/icon/Screenshot%202023-10-27%20165801.png" width="75%" height="75%"></p>
<p align="center"><i> Yolov8 Face</i></p>


RetinaFace and MTCNN seem to overperform in detection and alignment stages but they are much slower. If the speed of your pipeline is more important, then you should use opencv, ssd, and YoloV8. On the other hand, if you consider the accuracy, then you should use retinaface or mtcnn.

The performance of RetinaFace is very satisfactory even in the crowd as seen in the following illustration. Besides, it comes with an incredible facial landmark detection performance. Highlighted red points show some facial landmarks such as eyes, nose and mouth. That's why, alignment score of RetinaFace is high as well.

<p align="center"><img src="https://raw.githubusercontent.com/serengil/deepface/master/icon/retinaface-results.jpeg" width="90%" height="90%">
<br><em>RetinaFace</em>
</p>

You can find out more about RetinaFace on this [repo](https://github.com/serengil/retinaface).

**Real time Kadita CV** - [`Demo`](https://youtu.be/-c9sSJcx6wI)

You can run Kadita CV for real time videos as well. Stream function will access your webcam and apply both face recognition and facial attribute analysis. The function starts to analyze a frame if it can focus a face sequentially 1 frame. Then, it shows results in a frame.

```python
from kadita import DeepFace

DeepFace.stream(db_path="../tests/dataset")
```

<p align="center"><img src="https://raw.githubusercontent.com/Kastara-Digital-Technology/KaditaCV/main/icon/Screenshot%202023-10-20%20164135.png" width="90%" height="90%"></p>
<p align="center"><i></i></p>

Even though face recognition is based on one-shot learning, you can use multiple face pictures of a person as well. You should rearrange your directory structure as illustrated below.

```bash
user
├── database
│   ├── Iwan
│   │   ├── Iwan1.jpg
│   │   ├── Iwan2.jpg
│   ├── Rafi
│   │   ├── Rafi1.jpg
│   │   ├── Rafi2.jpg
│   ├── Firza
│   │   ├── Firza1.jpg
│   │   ├── Firza2.jpg
        
```

[//]: # (**API** - [`Demo`]&#40;https://youtu.be/HeKCQ6U9XmI&#41;)

[//]: # ()
[//]: # (DeepFace serves an API as well. You can clone [`/api`]&#40;https://github.com/serengil/deepface/tree/master/api&#41; folder and run the api via gunicorn server. This will get a rest service up. In this way, you can call deepface from an external system such as mobile app or web.)

[//]: # ()
[//]: # (```shell)

[//]: # (cd scripts)

[//]: # (./service.sh)

[//]: # (```)

[//]: # ()
[//]: # (<p align="center"><img src="https://raw.githubusercontent.com/serengil/deepface/master/icon/deepface-api.jpg" width="90%" height="90%"></p>)

[//]: # ()
[//]: # (Face recognition, facial attribute analysis and vector representation functions are covered in the API. You are expected to call these functions as http post methods. Default service endpoints will be `http://localhost:5000/verify` for face recognition, `http://localhost:5000/analyze` for facial attribute analysis, and `http://localhost:5000/represent` for vector representation. You can pass input images as exact image paths on your environment, base64 encoded strings or images on web. [Here]&#40;https://github.com/serengil/deepface/tree/master/api&#41;, you can find a postman project to find out how these methods should be called.)

[//]: # ()
[//]: # (**Dockerized Service**)

[//]: # ()
[//]: # (You can deploy the deepface api on a kubernetes cluster with docker. The following [shell script]&#40;https://github.com/serengil/deepface/blob/master/scripts/dockerize.sh&#41; will serve deepface on `localhost:5000`. You need to re-configure the [Dockerfile]&#40;https://github.com/serengil/deepface/blob/master/Dockerfile&#41; if you want to change the port. Then, even if you do not have a development environment, you will be able to consume deepface services such as verify and analyze. You can also access the inside of the docker image to run deepface related commands. Please follow the instructions in the [shell script]&#40;https://github.com/serengil/deepface/blob/master/scripts/dockerize.sh&#41;.)

[//]: # ()
[//]: # (```shell)

[//]: # (cd scripts)

[//]: # (./dockerize.sh)

[//]: # (```)

[//]: # ()
[//]: # (<p align="center"><img src="https://raw.githubusercontent.com/serengil/deepface/master/icon/deepface-dockerized-v2.jpg" width="50%" height="50%"></p>)

[//]: # ()
[//]: # (**Command Line Interface**)

[//]: # ()
[//]: # (DeepFace comes with a command line interface as well. You are able to access its functions in command line as shown below. The command deepface expects the function name as 1st argument and function arguments thereafter.)

[//]: # ()
[//]: # (```shell)

[//]: # (#face verification)

[//]: # ($ deepface verify -img1_path tests/dataset/img1.jpg -img2_path tests/dataset/img2.jpg)

[//]: # ()
[//]: # (#facial analysis)

[//]: # ($ deepface analyze -img_path tests/dataset/img1.jpg)

[//]: # (```)

[//]: # ()
[//]: # (You can also run these commands if you are running deepface with docker. Please follow the instructions in the [shell script]&#40;https://github.com/serengil/deepface/blob/master/scripts/dockerize.sh#L17&#41;.)

[//]: # (## Contribution [![Tests]&#40;https://github.com/serengil/deepface/actions/workflows/tests.yml/badge.svg&#41;]&#40;https://github.com/serengil/deepface/actions/workflows/tests.yml&#41;)

[//]: # ()
[//]: # (Pull requests are more than welcome! You should run the unit tests locally by running [`test/unit_tests.py`]&#40;https://github.com/serengil/deepface/blob/master/tests/unit_tests.py&#41; before creating a PR. Once a PR sent, GitHub test workflow will be run automatically and unit test results will be available in [GitHub actions]&#40;https://github.com/serengil/deepface/actions&#41; before approval. Besides, workflow will evaluate the code with pylint as well.)

[//]: # (## Support)

[//]: # ()
[//]: # (There are many ways to support a project - starring⭐️ the GitHub repo is just one 🙏)

[//]: # ()
[//]: # (You can also support this work on [Patreon]&#40;https://www.patreon.com/serengil?repo=deepface&#41; or [GitHub Sponsors]&#40;https://github.com/sponsors/serengil&#41;.)

[//]: # ()
[//]: # (<a href="https://www.patreon.com/serengil?repo=deepface">)

[//]: # (<img src="https://raw.githubusercontent.com/serengil/deepface/master/icon/patreon.png" width="30%" height="30%">)

[//]: # (</a>)

[//]: # (## Citation)

[//]: # ()
[//]: # (Please cite deepface in your publications if it helps your research. Here are its BibTex entries:)

[//]: # ()
[//]: # (If you use deepface for facial recogntion purposes, please cite the this publication.)

[//]: # ()
[//]: # (```BibTeX)

[//]: # (@inproceedings{serengil2020lightface,)

[//]: # (  title        = {LightFace: A Hybrid Deep Face Recognition Framework},)

[//]: # (  author       = {Serengil, Sefik Ilkin and Ozpinar, Alper},)

[//]: # (  booktitle    = {2020 Innovations in Intelligent Systems and Applications Conference &#40;ASYU&#41;},)

[//]: # (  pages        = {23-27},)

[//]: # (  year         = {2020},)

[//]: # (  doi          = {10.1109/ASYU50717.2020.9259802},)

[//]: # (  url          = {https://doi.org/10.1109/ASYU50717.2020.9259802},)

[//]: # (  organization = {IEEE})

[//]: # (})

[//]: # (```)

[//]: # ()
[//]: # ( If you use deepface for facial attribute analysis purposes such as age, gender, emotion or ethnicity prediction or face detection purposes, please cite the this publication.)

[//]: # ()
[//]: # (```BibTeX)

[//]: # (@inproceedings{serengil2021lightface,)

[//]: # (  title        = {HyperExtended LightFace: A Facial Attribute Analysis Framework},)

[//]: # (  author       = {Serengil, Sefik Ilkin and Ozpinar, Alper},)

[//]: # (  booktitle    = {2021 International Conference on Engineering and Emerging Technologies &#40;ICEET&#41;},)

[//]: # (  pages        = {1-4},)

[//]: # (  year         = {2021},)

[//]: # (  doi          = {10.1109/ICEET53442.2021.9659697},)

[//]: # (  url          = {https://doi.org/10.1109/ICEET53442.2021.9659697},)

[//]: # (  organization = {IEEE})

[//]: # (})

[//]: # (```)

Also, if you use Kadita CV in your GitHub projects, please add `KaditaCV` in the `requirements.txt`.

## Licence

Kadita CV is licensed under the MIT License - see [`LICENSE`](https://raw.githubusercontent.com/Kastara-Digital-Technology/KaditaCV/main/LICENSE) for more details.