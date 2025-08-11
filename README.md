# Reddit Text Video Youtube Automation



# Author: Sheetansh Kumar





This repo is a video automation tool in which audios + videos are automated.



Here we automate the process of data source, video creation and uploading the video to Youtube. Basically no manual work is done while doing all of this.

The benefit is that one can automate daily creation and uploading the video to Youtube / Instagram etc.



----------------------------



---------- Theory  ----------



A video is a combination of images/frames. If we can edit each frame then we can automate the whole process.

As simple as that :)



----------------------------

Well, not so simple ;)



The whole process is divided accross several parts.





Data Source:

  * Take reddit pages as my textual data source using reddit api



Audio rendering:

  - creates audio on the basis of textual data using gtts

  - saves it in a screen_time_map where one audio refers to a one screen and so on

  - one screen means currently shown image in the screen for a particular time

  - screen_time_map contains data for how much duration a screen should be shown in the video, in our case it should show till the voice assistant is speaking for that particular screen

  - when all audio files are generated, a full new combined audio file is created



Video rendering

  - edit frames using opencv in python

  - any sample background video can be used to capture per frame

  - inside each frame we insert data

  - using screen_time_map we show every frame for the particular time mentioned in the map

  - for video and audio operations we use "ffmpeg", a very important tool.

  - textual data is embedded similarly in each frame and how for required duration

 

Combine Audio and Video:

  - After both audio and video files are generated, we combine both and create new file

  



Upload to Youtube:

  - After the video is create, youtube upload api is called and the video is uploaded to YouTube

  

  

----------------------------



to run:

 - add credentials for reddit api, youtube api, gtts etc.

 - you need to add a sample video inside the location mentioned in videoconstant.py

 ```

pip install -r requirements.txt

python3 setup_video_environment.py
```

and then simply do,

```

python3 src/driver.py

```

Provide envs in your .evn file before running.

Replace the background video with you video, change text size and you are good to go!




You can also automate the whole thing using cronjob and then forget you need to even run anything manually.



----------------------------





If you are successful in doing all of the above, please do give a thumbs up in my youtube video ans give a start to this repo :)





Happy coding!

That's all Folks!

----------------------------

