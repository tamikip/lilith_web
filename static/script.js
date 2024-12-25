document.addEventListener('DOMContentLoaded', () => {
    const messageElement = document.getElementById('message');
    const timeElement = document.getElementById('time');
    const commentsContainer = document.getElementById('comments');
    const commentForm = document.getElementById('comment-form');
    const newCommentInput = document.getElementById('new-comment');
    const toggleCommentsButton = document.getElementById('toggle-comments');
    const commentsContainerElement = document.getElementById('comments-container');
    const toggleText = document.getElementById('toggle-text');

    let eventTimes = generateRandomTimes();

    function getRandomTime(start, end) {
        return Math.floor(Math.random() * (end - start + 1)) + start;
    }

    function generateRandomTimes() {
        return {
            lunchStart: getRandomTime(11, 12),
            dinnerStart: getRandomTime(17, 19),
            sleepStart: getRandomTime(21, 23),
            sleepEnd: getRandomTime(5, 7)
        };
    }

    function updateTimeAndMessage() {
        const now = new Date();
        const hours = now.getHours();
        const minutes = String(now.getMinutes()).padStart(2, '0');
        const seconds = String(now.getSeconds()).padStart(2, '0');

        timeElement.textContent = `${hours}:${minutes}:${seconds}`;

        let newMessage = '莉莉丝在直播';
        let shouldUpdateTimes = false;

        if (hours === eventTimes.lunchStart) {
            newMessage = '莉莉丝在吃午饭';
            shouldUpdateTimes = true;
        } else if (hours === eventTimes.dinnerStart) {
            newMessage = '莉莉丝在吃晚饭';
            shouldUpdateTimes = true;
        } else if (hours === eventTimes.sleepStart || (hours >= 0 && hours < eventTimes.sleepEnd)) {
            newMessage = '莉莉丝睡着了';
            if (hours === eventTimes.sleepEnd - 1) {
                shouldUpdateTimes = true;
            }
        }

        if (shouldUpdateTimes) {
            eventTimes = generateRandomTimes();
        }

        messageElement.textContent = newMessage;
    }

    setInterval(updateTimeAndMessage, 1000);
    updateTimeAndMessage();

    toggleCommentsButton.addEventListener('click', () => {
        commentsContainerElement.classList.toggle('expanded');
        const isExpanded = commentsContainerElement.classList.contains('expanded');
        toggleText.textContent = isExpanded ? '收起评论' : '展开评论';
    });

    commentForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const commentText = newCommentInput.value.trim();
        if (commentText) {
            const comment = document.createElement('div');
            comment.className = 'comment';
            comment.innerHTML = `
                <p>${commentText}</p>
                <time>${new Date().toLocaleTimeString()}</time>
            `;
            commentsContainer.appendChild(comment);
            newCommentInput.value = '';
        }
    });
});

document.addEventListener('DOMContentLoaded', function () {
    const imgElement = document.getElementById('animeImage');

    function refreshImage() {
        const timestamp = new Date().getTime(); // 获取当前时间戳
        const originalSrc = imgElement.src.split('?')[0]; // 去掉之前的时间戳
        imgElement.src = `${originalSrc}?t=${timestamp}`; // 添加新的时间戳
    }

    setInterval(refreshImage, 5000); // 每5000毫秒（5秒）执行一次
});


