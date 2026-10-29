/** 네크로맨서의 직선 탄환과 유도 후 직선 탄환. */
export class NecromancerBullet {
    constructor(x, y, angle, mode = 'straight') {
        this.x = x;
        this.y = y;
        this.angle = angle;
        this.mode = mode;
        this.speed = mode === 'homing' ? 150 : 240;
        this.radius = 5;
        this.damage = 1;
        this.locked = false;
        this.color = '#a855f7';
        this.isAlly = false;
        this.isDead = false;
    }

    update(players = [], dt = 1 / 60) {
        if (this.mode === 'homing' && !this.locked) {
            let closest = null;
            let minDistance = Infinity;
            for (const player of players) {
                if (!player || player.isDead) continue;
                const distance = Math.hypot(player.x - this.x, player.y - this.y);
                if (distance < minDistance) { minDistance = distance; closest = player; }
            }
            if (closest && minDistance <= 100) {
                this.locked = true;
                this.speed = 260;
            } else if (closest) {
                const targetAngle = Math.atan2(closest.y - this.y, closest.x - this.x);
                const difference = Math.atan2(Math.sin(targetAngle - this.angle), Math.cos(targetAngle - this.angle));
                this.angle += Math.max(-1.5 * dt, Math.min(1.5 * dt, difference));
            }
        }
        this.x += Math.cos(this.angle) * this.speed * dt;
        this.y += Math.sin(this.angle) * this.speed * dt;
    }

    draw(ctx) {
        ctx.save();
        ctx.fillStyle = this.color;
        ctx.shadowColor = '#c084fc';
        ctx.shadowBlur = 12;
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
        ctx.fill();
        ctx.restore();
    }

    isOutOfBounds(width, height) {
        return this.isDead || this.x < -20 || this.x > width + 20 || this.y < -20 || this.y > height + 20;
    }
}

export default NecromancerBullet;
