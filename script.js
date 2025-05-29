// 游戏常量
const GRID_SIZE = 20;
const GAME_SPEED = 100;
const INITIAL_SNAKE_LENGTH = 3;

// 游戏变量
let canvas, ctx;
let snake = [];
let food = {};
let direction = 'right';
let nextDirection = 'right';
let gameLoop;
let score = 0;
let isGameRunning = false;

// 鼓励消息
const motivationalMessages = [
    '一定要加油每一天！',
    '继续加油，你做得很棒！',
    '坚持就是胜利！',
    '今天也要充满活力！',
    '加油，突破自己！'
];

// 初始化游戏
function initGame() {
    canvas = document.getElementById('game-board');
    ctx = canvas.getContext('2d');
    
    // 初始化蛇的位置
    const startX = Math.floor(canvas.width / (2 * GRID_SIZE)) * GRID_SIZE;
    const startY = Math.floor(canvas.height / (2 * GRID_SIZE)) * GRID_SIZE;
    
    snake = [];
    for (let i = 0; i < INITIAL_SNAKE_LENGTH; i++) {
        snake.push({x: startX - i * GRID_SIZE, y: startY});
    }
    
    generateFood();
    updateScore(0);
}

// 生成食物
function generateFood() {
    const maxX = canvas.width / GRID_SIZE - 1;
    const maxY = canvas.height / GRID_SIZE - 1;
    
    do {
        food = {
            x: Math.floor(Math.random() * maxX) * GRID_SIZE,
            y: Math.floor(Math.random() * maxY) * GRID_SIZE
        };
    } while (snake.some(segment => segment.x === food.x && segment.y === food.y));
}

// 更新分数
function updateScore(newScore) {
    score = newScore;
    document.getElementById('score').textContent = score;
    
    // 在达到特定分数时显示鼓励消息
    if (score > 0 && score % 5 === 0) {
        showMotivationalMessage();
    }
}

// 显示鼓励消息
function showMotivationalMessage() {
    const message = motivationalMessages[Math.floor(Math.random() * motivationalMessages.length)];
    const messageDiv = document.createElement('div');
    messageDiv.className = 'motivation-message';
    messageDiv.textContent = message;
    document.querySelector('.game-container').appendChild(messageDiv);
    
    setTimeout(() => messageDiv.remove(), 2000);
}

// 游戏主循环
function gameStep() {
    if (!isGameRunning) return;
    
    direction = nextDirection;
    const head = {x: snake[0].x, y: snake[0].y};
    
    // 根据方向移动蛇头
    switch(direction) {
        case 'up': head.y -= GRID_SIZE; break;
        case 'down': head.y += GRID_SIZE; break;
        case 'left': head.x -= GRID_SIZE; break;
        case 'right': head.x += GRID_SIZE; break;
    }
    
    // 检查碰撞
    if (isCollision(head)) {
        gameOver();
        return;
    }
    
    // 移动蛇
    snake.unshift(head);
    
    // 检查是否吃到食物
    if (head.x === food.x && head.y === food.y) {
        updateScore(score + 1);
        generateFood();
    } else {
        snake.pop();
    }
    
    // 绘制游戏画面
    drawGame();
}

// 检查碰撞
function isCollision(head) {
    // 检查墙壁碰撞
    if (head.x < 0 || head.x >= canvas.width ||
        head.y < 0 || head.y >= canvas.height) {
        return true;
    }
    
    // 检查自身碰撞
    return snake.some(segment => segment.x === head.x && segment.y === head.y);
}

// 绘制游戏画面
function drawGame() {
    // 清空画布
    ctx.fillStyle = '#ecf0f1';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    
    // 绘制蛇
    ctx.fillStyle = '#2c3e50';
    snake.forEach((segment, index) => {
        if (index === 0) {
            // 蛇头使用不同颜色
            ctx.fillStyle = '#e74c3c';
        } else {
            ctx.fillStyle = '#2c3e50';
        }
        ctx.fillRect(segment.x, segment.y, GRID_SIZE - 1, GRID_SIZE - 1);
    });
    
    // 绘制食物
    ctx.fillStyle = '#27ae60';
    ctx.fillRect(food.x, food.y, GRID_SIZE - 1, GRID_SIZE - 1);
}

// 游戏结束
function gameOver() {
    isGameRunning = false;
    clearInterval(gameLoop);
    alert(`游戏结束！你的得分是: ${score}\n记住：一定要加油每一天！`);
}

// 开始游戏
function startGame() {
    if (isGameRunning) return;
    
    initGame();
    isGameRunning = true;
    gameLoop = setInterval(gameStep, GAME_SPEED);
}

// 事件监听
document.addEventListener('DOMContentLoaded', () => {
    // 键盘控制
    document.addEventListener('keydown', (e) => {
        switch(e.key) {
            case 'ArrowUp':
                if (direction !== 'down') nextDirection = 'up';
                break;
            case 'ArrowDown':
                if (direction !== 'up') nextDirection = 'down';
                break;
            case 'ArrowLeft':
                if (direction !== 'right') nextDirection = 'left';
                break;
            case 'ArrowRight':
                if (direction !== 'left') nextDirection = 'right';
                break;
        }
    });
    
    // 按钮控制
    document.getElementById('start-btn').addEventListener('click', startGame);
    document.getElementById('up-btn').addEventListener('click', () => {
        if (direction !== 'down') nextDirection = 'up';
    });
    document.getElementById('down-btn').addEventListener('click', () => {
        if (direction !== 'up') nextDirection = 'down';
    });
    document.getElementById('left-btn').addEventListener('click', () => {
        if (direction !== 'right') nextDirection = 'left';
    });
    document.getElementById('right-btn').addEventListener('click', () => {
        if (direction !== 'left') nextDirection = 'right';
    });
});
