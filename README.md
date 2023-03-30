# Hackathon (Mechathon)

Our project consists of one main script (Drowsiness_Detector.py) and one programme to train our Machine Learning Model (model.py).
We used TensorFlow modules to create a CNN which makes up the body of our hack.
Our dataset consists of 1452 images, classifed into 2 classes, "Open" and "Closed. The images are equally divided into the 2 classes.
We managed to achieve training accuracy of 96%, and a validation accuracy of 94%.
To capture real-time live feeds, we used pre-trained OpenCV's Cascade Classifier to detect the drivers' eyes.
After the eyes are detected, our trained model determines if the eyes are opened or closed.
If the driver's eyes remain closed for more than 2 seconds, it will trigger a script (to alert the driver/emergency brake)
After preprogamming a mock car with Arduino, we interface Arduino Uno with Python to control it with our computer.
The Arduino Uno will react to the keyboard inputs as well as inputs if the eyes are closed.
