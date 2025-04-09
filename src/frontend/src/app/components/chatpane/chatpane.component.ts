import { ChangeDetectorRef, Component, ElementRef, SimpleChanges, ViewChild } from '@angular/core';
import { Session } from '../../models/session';
import { Message } from '../../models/message';
import { Input } from '@angular/core';
import { ChatService } from '../../services/chat.service';
import { NgFor, NgIf } from '@angular/common';
import { StateService } from '../../services/state.service';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'chatpane',
  standalone: true,
  imports: [NgIf, NgFor, FormsModule],
  templateUrl: './chatpane.component.html',
  styleUrl: './chatpane.component.css'
})
export class ChatpaneComponent {
  @Input() selectedSession?: Session;

  @ViewChild('messagesInChatDiv') messagesInChatDiv?: ElementRef;

  messages: Message[] = []

  constructor(private chatService: ChatService, private stateService: StateService) { }

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['selectedSession']) {
      if (changes['selectedSession'].currentValue != null) {

        if (this.selectedSession) {
          this.chatService.getMessageSession(this.selectedSession.sessionId)
            .subscribe(messages => {
              this.messages = messages
              this.scrollEndPage();
            });
        }
      } else {
        this.messages = [];
      }
    }
  }

  sendPrompt(prompt: HTMLInputElement) {
    if (prompt.value.length == 0)
      return;

    if (this.selectedSession) {
      this.stateService.isLoading = true;
      this.chatService.sendQuestion(this.selectedSession?.sessionId, prompt.value).subscribe(message => {
        prompt.value = '';
        this.messages.push(message);
        this.stateService.isLoading = false;
      })
    }
  }

  private scrollEndPage() {
    if (this.messagesInChatDiv) {
      const elem = this.messagesInChatDiv.nativeElement;
      elem.scrollTop = elem.scrollHeight;
    }
  }

}
