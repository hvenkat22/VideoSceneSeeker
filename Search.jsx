import React, { useState } from 'react';
import ReactDOM from 'react-dom';
import VideoPlayer from '../components/VideoPlayer';
import SparkleIcon from '../components/Sparkle';
import Spinner from '../components/Spinner';
import VidIcon from '../components/VidIcon';

const Search = () => {
  const [videoFile, setVideoFile] = useState(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResult, setSearchResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleInputChange = (event) => {
    const file = event.target.files[0]; // Get the selected file from the input
    setVideoFile(file); // Update the videoFile state with the selected file
  };

  const handleSearch = async () => {
    setLoading(true);
    const formData = new FormData();
    formData.append('file', videoFile);
    formData.append('query', searchQuery);

    try {
      const response = await fetch('/video/search', {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();
      setSearchResult(data.timestamp || 'Query not found');
    } catch (error) {
      console.error('Error searching video:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <body>
      <div className='p-4'>
        <VidIcon/>
        <h1 className='text-3xl text-white  my-8 text-center'>Welcome to the Scene Searcher!</h1>
        <div className='flex flex-col border-2 border-white rounded-xl w-[600px] p-4 mx-auto'>
          <center>
            {/* Use VideoPlayer component to display the selected video */}
            {videoFile && <VideoPlayer file={videoFile} />}
          </center>
          {/* Conditional rendering: show input search bar and button only if videoFile exists */}
          {videoFile && (
            <center><div className="text-center my-4">
              <input
                type="text-3xl my-4"
                placeholder="Enter the scene to search for"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="mt-4 p-2 rounded-md border border-white text-black w-full"
              />
              <div className='flex items-center'><p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</p><SparkleIcon  /><button className="p-1 bg-purple-500 m-8 flex flex-col border-2 border-black" onClick={handleSearch} disabled={loading}>Search</button><SparkleIcon /></div>
            </div></center>
          )}
          {/* File input for selecting a video file */}
          {!videoFile && (
            <input
              type="file" // Use file input type to allow selecting a video file
              accept="video/*" // Specify accepted file types as video files
              onChange={handleInputChange} // Call handleInputChange function when file input changes
              className="mt-4 p-2 rounded-md border border-white text-white"
            />
          )}
          {/* Display search result */}
          {searchResult && (
            <div className="mt-4 p-2 rounded-md border border-white text-white">
              {searchResult}
            </div>
          )}
          {/* Display loading spinner */}
          {loading ? <Spinner /> : ''}
        </div>
      </div>
    </body>
  );
}

export default Search;
