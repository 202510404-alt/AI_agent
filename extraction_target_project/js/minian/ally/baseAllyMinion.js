/**
 * js/minian/ally/baseAllyMinion.js
 * 모든 아군 소환수/드론의 공통 베이스 클래스
 */
export class BaseAllyMinion {
    constructor(owner, config = {}) {
        this.owner = owner;               // 소환한 플레이어
        this.x = config.x || owner.x;
        this.y = config.y || owner.y;
        this.radius = config.radius || 12;
        this.hp = config.hp || 3;
        this.maxHp = config.maxHp || 3;
        this.color = config.color || '#10b981';
        
        this.isAlly = true;               // 아군 판정
        this.isDead = false;
        
        this.attackTimer = 0;
        this.fireRate = config.fireRate || 1.0;
    }

    takeDamage(amount) {
        if (this.isDead) return;
        this.hp -= amount;
        if (this.hp <= 0) {
            this.hp = 0;
            this.isDead = true;
        }
    }

    findClosestTarget(enemyEntities = []) {
        let closest = null;
        let minDist = Infinity;

        for (const enemy of enemyEntities) {
            if (!enemy || enemy.isDead) continue;
            const dist = Math.hypot(enemy.x - this.x, enemy.y - this.y);
            if (dist < minDist) {
                minDist = dist;
                closest = enemy;
            }
        }
        return closest;
    }

    updateMovement(enemyEntities, dt) {
        if (this.owner && typeof this.owner.isStunned === 'function' && this.owner.isStunned()) {
            this.isDead = true;
        }
    }

    updateAttack(enemyEntities, allyBullets, dt) {}

    draw(ctx) {}
}

export default BaseAllyMinion;