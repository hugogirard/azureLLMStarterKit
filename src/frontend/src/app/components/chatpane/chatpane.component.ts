import { Component, SimpleChanges } from '@angular/core';
import { Session } from '../../models/session';
import { Message } from '../../models/message';
import { Input } from '@angular/core';
import { ChatService } from '../../services/chat.service';

@Component({
  selector: 'chatpane',
  standalone: true,
  imports: [],
  templateUrl: './chatpane.component.html',
  styleUrl: './chatpane.component.css'
})
export class ChatpaneComponent {
  @Input() selectedSession?: Session;

  constructor(private chatService: ChatService) { }

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['selectedSession']) {
      if (changes['selectedSession'].currentValue != null) {
        // Load all message sessions
      }
    }
  }

  sendPrompt(prompt: string) {

  }
}
