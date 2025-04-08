export interface Message {
    id: string;
    prompt: string;
    type: string;
    sessionId: string;
    username: string;
    completion: string;
}