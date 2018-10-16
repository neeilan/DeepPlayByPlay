const {Builder, By, Key, until} = require('selenium-webdriver');
var shortid = require('shortid');
var elementId = 'statsPlayer_embed_statsPlayer';
var axios = require('axios');
var fs = require('fs');

var adblock = "load-extension=cjpalhdlnbpafiamejdnhcphjbkeiagm";

function saveBinaryFileAs(outputFileName, url) {
  return axios.request({
    responseType: 'arraybuffer',
    url: url,
    method: 'get',
  }).then((result) => {
    fs.writeFileSync('massdl2/' + shortid.generate() + " " + outputFileName + '.mp4', result.data);
  });
}

var adBlockPlus = require('adblock-plus-crx')
const chromeOptions = new (require('selenium-webdriver/chrome').Options)();
chromeOptions.addExtensions([adBlockPlus.base64()]);
chromeOptions.addArguments('mute-audio');


var retryQueue = [];
var retried = new Set();

async function downloadVideoFile (desc, url) {
  if (desc.indexOf('FREE THROW') > -1) return;

  let driver = await new Builder().forBrowser('chrome').setChromeOptions(chromeOptions).build();
  try {
    await driver.get(url);
    let videoTag =
       await driver.wait(until.elementLocated(By.id(elementId)), 100000);
    await videoTag.click();

    setTimeout(() => {
        videoTag.getAttribute('src').then((videoPath) => {
           if (videoPath.indexOf('blank') > -1 || videoPath.indexOf('2016/11/22') > -1) { console.log('BLANK'); }
           else { console.log(videoPath); saveBinaryFileAs(desc, videoPath); }
           driver.quit();
        });
    }, 8500);

  } catch(err) {
    console.log('ERROR... Pushing to retry queue');
    // retryQueue.push({ desc: desc, url: url  });
    fs.appendFileSync('failures', desc + '\n' + url + '\n');
    driver.quit();
  } finally {
  }
};

/* To avoid rate-limiting */
var _scheduled = 1;
function schedule(fn) {
  setTimeout(fn, 20000 * _scheduled++);
}

function downloadVideos(file, numPlays) {
  /* Downloads videos for the first numPlays plays */

  var stream = require('fs').createReadStream(file);
  var lineReader = require('readline').createInterface({
    input: stream
  });


  var linesToRead = numPlays * 2;
  var currLine = 0;

  var isPlayLine = true;
  var currPlay;

  lineReader.on('line', function (line) {
    if (currLine++ >= linesToRead) return false;
    
    if (isPlayLine) {
      currPlay = line;
    } else {
      // url line
      schedule(downloadVideoFile.bind(null, currPlay, line));
    }
    isPlayLine = !isPlayLine;
  });
};

// Specify game file with play info, and how many plays to download.
const filePath = 'path_to_plays_file';
const numPlaysToDownload = 100;
downloadVideos(filePath, numPlaysToDownload);

/*
// Schedule retry checker - Retry failures once, or append it to failures file to check later
setInterval(function retry() {
  console.log('ATTEMPTING RETRIES');
  while (retryQueue.length > 0) {
    var retryCandidate = retryQueue.pop();
    if (!retried.has(retryCandidate.url)) {
      retried.add(retryCandidate.url);
      downloadVideoFile(retryCandidate.desc, retryCandidate.url);
    } else {
      fs.appendFileSync('failures', retryCandidate.desc + '\n' + retryCandidate.url + '\n');
    }
  }
}, 1000 * 60 * 2);
*/
