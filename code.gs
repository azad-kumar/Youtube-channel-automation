
function upload(video_data) 
{ try 
  { var video = UrlFetchApp.fetch(video_data.video_url); 


  YouTube.Videos.insert(
    { snippet: 
      { title: "everyday motivation", description: video_data.title, tags: ["motivation"] }, status: { privacyStatus: "public", }, 
    }, "snippet,status", video); 
  Logger.log("upload successful");
  return ContentService.createTextOutput("done") } 
  catch (err) { 
    Logger.log(err.message)
    return ContentService.createTextOutput(err.message) } 
}


function start() {
  try {
    var video_url = UrlFetchApp.fetch("PRIVATE URL : NOT FOR PUBLIC");
    var content = video_url.getContentText();
    var responseJson = JSON.parse(content);
    if (responseJson.status == true)
    {
      var url =  responseJson.response; // Log the status property from the JSON response
      return sendPostRequest(url);
    }
    else
    {
      Logger.log("empty url")
      return false
    }
    
  } catch (err) {
    Logger.log(err);
    return false
  }
}


function sendPostRequest(url) {
  try {
    var url_ = "PRIVATE URL : NOT FOR PUBLIC";
    var payload = {
      'url': url,
    };

    var options = {
      method: "post",
      contentType: "application/json",
      payload: JSON.stringify(payload)
    };

    var response = UrlFetchApp.fetch(url_, options);
    var content = response.getContentText();
    var data_dict = JSON.parse(content);
    var video_data = {
        'title' : data_dict.meta.title,
        'video_url' : data_dict.url[0].url,
        'thumbnail' : data_dict.thumb
    };
    return video_data;
  } catch (error) {
    Logger.log(error);
    return false;
  }

}

function Pin_download(video_data) {
  try {
    var url_ = "PRIVATE URL : NOT FOR PUBLIC";
    var payload = {
      'VideoLink': video_data.video_url,
    };

    var options = {
      method: "post",
      contentType: "application/json",
      payload: JSON.stringify(payload)
    };

    var response = UrlFetchApp.fetch(url_, options);
    var content = response.getContentText();
    var data_dict = JSON.parse(content);
    if (data_dict.status == true){
      Logger.log("download successful")
      return true;
    }
    else{
      return false
    }
    
  } catch (error) {
    Logger.log(error);
    return false;
  }

}




function upload_video(){
  video_data = start();
  if (video_data != false)
  {
    try{
      Pin_download(video_data)
    }
    catch(error)
    {
      Logger.log('pinterest video not downloded')
    }
    try{
      upload(video_data);
      
    }
    catch(error)
    {
      Logger.log("upload Failes")
    }
    
  }
  
}






