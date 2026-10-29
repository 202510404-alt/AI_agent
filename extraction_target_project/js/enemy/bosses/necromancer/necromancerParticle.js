/** 별도 난수 소비 없이 구슬 주변 연기를 그린다. */
export const NECROMANCER_PARTICLE_DATA = {
    id: 'purpleOrbSmoke', color: 'purple', origin: 'staffOrb', implemented: true
};

export function createNecromancerParticles(ctx, x, y, time = 0) {
    ctx.save();
    for (let i = 0; i < 5; i++) {
        const phase = time * 2 + i * 1.4;
        ctx.beginPath();
        ctx.arc(x + Math.sin(phase) * 9, y - 6 - ((time * 12 + i * 8) % 30), 4 + i * 0.5, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(168, 85, 247, ${0.12 + i * 0.025})`;
        ctx.fill();
    }
    ctx.restore();
}
