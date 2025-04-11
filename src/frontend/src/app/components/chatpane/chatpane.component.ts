import { ChangeDetectorRef, Component, ElementRef, EventEmitter, Output, SimpleChanges, ViewChild } from '@angular/core';
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

  @Output() onNewTitle = new EventEmitter<string>();

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

    // Validate if this is a new chat
    // if it's the case we get the title
    if (this.selectedSession?.isNewChat) {
      this.selectedSession.isNewChat = false;
      this.chatService.newTile(this.selectedSession.id, prompt.value)
        .subscribe(title => {
          if (this.selectedSession)
            this.selectedSession.title = title;
          this.onNewTitle.emit(title);
        });
    }

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
