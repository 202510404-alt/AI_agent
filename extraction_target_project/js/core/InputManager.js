/**
 * js/core/InputManager.js
 * 단일화 입력 및 네트워크 패킷 제어기
 * 
 * InputHandler를 래핑 및 상속하여 네트워크 송수신 및 AI 모드 전환 제어 기능을 제공합니다.
 */
import { InputHandler } from './input.js';

export class InputManager extends InputHandler {
    constructor() {
        super();
        this.networkManager = null;
    }

    /**
     * 네트워크 매니저 인스턴스 연동
     * @param {import('../network/networkManager.js').NetworkManager} net 
     */
    attachNetworkManager(net) {
        this.networkManager = net;
    }

    /**
     * 현재 프레임 조작을 네트워크 패킷으로 압축하여 서버로 발송
     * @param {number} slotIndex 
     * @param {object} [context] 
     */
    flushInputToNetwork(slotIndex, context = null) {
        const action = this.getInputAction(slotIndex, context);
        if (this.networkManager && slotIndex) {
            this.networkManager.sendInputSync(slotIndex, action);
        }
        return action;
    }
}

export default InputManager;
