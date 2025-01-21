const mark = document.querySelector('#main .leaderboard .mark');
console.log(mark);
mark.onclick = function() {
    const leaderboard = document.querySelector('#main .leaderboard');
    leaderboard.style.display = 'none';
}

const leaderboardBtn = document.querySelector('#main .options .leaderboard-btn');
leaderboardBtn.onclick = function() {
    const leaderboard = document.querySelector('#main .leaderboard');
    leaderboard.style.display = 'flex';
}

