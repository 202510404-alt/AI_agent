/** 네크로맨서 탄환의 미구현 더미. */
export class NecromancerBullet {
    constructor(x, y, angle, mode = 'straight') {
        this.x = x;
        this.y = y;
        this.angle = angle;
        this.mode = mode;
        this.color = '#a855f7';
        this.isAlly = false;
        this.isDead = false;
        this.implemented = false;
    }

    // 유도·직선 전환 및 렌더링은 본 구현 단계에서 연결한다.
    update() {}
    draw() {}
}

export default NecromancerBullet;
