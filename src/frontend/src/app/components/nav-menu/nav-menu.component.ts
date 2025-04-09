import { Component, EventEmitter, Output } from '@angular/core';
import { StateService } from '../../services/state.service'
import { ChatService } from '../../services/chat.service';
import { Session } from '../../models/session';
import { NgFor, NgIf } from '@angular/common'

@Component({
  selector: 'nav-menu',
  standalone: true,
  imports: [NgFor, NgIf],
  templateUrl: './nav-menu.component.html',
  styleUrl: './nav-menu.component.css'
})
export class NavMenuComponent {

  sessions: Session[] = [];

  selectedSession?: Session;

  @Output() sessionSelected = new EventEmitter<Session>();

  constructor(private stateService: StateService,
    private chatService: ChatService
  ) { }

  ngOnInit() {
    this.getSessionsUser();
  }

  createNewChat() {
    this.stateService.isLoading = true;
    this.chatService.newSession().subscribe(session => {
      this.stateService.isLoading = false;
      this.selectedSession = session ?? undefined;
      if (session) {
        this.selectedSession = session;
        this.sessionSelected.emit(session);
        this.sessions.push(session);
      }
    });
  }

  getSessionsUser() {
    this.stateService.isLoading = true;
    this.chatService.getSessions().subscribe(sessions => {
      this.stateService.isLoading = false;
      this.sessions = sessions;
      if (this.sessions.length > 0) {
        const session = sessions[0]
        this.sessionSelected.emit(session);
        this.selectedSession = session;
      }
    });
  }
}
