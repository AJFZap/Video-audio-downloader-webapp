# Audio and Video downloader with Flask

## Small web-app that allows the user to download the audio or the whole video from a given youtube link.

This is a Flask-based web application that allows users to download YouTube videos in MP3 and MP4 formats. Simply input a YouTube link, and the app will process the request and provide download for the selected format. (Eventually it will accept more than just youtube videos.)

## Features

* Download Youtube videos in MP4 format.
* Download Youtube audio in MP3 format.
* Simplistic user friendly interface.
* Error handling and validation for Youtube Links.

## Prerequisites

* Python 3.11
* Flask
* Pytubefix (Since pytube still has errors on it's cipher class)
* Other dependencies listed in requirements.txt

## Technologies Used

* **Backend:** Flask, pytubefix
* **Frontend:** Tailwind, HTML, CSS, JQuery, JS
* **Deployment:** Vercel

## Webpage to check it out!
[YT-Downloader](https://yt-vidaud-downloader.vercel.app/)