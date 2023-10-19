## Introduction

This is an example program of a monitoring system that implements multi camera management, facial recognition, and facial input functions. And the monitoring and management system can achieve queries and management for specific times, locations, and personnel.
这是一个实现了多摄像头管理以及人脸识别、人脸录入的功能的监控系统的示例程序。并且该监控管理系统可以实现针对特定时间、特定地点、特定人员的查询和管理。

## Technology Map
python3.8
opencv
mysql8.0
pyside2 or pyqt5

## How to use
first,  enter the project root directory, `virtualenv venv`, then cd venv/scripts ,`activate`, then `pip install -r requirements` , just so easy.

We can add cameras through camera ID or streaming address, and configure the display information of the camera, such as display mode (including facial recognition mode, facial detection mode, traditional mode), camera location information or name, and so on. We can first input facial information, and then the system will have the facial features of this person. Of course, we can also delete a specific facial feature.
我们可以通过摄像头id或者拉流地址添加摄像头，并可以配置摄像头的显示信息，例如：显示模式（包括人脸识别模式、人脸检测模式、传统模式）、摄像头的位置信息或者名称等等。我们可以首先录入人脸信息，然后系统将会有这个人的人脸特征。当然我们也可以删除某个特定的人脸特征。

Finally, in the system log, we can search for specific individuals based on "facial features (corresponding person names)" and "location" or "time".
最后，在系统日志中，我们可以根据“人脸特征（与之对应的人员姓名）”和“位置”或者“时间”来查找特定的人员。

## Demostrations

【本科毕设 OpenCV+PySide2+MySQL的人脸识别监控管理系统】 https://www.bilibili.com/video/BV1Ug4y1g7uj
![2ca2c197e7c9ecc91caf6cf4bd7a6bf](https://github.com/inathanxu/MutiCameraManagement-FaceRecog/assets/62796940/b287e56b-bfbd-4cd5-ba47-7f4625d5b7ae)
![c8947ab50bf4515e9379b185b63cb7f](https://github.com/inathanxu/MutiCameraManagement-FaceRecog/assets/62796940/a11de7af-da5d-4184-987e-7b723981b0bb)
![5488f8496925a6807cefbf838684266](https://github.com/inathanxu/MutiCameraManagement-FaceRecog/assets/62796940/15b51e7f-f617-4e82-a008-d2b5df400c39)

## Help or About me 
If you have any problem, just raise an issue :-D
如果你有任何安装上的问题，欢迎通过这个email联系我，naixingxu@163.com，或者关注bilibili网站的up“inathanxu”进行私聊，远程协助安装将可能要求你请我喝杯咖啡 ~(@^_^@)~

