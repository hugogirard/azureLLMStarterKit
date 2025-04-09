import { Component, SimpleChanges } from '@angular/core';
import { Session } from '../../models/session';
import { Message } from '../../models/message';
import { Input } from '@angular/core';
import { ChatService } from '../../services/chat.service';
import { NgFor, NgIf } from '@angular/common';

@Component({
  selector: 'chatpane',
  standalone: true,
  imports: [NgIf, NgFor],
  templateUrl: './chatpane.component.html',
  styleUrl: './chatpane.component.css'
})
export class ChatpaneComponent {
  @Input() selectedSession?: Session;

  messages: Message[] = []

  constructor(private chatService: ChatService) { }

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['selectedSession']) {
      if (changes['selectedSession'].currentValue != null) {

        if (this.selectedSession) {
          this.chatService.getMessageSession(this.selectedSession.sessionId)
            .subscribe(messages => {
              messages = messages
            });
        }

      }
    }
  }

  sendPrompt(prompt: string) {
    if (prompt.length == 0)
      return;
  }

}
