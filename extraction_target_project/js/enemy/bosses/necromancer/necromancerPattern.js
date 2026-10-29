/** 네크로맨서 패턴의 미구현 명세. */
export const NECROMANCER_PATTERNS = [
    { id: 'zombieSpawn', name: '8방향 사방 좀비 스폰', count: 8, perWall: 2,
        walls: ['top', 'bottom', 'left', 'right'], targeting: 'nearestPlayerAtSpawn', movement: 'straight', positionSeed: null },
    { id: 'staffBarrage', name: '지팡이 집중 사격', origin: 'staffOrb',
        targeting: 'nearestPlayer', bulletColor: 'purple', randomChannel: 'bossPattern' },
    { id: 'homingToStraight', name: '유도 후 직선 전환 회전 탄막',
        targeting: 'nearestPlayer', movement: 'homingThenStraight', randomChannel: 'bossPattern' },
    { id: 'poisonMist', name: '타깃팅 범위 독안개', targeting: 'nearestPlayer', shape: 'circle',
        warningSeconds: 1.5, durationSeconds: 3, damageTicks: 2, color: 'lightGreen', randomChannel: 'bossPattern' }
];

export class NecromancerPattern {
    // 패턴 실행은 본 구현 단계에서 연결한다.
    static execute() {}
}

export default NecromancerPattern;
