console.log('1111', 1111);

// Function to validate YouTube URLs
function isValidYouTubeURL(url) {
    const regex = /^(https?\:\/\/)?(www\.youtube\.com|youtu\.?be)\/.+$/;
    return regex.test(url);
}

// Download Video button clicked.
document.getElementById('downloadvideobutton').addEventListener('click', async () => {
    const videoLink = document.getElementById('streamlink').value;
    const scriptContent = document.getElementById('script-content');
    // const summaryContent = document.getElementById('summary-content');

    // Validate YouTube link
    if (!isValidYouTubeURL(videoLink)) {
        alert("Please enter a valid YouTube link.");
        return;
    }

    // Send the link to the backend.
    if(videoLink) {
        document.getElementById('loading-ring').style.display = 'block';
        
        // Clear previous content
        scriptContent.innerHTML = '';
        // summaryContent.innerHTML = '';

        const endpointUrl = '/video';
        
        try {
            const response = await fetch(endpointUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ link: videoLink })
            });

            const data = await response.json();

            // Check if the response contains an error
            if (data['error']) {
                // If error exists, throw an error
                throw new Error(data['error']);
            }

            // Show the results!
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            let date = new Date().toISOString().split('T')[0]
            
            a.style.display = 'none';
            a.href = url;
            a.download = `YTDownloader-${date}.mp4`;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            
            scriptContent.innerHTML = data['script-content'];
            // summaryContent.innerHTML = data['summary'];
            document.getElementById('script-gen').style.display = 'block';

        } catch (error) {
            document.getElementById('script-gen').style.display = 'none';
            console.error('', error);
            alert('Error occurred: ' + error.message);
            
        }
        document.getElementById('loading-ring').style.display = 'none';
    } else {
        alert("Please enter a Video link.");
    }
});

// Download Audio button clicked.
document.getElementById('downloadaudiobutton').addEventListener('click', async () => {
    const videoLink = document.getElementById('streamlink').value;

    // Validate YouTube link
    if (!isValidYouTubeURL(videoLink)) {
        alert("Please enter a valid YouTube link.");
        return;
    }

    // Send the link to the backend.
    if(videoLink) {
        document.getElementById('loading-ring').style.display = 'block';

        const endpointUrl = '/audio';

        try {
            const response = await fetch(endpointUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ link: videoLink })
            });

            const data = await response.json();

            // Check if the response contains an error
            if (data['error']) {
                // If error exists, throw an error
                throw new Error(data['error']);
            }

            // Show the video data
            document.getElementById('video-thumbnail').src = data.video_data.thumbnail;videoLink
            document.getElementById('video-title').innerText = data.video_data.title;
            document.getElementById('video-title').href = videoLink;
            document.getElementById('video-channel').innerText = data.video_data.channel;
            document.getElementById('video-channel').href = data.video_data.channel_url;
            document.getElementById('video-length').innerText = data.video_data.length + ' Seconds';
            document.getElementById('video-views').innerText = data.video_data.views + ' Views';
            document.getElementById('video-data').style.display = 'block';

            // Fetch the file and create a Blob URL
            const fileResponse = await fetch(`/download/${data.file_name}`);
            if (!fileResponse.ok) {
                throw new Error('File download failed: ' + fileResponse.statusText);
            }
            const blob = await fileResponse.blob();

            // Create a link to the file and click it to trigger download
            var link = document.createElement('a');
            link.href = window.URL.createObjectURL(blob);
            link.download = `${data.video_data.title}-YT Downloader.mp3`;  // Set the desired file name
            link.click();

        } catch (error) {
            console.error('error', error);
            alert('Error occurred: ' + error.message);
            
        }
        document.getElementById('loading-ring').style.display = 'none';
    } else {
        alert("Please enter a Video link.");
    }
});