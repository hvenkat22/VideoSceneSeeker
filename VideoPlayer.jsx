// Inside VideoPlayer.jsx
import React from 'react';

const VideoPlayer = ({ file }) => {
  const videoUrl = URL.createObjectURL(file);

  return (
    <video width="800" height="800" controls>
      <source src={videoUrl} type="video/mp4" />
      Your browser does not support the video tag.
    </video>
  );
};

export default VideoPlayer;
