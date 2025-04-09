import { Component, SimpleChanges } from '@angular/core';
import { Session } from '../../models/session';
import { Message } from '../../models/message';
import { Input } from '@angular/core';
import { ChatService } from '../../services/chat.service';
import { NgFor, NgIf } from '@angular/common';
import { StateService } from '../../services/state.service';

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

  constructor(private chatService: ChatService, private stateService: StateService) { }

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

    if (this.selectedSession) {
      this.stateService.isLoading = true;
      this.chatService.sendQuestion(this.selectedSession?.sessionId, prompt).subscribe(message => {
        this.messages.push(message);
        this.stateService.isLoading = false;
      })
    }
  }

}
