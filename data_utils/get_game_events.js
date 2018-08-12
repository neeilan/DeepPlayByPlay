const axios = require('axios');
const fs = require('fs');


function downloadPlays(gameId) {
    const url = `http://stats.nba.com/stats/playbyplayv2?EndPeriod=10&EndRange=55800&GameID=${gameId}&RangeType=2&Season=2017-18&SeasonType=Regular+Season&StartPeriod=1&StartRange=0`;

    function getPlayEvent(gameId, eventId, title, season = '2017-18') {
        return {
            'url': `http://stats.nba.com/events/?flag=1&GameID=${gameId}&GameEventID=${eventId}&Season=${season}&sct=plot`,
            'desc': title
        };
    }

    function includePlay(playDesc) {
        if (!playDesc || playDesc.indexOf('FREE') > -1) return false; // Free throws aren't recorded

        var validTerms = ['SHOT', 'LAYUP', 'DUNK', 'MISS', 'FADE'];
        for (var i = 0; i < validTerms.length; i++) {
            if (playDesc.indexOf(validTerms[i]) > -1) {
                return true;
            }
        }

        return false;
    }

    function generateTitle(play) {
        var title = "";
        if (play[7] != null) title += play[7];
        if (play[8] != null) title += play[8];
        if (play[9] != null) title += play[9];
        return title.toUpperCase();
    }

    function writeToDisk(gameId, events) {
        events.forEach(event => {
            var filename = './plays/' + gameId;
            fs.appendFileSync(filename, event.desc + '\n' + event.url + '\n');
        });
    }

    axios.get(url)
        .then(res => res.data.resultSets[0].rowSet)
        .then(plays => plays.map(play => getPlayEvent(gameId, play[1], generateTitle(play))))
        .then(events => events.filter(event => includePlay(event.desc)))
        .then(events => writeToDisk(gameId, events));

};


// Read in game ids and get the list of play events for each game

const gameIdsFile = 'games_ids';

var lineReader = require('readline').createInterface({
    input: require('fs').createReadStream(gameIdsFile)
});

// Set a counter to limit long-running jobs
var counter = 0;

lineReader.on('line', function(line) {
    if (counter < 20) {
        counter++;
        console.log('Downloading ' + line.trim());
        downloadPlays(line.trim());
    }
});
